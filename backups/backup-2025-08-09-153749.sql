--
-- PostgreSQL database dump
--

-- Dumped from database version 15.13
-- Dumped by pg_dump version 15.13

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: public; Type: SCHEMA; Schema: -; Owner: postgres
--

-- *not* creating schema, since initdb creates it


ALTER SCHEMA public OWNER TO postgres;

--
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON SCHEMA public IS '';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO postgres;

--
-- Name: content; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.content (
    id integer NOT NULL,
    influenceuse_id integer NOT NULL,
    title character varying(255),
    description text,
    content_type character varying(5) NOT NULL,
    status character varying(9) DEFAULT 'draft'::character varying NOT NULL,
    file_url character varying(500),
    file_size integer,
    file_format character varying(50),
    thumbnail_url character varying(500),
    prompt text,
    ai_model character varying(100),
    generation_params json,
    generation_time integer,
    categories json DEFAULT '[]'::json,
    tags json DEFAULT '[]'::json,
    width integer,
    height integer,
    duration integer,
    is_public boolean DEFAULT false NOT NULL,
    is_featured boolean DEFAULT false NOT NULL,
    published_at timestamp with time zone,
    views_count integer DEFAULT 0 NOT NULL,
    likes_count integer DEFAULT 0 NOT NULL,
    shares_count integer DEFAULT 0 NOT NULL,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone
);


ALTER TABLE public.content OWNER TO postgres;

--
-- Name: content_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.content_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.content_id_seq OWNER TO postgres;

--
-- Name: content_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.content_id_seq OWNED BY public.content.id;


--
-- Name: conversations; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.conversations (
    id integer NOT NULL,
    user_id integer NOT NULL,
    influenceuse_id integer NOT NULL,
    platform character varying(100),
    platform_conversation_id character varying(255),
    status character varying(8) DEFAULT 'active'::character varying NOT NULL,
    chatbot_enabled boolean DEFAULT true NOT NULL,
    auto_reply_enabled boolean DEFAULT true NOT NULL,
    ollama_model character varying(100) DEFAULT 'llama2:7b'::character varying NOT NULL,
    conversation_history json DEFAULT '[]'::json,
    last_message_at timestamp with time zone,
    message_count integer DEFAULT 0 NOT NULL,
    response_time_avg integer,
    satisfaction_score integer,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone
);


ALTER TABLE public.conversations OWNER TO postgres;

--
-- Name: conversations_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.conversations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.conversations_id_seq OWNER TO postgres;

--
-- Name: conversations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.conversations_id_seq OWNED BY public.conversations.id;


--
-- Name: influenceuses; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.influenceuses (
    id integer NOT NULL,
    user_id integer NOT NULL,
    stage_name character varying(255) NOT NULL,
    bio text,
    avatar_url character varying(500),
    cover_image_url character varying(500),
    followers_count integer DEFAULT 0 NOT NULL,
    following_count integer DEFAULT 0 NOT NULL,
    posts_count integer DEFAULT 0 NOT NULL,
    content_categories json DEFAULT '[]'::json NOT NULL,
    content_style character varying(100),
    subscription_price double precision DEFAULT '0'::double precision NOT NULL,
    tips_enabled boolean DEFAULT true NOT NULL,
    custom_content_enabled boolean DEFAULT true NOT NULL,
    is_active boolean DEFAULT true NOT NULL,
    is_verified boolean DEFAULT false NOT NULL,
    is_featured boolean DEFAULT false NOT NULL,
    auto_posting_enabled boolean DEFAULT true NOT NULL,
    chatbot_enabled boolean DEFAULT true NOT NULL,
    analytics_enabled boolean DEFAULT true NOT NULL,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone,
    last_activity timestamp with time zone
);


ALTER TABLE public.influenceuses OWNER TO postgres;

--
-- Name: influenceuses_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.influenceuses_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.influenceuses_id_seq OWNER TO postgres;

--
-- Name: influenceuses_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.influenceuses_id_seq OWNED BY public.influenceuses.id;


--
-- Name: messages; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.messages (
    id integer NOT NULL,
    conversation_id integer NOT NULL,
    content text NOT NULL,
    message_type character varying(50),
    sender_type character varying(50),
    platform_message_id character varying(255),
    platform_timestamp timestamp with time zone,
    is_ai_generated boolean DEFAULT false NOT NULL,
    ai_model character varying(100),
    ai_confidence integer,
    metadata_json json,
    created_at timestamp with time zone DEFAULT now()
);


ALTER TABLE public.messages OWNER TO postgres;

--
-- Name: messages_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.messages_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.messages_id_seq OWNER TO postgres;

--
-- Name: messages_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.messages_id_seq OWNED BY public.messages.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id integer NOT NULL,
    email character varying(255) NOT NULL,
    username character varying(100) NOT NULL,
    hashed_password character varying(255) NOT NULL,
    full_name character varying(255),
    role character varying(12) DEFAULT 'influenceuse'::character varying NOT NULL,
    is_active boolean DEFAULT true NOT NULL,
    is_verified boolean DEFAULT false NOT NULL,
    avatar_url character varying(500),
    bio text,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone,
    last_login timestamp with time zone
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_id_seq OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: content id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.content ALTER COLUMN id SET DEFAULT nextval('public.content_id_seq'::regclass);


--
-- Name: conversations id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.conversations ALTER COLUMN id SET DEFAULT nextval('public.conversations_id_seq'::regclass);


--
-- Name: influenceuses id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.influenceuses ALTER COLUMN id SET DEFAULT nextval('public.influenceuses_id_seq'::regclass);


--
-- Name: messages id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.messages ALTER COLUMN id SET DEFAULT nextval('public.messages_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.alembic_version (version_num) FROM stdin;
1d41cdb5499e
\.


--
-- Data for Name: content; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.content (id, influenceuse_id, title, description, content_type, status, file_url, file_size, file_format, thumbnail_url, prompt, ai_model, generation_params, generation_time, categories, tags, width, height, duration, is_public, is_featured, published_at, views_count, likes_count, shares_count, created_at, updated_at) FROM stdin;
1	1	Bienvenue	Contenu de démo	text	published	\N	\N	\N	\N	\N	\N	\N	\N	[]	[]	\N	\N	\N	t	f	\N	0	0	0	2025-08-09 13:50:17.56914+00	\N
\.


--
-- Data for Name: conversations; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.conversations (id, user_id, influenceuse_id, platform, platform_conversation_id, status, chatbot_enabled, auto_reply_enabled, ollama_model, conversation_history, last_message_at, message_count, response_time_avg, satisfaction_score, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: influenceuses; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.influenceuses (id, user_id, stage_name, bio, avatar_url, cover_image_url, followers_count, following_count, posts_count, content_categories, content_style, subscription_price, tips_enabled, custom_content_enabled, is_active, is_verified, is_featured, auto_posting_enabled, chatbot_enabled, analytics_enabled, created_at, updated_at, last_activity) FROM stdin;
1	1	Demo Influenceuse	Profil démo	\N	\N	1000	0	1	[]	\N	0	t	t	t	f	f	t	t	t	2025-08-09 13:50:17.56914+00	\N	\N
\.


--
-- Data for Name: messages; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.messages (id, conversation_id, content, message_type, sender_type, platform_message_id, platform_timestamp, is_ai_generated, ai_model, ai_confidence, metadata_json, created_at) FROM stdin;
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, email, username, hashed_password, full_name, role, is_active, is_verified, avatar_url, bio, created_at, updated_at, last_login) FROM stdin;
1	admin@influenceur-ia.com	admin	$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj3bp.gS.6.m	\N	admin	t	t	\N	\N	2025-08-09 13:50:17.56914+00	\N	\N
2	dev@example.com	devuser	$2b$12$yWcWmJhFKkC99EIv.l8mqOMj3Bvwn0Vxi25QzQwXn6r2UXrM7mF9W	Dev User	INFLUENCEUSE	t	f	\N	\N	2025-08-09 15:07:20.674498+00	\N	\N
\.


--
-- Name: content_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.content_id_seq', 1, true);


--
-- Name: conversations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.conversations_id_seq', 1, false);


--
-- Name: influenceuses_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.influenceuses_id_seq', 1, true);


--
-- Name: messages_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.messages_id_seq', 1, false);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 2, true);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: content content_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.content
    ADD CONSTRAINT content_pkey PRIMARY KEY (id);


--
-- Name: conversations conversations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.conversations
    ADD CONSTRAINT conversations_pkey PRIMARY KEY (id);


--
-- Name: influenceuses influenceuses_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.influenceuses
    ADD CONSTRAINT influenceuses_pkey PRIMARY KEY (id);


--
-- Name: messages messages_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.messages
    ADD CONSTRAINT messages_pkey PRIMARY KEY (id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: ix_messages_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_messages_id ON public.messages USING btree (id);


--
-- Name: ix_users_email; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_users_email ON public.users USING btree (email);


--
-- Name: ix_users_username; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_users_username ON public.users USING btree (username);


--
-- Name: content content_influenceuse_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.content
    ADD CONSTRAINT content_influenceuse_id_fkey FOREIGN KEY (influenceuse_id) REFERENCES public.influenceuses(id) ON DELETE CASCADE;


--
-- Name: conversations conversations_influenceuse_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.conversations
    ADD CONSTRAINT conversations_influenceuse_id_fkey FOREIGN KEY (influenceuse_id) REFERENCES public.influenceuses(id) ON DELETE CASCADE;


--
-- Name: conversations conversations_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.conversations
    ADD CONSTRAINT conversations_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: influenceuses influenceuses_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.influenceuses
    ADD CONSTRAINT influenceuses_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: messages messages_conversation_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.messages
    ADD CONSTRAINT messages_conversation_id_fkey FOREIGN KEY (conversation_id) REFERENCES public.conversations(id) ON DELETE CASCADE;


--
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE USAGE ON SCHEMA public FROM PUBLIC;


--
-- PostgreSQL database dump complete
--

