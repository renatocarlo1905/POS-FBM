--
-- PostgreSQL database dump
--

\restrict qdlwZs36BLyeWIlpGK0BqKTupz93pdqR262zywMnUNOjKgnEe0MOdqbW9B2ssSt

-- Dumped from database version 18.6 (Debian 18.6-1.pgdg13+2)
-- Dumped by pg_dump version 18.6 (Debian 18.6-1.pgdg13+2)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: prevent_fact_change(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.prevent_fact_change() RETURNS trigger
    LANGUAGE plpgsql
    AS $$ BEGIN RAISE EXCEPTION 'Immutable fact: append a correction instead'; END $$;


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: audit; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.audit (
    id bigint NOT NULL,
    at text,
    actor text,
    action text,
    detail text
);


--
-- Name: audit_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.audit ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.audit_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: corrections; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.corrections (
    id text NOT NULL,
    target text NOT NULL,
    kind text NOT NULL,
    before_data text NOT NULL,
    after_data text NOT NULL,
    reason text NOT NULL,
    operator text NOT NULL,
    authorizer text NOT NULL,
    at text NOT NULL,
    origin integer NOT NULL,
    request_hash text NOT NULL,
    document text NOT NULL,
    ordinal bigint NOT NULL
);


--
-- Name: corrections_ordinal_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.corrections ALTER COLUMN ordinal ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.corrections_ordinal_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: events; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.events (
    id text NOT NULL,
    branch integer,
    seq bigint,
    body text NOT NULL,
    hash text NOT NULL,
    status text,
    issue text,
    received text,
    ordinal bigint NOT NULL,
    CONSTRAINT events_branch_check CHECK ((branch = ANY (ARRAY[1, 2]))),
    CONSTRAINT events_seq_check CHECK ((seq > 0)),
    CONSTRAINT events_status_check CHECK ((status = ANY (ARRAY['accepted'::text, 'rejected'::text])))
);


--
-- Name: events_ordinal_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.events ALTER COLUMN ordinal ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.events_ordinal_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: inventory_entries; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.inventory_entries (
    id text NOT NULL,
    request_hash text NOT NULL,
    at text NOT NULL,
    actor text NOT NULL,
    data text NOT NULL
);


--
-- Name: kv; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.kv (
    k text NOT NULL,
    v text NOT NULL
);


--
-- Name: products; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.products (
    id text NOT NULL,
    code text NOT NULL,
    data text NOT NULL
);


--
-- Name: related_changes; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.related_changes (
    sale text NOT NULL,
    related text NOT NULL
);


--
-- Name: stock; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.stock (
    id text NOT NULL,
    available integer
);


--
-- Name: stock_ledger; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.stock_ledger (
    id text NOT NULL,
    product text NOT NULL,
    warehouse text NOT NULL,
    delta integer NOT NULL,
    at text NOT NULL,
    origin text NOT NULL,
    reason text NOT NULL
);


--
-- Name: warehouse_stock; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.warehouse_stock (
    product text NOT NULL,
    warehouse text NOT NULL,
    quantity integer NOT NULL
);


--
-- Name: audit audit_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.audit
    ADD CONSTRAINT audit_pkey PRIMARY KEY (id);


--
-- Name: corrections corrections_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.corrections
    ADD CONSTRAINT corrections_pkey PRIMARY KEY (id);


--
-- Name: events events_branch_seq_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.events
    ADD CONSTRAINT events_branch_seq_key UNIQUE (branch, seq);


--
-- Name: events events_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.events
    ADD CONSTRAINT events_pkey PRIMARY KEY (id);


--
-- Name: inventory_entries inventory_entries_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.inventory_entries
    ADD CONSTRAINT inventory_entries_pkey PRIMARY KEY (id);


--
-- Name: kv kv_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kv
    ADD CONSTRAINT kv_pkey PRIMARY KEY (k);


--
-- Name: products products_code_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_code_key UNIQUE (code);


--
-- Name: products products_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_pkey PRIMARY KEY (id);


--
-- Name: related_changes related_changes_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.related_changes
    ADD CONSTRAINT related_changes_pkey PRIMARY KEY (sale, related);


--
-- Name: stock_ledger stock_ledger_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.stock_ledger
    ADD CONSTRAINT stock_ledger_pkey PRIMARY KEY (id);


--
-- Name: stock stock_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.stock
    ADD CONSTRAINT stock_pkey PRIMARY KEY (id);


--
-- Name: warehouse_stock warehouse_stock_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.warehouse_stock
    ADD CONSTRAINT warehouse_stock_pkey PRIMARY KEY (product, warehouse);


--
-- Name: corrections immutable_corrections; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER immutable_corrections BEFORE DELETE OR UPDATE ON public.corrections FOR EACH ROW EXECUTE FUNCTION public.prevent_fact_change();


--
-- Name: events immutable_events; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER immutable_events BEFORE DELETE OR UPDATE ON public.events FOR EACH ROW EXECUTE FUNCTION public.prevent_fact_change();


--
-- Name: stock_ledger immutable_stock_ledger; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER immutable_stock_ledger BEFORE DELETE OR UPDATE ON public.stock_ledger FOR EACH ROW EXECUTE FUNCTION public.prevent_fact_change();


--
-- Name: warehouse_stock warehouse_stock_product_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.warehouse_stock
    ADD CONSTRAINT warehouse_stock_product_fkey FOREIGN KEY (product) REFERENCES public.products(id);


--
-- PostgreSQL database dump complete
--

\unrestrict qdlwZs36BLyeWIlpGK0BqKTupz93pdqR262zywMnUNOjKgnEe0MOdqbW9B2ssSt


-- Historial sintético E1: separado de los eventos operativos y de sus secuencias.
CREATE TABLE IF NOT EXISTS public.simulated_sales (
    id text PRIMARY KEY,
    batch text NOT NULL,
    body text NOT NULL
);

-- Turnos históricos simulados, sin efectos sobre las cajas operativas.
CREATE TABLE IF NOT EXISTS public.simulated_shifts (
    id text PRIMARY KEY,
    body text NOT NULL
);
