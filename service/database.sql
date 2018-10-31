--
-- Name: logs; Type: TABLE; Schema: public; Owner: exante
--

CREATE TABLE blocks (
    blocknumber integer,
    "timestamp" integer
);


--
-- Name: transactions; Type: TABLE; Schema: public; Owner: exante
--

CREATE TABLE transactions (
    blocknumber integer,
    "timestamp" integer,
    hash character varying(66),
    nonce bigint,
    transactionindex integer,
    "from" character varying(130),
    "to" character varying(130),
    amount numeric(24,0),
    fee numeric(24,0),
    "type" character varying(64),
    extra jsonb
);


ALTER TABLE ONLY transactions
    ADD CONSTRAINT transactions_pkey PRIMARY KEY (hash);

--
-- Name: idx_blocknumber; Type: INDEX; Schema: public; Owner: exante
--

CREATE INDEX idx_blocknumber ON transactions USING btree (blocknumber);


--
-- Name: idx_blocknumber2; Type: INDEX; Schema: public; Owner: exante
--

CREATE INDEX idx_blocknumber2 ON transactions USING btree (blocknumber, transactionindex);

--
-- Name: idx_from; Type: INDEX; Schema: public; Owner: exante
--

CREATE INDEX idx_from ON transactions USING btree ("from");

--
-- Name: idx_to; Type: INDEX; Schema: public; Owner: exante
--

CREATE INDEX idx_to ON transactions USING btree ("to");

--
-- Name: idx_logs; Type: INDEX; Schema: public; Owner: exante
--

CREATE UNIQUE INDEX idx_blocknumber_blocks ON blocks USING btree (blocknumber);
