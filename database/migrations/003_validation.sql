BEGIN;
ALTER TABLE pos.cash_sessions DROP CONSTRAINT cash_sessions_check;
ALTER TABLE pos.cash_sessions ADD CONSTRAINT cash_sessions_check CHECK ((closed_at IS NULL AND closed_by IS NULL AND counted_cash IS NULL) OR (closed_at IS NOT NULL AND closed_at >= opened_at AND closed_by IS NOT NULL AND counted_cash IS NOT NULL));
CREATE OR REPLACE FUNCTION pos.receive_sale(p_operation uuid, p_terminal uuid, p_payload jsonb)
RETURNS uuid LANGUAGE plpgsql SECURITY DEFINER SET search_path=pg_catalog,pos AS $$
DECLARE
 t pos.terminals%ROWTYPE; old pos.sync_receipts%ROWTYPE; cs pos.cash_sessions%ROWTYPE;
 sid uuid; item jsonb; pay jsonb; seller jsonb; pid uuid; qty integer; price numeric;
 subtotal numeric := 0; total numeric; disc numeric; paytotal numeric := 0;
 line integer := 0; existing_qty bigint; shortage jsonb := '[]'; happened timestamptz;
 cashier uuid; zone text;
BEGIN
 IF p_operation IS NULL OR p_terminal IS NULL OR p_payload IS NULL THEN RAISE EXCEPTION 'Missing operation, terminal or payload'; END IF;
 -- Global operation lock handles simultaneous retries even across different terminals.
 PERFORM pg_advisory_xact_lock(hashtextextended(p_operation::text,0));
 SELECT * INTO old FROM pos.sync_receipts WHERE operation_id=p_operation;
 IF FOUND THEN
  IF old.terminal_id<>p_terminal OR old.payload<>p_payload THEN RAISE EXCEPTION 'Operation ID reused with different content'; END IF;
  RETURN old.sale_id;
 END IF;
 SELECT * INTO STRICT t FROM pos.terminals WHERE id=p_terminal;
 -- Do not reject old offline sales merely because a terminal was later deactivated.
 PERFORM 1 FROM pos.locations WHERE id=t.location_id FOR UPDATE;
 IF jsonb_typeof(p_payload->'lines') IS DISTINCT FROM 'array' OR jsonb_typeof(p_payload->'payments') IS DISTINCT FROM 'array'
    OR jsonb_typeof(p_payload->'sellers') IS DISTINCT FROM 'array' THEN RAISE EXCEPTION 'Expected lines, payments and sellers arrays'; END IF;
 IF jsonb_array_length(p_payload->'lines')=0 OR jsonb_array_length(p_payload->'payments')=0 THEN RAISE EXCEPTION 'Empty sale'; END IF;
 IF jsonb_typeof(p_payload->'captured_offline') IS DISTINCT FROM 'boolean' THEN RAISE EXCEPTION 'captured_offline must be boolean'; END IF;
 IF coalesce(p_payload->>'local_sequence','') !~ '^[1-9][0-9]*$' THEN RAISE EXCEPTION 'Sequence must be a positive integer'; END IF;
 -- Explicit offset is mandatory so the database session timezone cannot change meaning.
 IF coalesce(p_payload->>'occurred_at','') !~ '(Z|[+-][0-9]{2}:[0-9]{2})$' THEN RAISE EXCEPTION 'Timestamp requires an explicit offset'; END IF;
 happened := (p_payload->>'occurred_at')::timestamptz;
 sid := (p_payload->>'sale_id')::uuid; cashier := (p_payload->>'cashier_id')::uuid;
 SELECT timezone INTO zone FROM pos.branches WHERE id=t.branch_id;
 SELECT * INTO STRICT cs FROM pos.cash_sessions WHERE id=(p_payload->>'cash_session_id')::uuid AND terminal_id=t.id;
 IF happened<cs.opened_at OR (cs.closed_at IS NOT NULL AND happened>cs.closed_at) THEN RAISE EXCEPTION 'Sale outside its cash session'; END IF;
 disc := (p_payload->>'discount')::numeric;
 IF disc IS NULL OR disc<0 OR disc<>round(disc,2) OR disc='NaN'::numeric THEN RAISE EXCEPTION 'Invalid discount'; END IF;
 FOR item IN SELECT value FROM jsonb_array_elements(p_payload->'lines') LOOP
  IF coalesce(item->>'quantity','') !~ '^[1-9][0-9]*$' THEN RAISE EXCEPTION 'Quantity must be a positive integer'; END IF;
  qty := (item->>'quantity')::integer; price := (item->>'unit_price')::numeric;
  IF price IS NULL OR price<0 OR price<>round(price,2) OR price='NaN'::numeric THEN RAISE EXCEPTION 'Invalid unit price'; END IF;
  subtotal := subtotal+qty*price;
 END LOOP;
 total := subtotal-disc;
 FOR pay IN SELECT value FROM jsonb_array_elements(p_payload->'payments') LOOP
  price := (pay->>'amount')::numeric;
  IF price IS NULL OR price<=0 OR price<>round(price,2) OR price='NaN'::numeric THEN RAISE EXCEPTION 'Invalid payment'; END IF;
  paytotal := paytotal+price;
 END LOOP;
 IF total<=0 OR paytotal<>total THEN RAISE EXCEPTION 'Payments do not cover the exact net total'; END IF;
 INSERT INTO pos.sales(id,terminal_id,branch_id,cash_session_id,cashier_id,local_sequence,occurred_at,business_timezone,clock_source,captured_offline,subtotal,discount,total)
 VALUES(sid,t.id,t.branch_id,cs.id,cashier,(p_payload->>'local_sequence')::bigint,happened,zone,'terminal',(p_payload->>'captured_offline')::boolean,subtotal,disc,total);
 FOR item IN SELECT value FROM jsonb_array_elements(p_payload->'lines') LOOP
  line:=line+1; pid:=(item->>'product_id')::uuid; qty:=(item->>'quantity')::integer; price:=(item->>'unit_price')::numeric;
  INSERT INTO pos.sale_lines(sale_id,line_no,product_id,barcode_snapshot,description_snapshot,quantity,unit_price,unit_cost,weight_grams,gross)
  VALUES(sid,line,pid,item->>'barcode',item->>'description',qty,price,(item->>'unit_cost')::numeric,(item->>'weight_grams')::numeric,qty*price);
  SELECT coalesce(sum(quantity_delta),0) INTO existing_qty FROM pos.stock_movements WHERE location_id=t.location_id AND product_id=pid;
  IF existing_qty<qty THEN shortage:=shortage||jsonb_build_array(jsonb_build_object('product_id',pid,'available',existing_qty,'sold',qty)); END IF;
  INSERT INTO pos.stock_movements(location_id,product_id,quantity_delta,kind,sale_id,sale_line_no,occurred_at,actor_id,reason)
  VALUES(t.location_id,pid,-qty,'sale',sid,line,happened,cashier,'Counter sale');
 END LOOP;
 FOR pay IN SELECT value FROM jsonb_array_elements(p_payload->'payments') LOOP
  INSERT INTO pos.payments(id,sale_id,method_code,amount,occurred_at,reference)
  VALUES((pay->>'id')::uuid,sid,pay->>'method',(pay->>'amount')::numeric,happened,pay->>'reference');
 END LOOP;
 FOR seller IN SELECT value FROM jsonb_array_elements(p_payload->'sellers') LOOP
  INSERT INTO pos.sale_sellers VALUES(sid,(seller#>>'{}')::uuid);
 END LOOP;
 INSERT INTO pos.sync_receipts(operation_id,terminal_id,payload,sale_id) VALUES(p_operation,t.id,p_payload,sid);
 IF shortage<>'[]'::jsonb THEN
  INSERT INTO pos.sync_issues(operation_id,code,detail) VALUES(p_operation,'STOCK_SHORTAGE',shortage);
 END IF;
 IF happened>clock_timestamp()+interval '5 minutes' THEN
  INSERT INTO pos.sync_issues(operation_id,code,detail) VALUES(p_operation,'CLOCK_AHEAD',jsonb_build_object('occurred_at',happened));
 END IF;
 RETURN sid;
END $$;
INSERT INTO pos.schema_migrations(version) VALUES(3);
COMMIT;
