--
-- PostgreSQL database dump
--

-- Dumped from database version 14.4
-- Dumped by pg_dump version 14.4

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
-- Name: dish; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.dish (
    id integer NOT NULL,
    date_created timestamp with time zone,
    date_updated timestamp with time zone,
    name character varying(255) NOT NULL,
    description text,
    price numeric(10,2),
    preparation_time integer,
    is_vegan boolean NOT NULL
);


ALTER TABLE public.dish OWNER TO postgres;

--
-- Name: dish_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.dish_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.dish_id_seq OWNER TO postgres;

--
-- Name: dish_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.dish_id_seq OWNED BY public.dish.id;


--
-- Name: menu_card; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.menu_card (
    id integer NOT NULL,
    date_created timestamp with time zone,
    date_updated timestamp with time zone,
    name character varying(255) NOT NULL,
    description text
);


ALTER TABLE public.menu_card OWNER TO postgres;

--
-- Name: menu_card_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.menu_card_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.menu_card_id_seq OWNER TO postgres;

--
-- Name: menu_card_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.menu_card_id_seq OWNED BY public.menu_card.id;


--
-- Name: menu_dish_junction; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.menu_dish_junction (
    menu_card_id integer NOT NULL,
    dish_id integer NOT NULL
);


ALTER TABLE public.menu_dish_junction OWNER TO postgres;

--
-- Name: user; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."user" (
    id integer NOT NULL,
    date_created timestamp with time zone,
    date_updated timestamp with time zone,
    email character varying NOT NULL,
    password character varying NOT NULL
);


ALTER TABLE public."user" OWNER TO postgres;

--
-- Name: user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.user_id_seq OWNER TO postgres;

--
-- Name: user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.user_id_seq OWNED BY public."user".id;


--
-- Name: dish id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dish ALTER COLUMN id SET DEFAULT nextval('public.dish_id_seq'::regclass);


--
-- Name: menu_card id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.menu_card ALTER COLUMN id SET DEFAULT nextval('public.menu_card_id_seq'::regclass);


--
-- Name: user id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."user" ALTER COLUMN id SET DEFAULT nextval('public.user_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.alembic_version (version_num) FROM stdin;
11120bc2540a
\.


--
-- Data for Name: dish; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.dish (id, date_created, date_updated, name, description, price, preparation_time, is_vegan) FROM stdin;
1	2022-08-01 08:54:41.362732+00	2022-08-01 12:28:36.150497+00	Scrambled eggs	Fresh from local farm with onion.	5.00	5	f
2	2022-08-01 10:03:38.094122+00	2022-08-01 12:36:19.094799+00	Smoothie	Mixed Berry or Strawberry-banana	5.00	3	t
3	2022-08-01 12:37:06.863352+00	\N	Oatmeal	Served with brown sugar, raisins, and choice of steamed milk. Choice of blueberries and/or banana.	8.00	8	t
4	2022-08-01 12:37:45.795626+00	\N	Avocado Toast	Toy box tomatoes, sunflower seeds, pickled onions.	6.00	6	t
5	2022-08-01 12:38:36.19606+00	\N	Steak & Eggs	5oz. Angus Tenderloin served with two eggs and breakfast potatoes.	10.00	12	f
6	2022-08-01 12:38:56.549666+00	\N	Smoked Salmon Plate	Tomato, cream cheese, capers, and choice of bagel.	12.00	12	f
7	2022-08-01 12:43:37.199601+00	\N	Bacon Omelet	Bacon, heirloom tomatoes, mixed mushrooms and white cheddar cheese.	14.00	15	f
8	2022-08-01 12:44:18.93881+00	\N	Buttermilk Pancake	Choice of buttermilk, blueberry, chocolate chip or banana. Maple syrup.	10.00	13	f
9	2022-08-01 12:45:19.437427+00	\N	Burrito	Breakfast Burritos are the ultimate morning meal on the go.	10.00	10	t
10	2022-08-01 12:46:31.719006+00	2022-08-01 12:48:03.212667+00	Fish Tacos	Grilled or fried white fish, chipotle sauce, fresh pico de gallo, cheese, corn tortillas and homemade salsa. Served with shoe string fries	20.00	20	f
12	2022-08-01 12:49:34.888184+00	\N	Meatloaf Sandwich	Thick slice of house-made meatloaf topped with BBQ sauce, cheddar cheese, garlic aioli, lettuce, red onions, tomatoes on grilled Parmesan sourdough	15.00	23	f
13	2022-08-01 12:50:05.532483+00	\N	Shrimp Fresca Pasta.	Grilled shrimp, diced tomatoes and spinach served over pasta in a light lemon butter sauce	35.00	25	f
14	2022-08-01 12:51:31.694666+00	\N	Fried Ice Cream	Hot and cold.	13.00	5	t
15	2022-08-01 12:52:01.649829+00	\N	Chocolate Mousse	Sweet and sour	11.00	5	t
16	2022-08-01 12:52:54.454717+00	\N	Quesadilla	Two crispy flour tortillas stuffed with cheddar and jack cheese, green onions and tomatoes. Served with sour cream and guacamole. 	33.00	15	f
17	2022-08-01 12:53:36.336234+00	\N	Mexican Pizza	Crisp flour tortilla topped with choice of refried or Rancho beans (whole), and choice of ground beef, chicken or picadillo. Topped with jack and cheddar cheese, tomatoes and green onions. Garnished with sour cream and guacamole.	14.00	20	f
18	2022-08-01 12:54:16.427131+00	\N	Appetizer Guacamole	Azteca's fresh guacamole with chips.	12.00	15	t
11	2022-08-01 12:49:00.088339+00	\N	Chicken Tenders	Hand-breaded tenders served with smoky mesquite sweet BBQ sauce and shoe string fries	25.00	22	f
19	2022-08-01 12:57:07.216615+00	\N	Tea with rum	Tea with rum	6.00	2	t
20	2022-08-01 12:57:54.547003+00	\N	Cafe latte	With oat milk	6.00	2	t
21	2022-08-01 12:58:24.934534+00	\N	Cappuccino	With oat or cow milk	6.00	2	t
22	2022-08-01 12:58:44.021625+00	\N	Orange juice	Fresh not from concentrate	6.00	2	t
23	2022-08-01 12:59:04.222213+00	\N	Red wine	Spanish red	6.00	2	t
24	2022-08-01 12:59:17.505347+00	\N	Beer	Draft beer	6.00	2	t
25	2022-08-01 13:00:22.459795+00	\N	Croissant	With or without chocolate	6.00	2	t
26	2022-08-01 13:01:28.014843+00	\N	Mushroom dumplings	10 pieces.	12.00	10	t
27	2022-08-01 13:01:50.806209+00	\N	Cheese dumplings	10 pieces.	14.00	10	f
28	2022-08-01 13:02:27.927092+00	\N	Cod soup	With potatoes and garlic bread.	14.00	8	f
\.


--
-- Data for Name: menu_card; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.menu_card (id, date_created, date_updated, name, description) FROM stdin;
1	2022-08-01 08:54:25.726112+00	2022-08-01 12:04:31.074631+00	Breakfast	Every day from 7 to 10
2	2022-08-01 09:56:49.592094+00	2022-08-01 12:05:36.201908+00	Lunch	Mon-Fri from 11 to 13
3	2022-08-01 12:07:26.409409+00	\N	Dinner	Weekends from 12 to 22
4	2022-08-01 12:08:04.339211+00	\N	Supper	Mon-Fri from 18-20
5	2022-08-01 13:15:48.147347+00	\N	Empty card	Empty menu just for tests.
\.


--
-- Data for Name: menu_dish_junction; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.menu_dish_junction (menu_card_id, dish_id) FROM stdin;
1	1
2	1
2	2
1	2
1	3
1	4
1	5
1	6
1	7
1	8
1	9
1	20
1	21
1	22
1	25
2	12
2	13
2	14
2	15
2	16
2	17
2	18
2	19
2	20
2	21
2	24
2	28
3	27
3	26
3	24
3	23
3	22
3	17
3	10
4	26
4	27
4	25
4	24
4	23
4	22
4	17
4	4
4	2
4	6
\.


--
-- Data for Name: user; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."user" (id, date_created, date_updated, email, password) FROM stdin;
\.


--
-- Name: dish_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.dish_id_seq', 28, true);


--
-- Name: menu_card_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.menu_card_id_seq', 5, true);


--
-- Name: user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.user_id_seq', 1, false);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: dish dish_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dish
    ADD CONSTRAINT dish_pkey PRIMARY KEY (id);


--
-- Name: menu_card menu_card_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.menu_card
    ADD CONSTRAINT menu_card_name_key UNIQUE (name);


--
-- Name: menu_card menu_card_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.menu_card
    ADD CONSTRAINT menu_card_pkey PRIMARY KEY (id);


--
-- Name: menu_dish_junction menu_dish_junction_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.menu_dish_junction
    ADD CONSTRAINT menu_dish_junction_pkey PRIMARY KEY (menu_card_id, dish_id);


--
-- Name: user user_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (id);


--
-- Name: ix_dish_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_dish_id ON public.dish USING btree (id);


--
-- Name: ix_menu_card_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_menu_card_id ON public.menu_card USING btree (id);


--
-- Name: ix_user_email; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_user_email ON public."user" USING btree (email);


--
-- Name: ix_user_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_user_id ON public."user" USING btree (id);


--
-- Name: menu_dish_junction menu_dish_junction_dish_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.menu_dish_junction
    ADD CONSTRAINT menu_dish_junction_dish_id_fkey FOREIGN KEY (dish_id) REFERENCES public.dish(id);


--
-- Name: menu_dish_junction menu_dish_junction_menu_card_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.menu_dish_junction
    ADD CONSTRAINT menu_dish_junction_menu_card_id_fkey FOREIGN KEY (menu_card_id) REFERENCES public.menu_card(id);


--
-- PostgreSQL database dump complete
--

