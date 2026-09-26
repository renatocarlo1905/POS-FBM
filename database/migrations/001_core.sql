BEGIN;
CREATE SCHEMA pos;
REVOKE CREATE ON SCHEMA public FROM PUBLIC;
CREATE TABLE pos.schema_migrations(version integer PRIMARY KEY, applied_at timestamptz NOT NULL DEFAULT now());

-- UUIDs can be generated on disconnected terminals. Amounts are exact decimals.
CREATE DOMAIN pos.amount AS numeric(18,2) CHECK (VALUE >= 0 AND VALUE <> 'NaN'::numeric);
CREATE TABLE pos.branches (
 id uuid PRIMARY KEY DEFAULT gen_random_uuid(), code text NOT NULL UNIQUE CHECK(code ~ '^[A-Z0-9_-]+$'),
 name text NOT NULL CHECK(btrim(name)<>''), timezone text NOT NULL DEFAULT 'America/Mexico_City', active boolean NOT NULL DEFAULT true
);
CREATE TABLE pos.warehouses (
 id uuid PRIMARY KEY DEFAULT gen_random_uuid(), code text NOT NULL UNIQUE, name text NOT NULL, active boolean NOT NULL DEFAULT true
);
CREATE TABLE pos.locations (
 id uuid PRIMARY KEY DEFAULT gen_random_uuid(), warehouse_id uuid NOT NULL REFERENCES pos.warehouses,
 branch_id uuid REFERENCES pos.branches, code text NOT NULL UNIQUE, name text NOT NULL,
 active boolean NOT NULL DEFAULT true, UNIQUE(id,branch_id)
);
CREATE TABLE pos.terminals (
 id uuid PRIMARY KEY DEFAULT gen_random_uuid(), branch_id uuid NOT NULL REFERENCES pos.branches,
 location_id uuid NOT NULL UNIQUE, code text NOT NULL UNIQUE CHECK(code ~ '^[A-Z0-9_-]+$'),
 active boolean NOT NULL DEFAULT true,
 FOREIGN KEY(location_id,branch_id) REFERENCES pos.locations(id,branch_id),
 UNIQUE(id,branch_id)
);
COMMENT ON COLUMN pos.terminals.location_id IS 'V1: one terminal owns a selling location; prevents two disconnected terminals sharing its allocation. Multiple terminals require a later allocation protocol.';
CREATE TABLE pos.staff (
 id uuid PRIMARY KEY DEFAULT gen_random_uuid(), code text NOT NULL UNIQUE, display_name text NOT NULL,
 active boolean NOT NULL DEFAULT true
);
COMMENT ON TABLE pos.staff IS 'Business staff, not authentication credentials. Identity, permissions and authorization will be added with backend.';
CREATE TABLE pos.categories (
 id uuid PRIMARY KEY DEFAULT gen_random_uuid(), parent_id uuid REFERENCES pos.categories,
 name text NOT NULL, CHECK(parent_id IS DISTINCT FROM id)
);
CREATE TABLE pos.products (
 id uuid PRIMARY KEY DEFAULT gen_random_uuid(), barcode text NOT NULL UNIQUE CHECK(btrim(barcode)<>''),
 short_description text NOT NULL, description text, category_id uuid REFERENCES pos.categories,
 material text, purity numeric(8,6) CHECK(purity > 0 AND purity <= 1),
 weight_grams numeric(12,3) CHECK(weight_grams >= 0 AND weight_grams <> 'NaN'::numeric),
 reference_price pos.amount NOT NULL, reference_cost pos.amount,
 active boolean NOT NULL DEFAULT true, created_at timestamptz NOT NULL DEFAULT now()
);
CREATE TABLE pos.cash_sessions (
 id uuid PRIMARY KEY, terminal_id uuid NOT NULL REFERENCES pos.terminals, opened_by uuid NOT NULL REFERENCES pos.staff,
 opened_at timestamptz NOT NULL, received_at timestamptz NOT NULL DEFAULT clock_timestamp(),
 opening_cash pos.amount NOT NULL, closed_at timestamptz, closed_by uuid REFERENCES pos.staff,
 counted_cash pos.amount, UNIQUE(id,terminal_id),
 CHECK ((closed_at IS NULL AND closed_by IS NULL AND counted_cash IS NULL) OR
        (closed_at >= opened_at AND closed_by IS NOT NULL AND counted_cash IS NOT NULL))
);
CREATE INDEX cash_sessions_terminal_time ON pos.cash_sessions(terminal_id,opened_at);
-- No partial unique index on "open" sessions: a disconnected terminal can upload
-- several historical sessions whose closures have not reached the server yet.
CREATE TABLE pos.payment_methods (
 code text PRIMARY KEY, name text NOT NULL, active boolean NOT NULL DEFAULT true
);
CREATE TABLE pos.sales (
 id uuid PRIMARY KEY, terminal_id uuid NOT NULL, branch_id uuid NOT NULL,
 cash_session_id uuid NOT NULL, cashier_id uuid NOT NULL REFERENCES pos.staff,
 local_sequence bigint NOT NULL CHECK(local_sequence>0),
 occurred_at timestamptz NOT NULL, received_at timestamptz NOT NULL DEFAULT clock_timestamp(),
 business_timezone text NOT NULL, clock_source text NOT NULL CHECK(clock_source IN ('terminal','server')),
 captured_offline boolean NOT NULL, currency text NOT NULL DEFAULT 'MXN' CHECK(currency='MXN'),
 subtotal pos.amount NOT NULL, discount pos.amount NOT NULL, total pos.amount NOT NULL,
 FOREIGN KEY(terminal_id,branch_id) REFERENCES pos.terminals(id,branch_id),
 FOREIGN KEY(cash_session_id,terminal_id) REFERENCES pos.cash_sessions(id,terminal_id),
 UNIQUE(terminal_id,local_sequence), CHECK(total=subtotal-discount AND total>0)
);
CREATE INDEX sales_branch_time ON pos.sales(branch_id,occurred_at);
CREATE INDEX sales_received_time ON pos.sales(received_at);
CREATE TABLE pos.sale_lines (
 sale_id uuid NOT NULL REFERENCES pos.sales, line_no integer NOT NULL CHECK(line_no>0),
 product_id uuid NOT NULL REFERENCES pos.products, barcode_snapshot text NOT NULL,
 description_snapshot text NOT NULL, quantity integer NOT NULL CHECK(quantity>0),
 unit_price pos.amount NOT NULL, unit_cost pos.amount, weight_grams numeric(12,3) CHECK(weight_grams>=0 AND weight_grams<>'NaN'::numeric),
 gross pos.amount NOT NULL, PRIMARY KEY(sale_id,line_no), CHECK(gross=quantity*unit_price)
);
CREATE INDEX sale_lines_product ON pos.sale_lines(product_id);
CREATE TABLE pos.payments (
 id uuid PRIMARY KEY, sale_id uuid NOT NULL REFERENCES pos.sales, method_code text NOT NULL REFERENCES pos.payment_methods,
 amount pos.amount NOT NULL CHECK(amount>0), occurred_at timestamptz NOT NULL,
 reference text, CHECK(reference IS NULL OR length(reference)<=200)
);
COMMENT ON TABLE pos.payments IS 'Amounts applied to the sale, net of change. Do not store full card numbers or security codes. Layaway/repair payment links are intentionally not specified yet.';
CREATE INDEX payments_sale ON pos.payments(sale_id);
CREATE TABLE pos.sale_sellers (
 sale_id uuid NOT NULL REFERENCES pos.sales, staff_id uuid NOT NULL REFERENCES pos.staff,
 PRIMARY KEY(sale_id,staff_id)
);
COMMENT ON TABLE pos.sale_sellers IS 'Participants only. Commission formulas and allocation are pending specification.';

-- Immutable movement ledger. Balances are derived, never uploaded as replacements.
CREATE TABLE pos.stock_movements (
 id uuid PRIMARY KEY DEFAULT gen_random_uuid(), location_id uuid NOT NULL REFERENCES pos.locations,
 product_id uuid NOT NULL REFERENCES pos.products, quantity_delta integer NOT NULL CHECK(quantity_delta<>0),
 kind text NOT NULL CHECK(kind IN ('opening','sale','adjustment','transfer_in','transfer_out')),
 sale_id uuid, sale_line_no integer, occurred_at timestamptz NOT NULL,
 received_at timestamptz NOT NULL DEFAULT clock_timestamp(), actor_id uuid NOT NULL REFERENCES pos.staff,
 reason text NOT NULL CHECK(btrim(reason)<>''), transfer_id uuid,
 FOREIGN KEY(sale_id,sale_line_no) REFERENCES pos.sale_lines(sale_id,line_no),
 UNIQUE(sale_id,sale_line_no),
 CHECK((kind='sale' AND sale_id IS NOT NULL AND sale_line_no IS NOT NULL AND quantity_delta<0)
    OR (kind<>'sale' AND sale_id IS NULL AND sale_line_no IS NULL)),
 CHECK((kind IN ('transfer_in','transfer_out'))=(transfer_id IS NOT NULL)),
 CHECK(kind<>'opening' OR quantity_delta>0)
);
CREATE INDEX stock_location_product ON pos.stock_movements(location_id,product_id);
CREATE VIEW pos.stock_balances AS
 SELECT location_id,product_id,sum(quantity_delta)::bigint quantity
 FROM pos.stock_movements GROUP BY location_id,product_id;
CREATE VIEW pos.warehouse_balances AS
 SELECT l.warehouse_id,b.product_id,sum(b.quantity) quantity
 FROM pos.stock_balances b JOIN pos.locations l ON l.id=b.location_id
 GROUP BY l.warehouse_id,b.product_id;

CREATE TABLE pos.sync_receipts (
 operation_id uuid PRIMARY KEY, terminal_id uuid NOT NULL REFERENCES pos.terminals,
 payload jsonb NOT NULL CHECK(jsonb_typeof(payload)='object'), sale_id uuid NOT NULL UNIQUE REFERENCES pos.sales,
 received_at timestamptz NOT NULL DEFAULT clock_timestamp(), UNIQUE(terminal_id,operation_id)
);
CREATE TABLE pos.sync_issues (
 id uuid PRIMARY KEY DEFAULT gen_random_uuid(), operation_id uuid NOT NULL REFERENCES pos.sync_receipts,
 code text NOT NULL, detail jsonb NOT NULL, created_at timestamptz NOT NULL DEFAULT clock_timestamp(),
 resolved_at timestamptz, resolution text, CHECK((resolved_at IS NULL)=(resolution IS NULL))
);
CREATE TABLE pos.legacy_mappings (
 source_system text NOT NULL, source_table text NOT NULL, source_id text NOT NULL,
 target_entity text NOT NULL, target_id uuid NOT NULL, notes text,
 PRIMARY KEY(source_system,source_table,source_id,target_entity)
);
COMMENT ON TABLE pos.legacy_mappings IS 'Traceability only; target UUID must be checked by migration tooling. Old unknown times must not be fabricated as precise new sales.';

CREATE FUNCTION pos.immutable_record() RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN RAISE EXCEPTION 'Historical records are immutable; use a compensating operation'; END $$;
DO $$ DECLARE n text; BEGIN
 FOREACH n IN ARRAY ARRAY['sales','sale_lines','payments','sale_sellers','stock_movements','sync_receipts'] LOOP
  EXECUTE format('CREATE TRIGGER immutable BEFORE UPDATE OR DELETE ON pos.%I FOR EACH ROW EXECUTE FUNCTION pos.immutable_record()',n);
 END LOOP;
END $$;

-- A v1 counter sale import. All writes succeed or roll back together.
-- SECURITY DEFINER is exposed only to a trusted backend role, not to browser clients.
CREATE FUNCTION pos.receive_sale(p_operation uuid, p_terminal uuid, p_payload jsonb)
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
COMMENT ON FUNCTION pos.receive_sale(uuid,uuid,jsonb) IS 'Receives already completed sales, not a checkout authorization. Preserves collected sales with shortages and flags reconciliation. Backend must authenticate terminal and enforce approved pricing/discount policy; local durable queue and allocation protocol are not implemented here.';

REVOKE ALL ON ALL TABLES IN SCHEMA pos FROM PUBLIC;
REVOKE ALL ON ALL FUNCTIONS IN SCHEMA pos FROM PUBLIC;
INSERT INTO pos.schema_migrations(version) VALUES(1);
COMMIT;
