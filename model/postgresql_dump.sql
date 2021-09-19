--
-- PostgreSQL database dump
--

-- Dumped from database version 13.3
-- Dumped by pg_dump version 13.3

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
-- Name: body; Type: TABLE; Schema: public; Owner: hiraki
--

CREATE TABLE public.body (
    name character varying(20) NOT NULL,
    height integer,
    breast integer,
    waist integer,
    hip integer,
    school text,
    year integer
);


ALTER TABLE public.body OWNER TO hiraki;

--
-- Name: events; Type: TABLE; Schema: public; Owner: hiraki
--

CREATE TABLE public.events (
    day integer NOT NULL,
    month integer NOT NULL,
    type text NOT NULL,
    details text NOT NULL,
    short_note text,
    note text,
    notified boolean
);


ALTER TABLE public.events OWNER TO hiraki;

--
-- Name: settings; Type: TABLE; Schema: public; Owner: hiraki
--

CREATE TABLE public.settings (
    field text NOT NULL,
    value json
);


ALTER TABLE public.settings OWNER TO hiraki;

--
-- Name: systemlog; Type: TABLE; Schema: public; Owner: hiraki
--

CREATE TABLE public.systemlog (
    id integer NOT NULL,
    "time" timestamp without time zone,
    content text
);


ALTER TABLE public.systemlog OWNER TO hiraki;

--
-- Name: systemlog_id_seq; Type: SEQUENCE; Schema: public; Owner: hiraki
--

CREATE SEQUENCE public.systemlog_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.systemlog_id_seq OWNER TO hiraki;

--
-- Name: systemlog_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hiraki
--

ALTER SEQUENCE public.systemlog_id_seq OWNED BY public.systemlog.id;


--
-- Name: systemlog id; Type: DEFAULT; Schema: public; Owner: hiraki
--

ALTER TABLE ONLY public.systemlog ALTER COLUMN id SET DEFAULT nextval('public.systemlog_id_seq'::regclass);


--
-- Data for Name: body; Type: TABLE DATA; Schema: public; Owner: hiraki
--

COPY public.body (name, height, breast, waist, hip, school, year) FROM stdin;
Honoka_Kosaka	157	78	58	82	Otonokizaka	2
Umi_Sonoda	159	76	58	80	Otonokizaka	2
Kotori_Minami	159	80	58	80	Otonokizaka	2
Hanayo_Koizumi	156	82	60	83	Otonokizaka	1
Rin_Hoshizora	155	75	59	80	Otonokizaka	1
Maki_Nishikino	161	78	56	83	Otonokizaka	1
Eli_Ayase	162	88	60	84	Otonokizaka	3
Nozomi_Tojo	159	90	60	82	Otonokizaka	3
Chika_Takami	157	82	59	83	Uranohoshi	2
Riko_Sakurauchi	160	80	58	82	Uranohoshi	2
You_Watanabe	157	82	57	81	Uranohoshi	2
Ruby_Kurosawa	154	76	56	79	Uranohoshi	1
Yoshiko_Tsushima	156	79	58	80	Uranohoshi	1
Hanamaru_Kunikida	152	83	57	83	Uranohoshi	1
Dia_Kurosawa	162	80	57	80	Uranohoshi	3
Kanan_Matsuura	162	83	58	84	Uranohoshi	3
Mari_Ohara	163	87	60	84	Uranohoshi	3
Ayumu_Uehara	159	82	58	84	Nijigasaki	2
Ai_Miyashita	163	84	53	86	Nijigasaki	2
Setsuna_Yuki	154	83	56	81	Nijigasaki	2
Kasumi_Nakasu	155	76	55	79	Nijigasaki	1
Shizuku_Osaka	157	80	58	83	Nijigasaki	1
Rina_Tennoji	149	71	52	75	Nijigasaki	1
Emma_Verde	166	92	61	88	Nijigasaki	3
Kanata_Konoe	158	85	60	86	Nijigasaki	3
Karin_Asaka	167	88	57	89	Nijigasaki	3
Nico_Yazawa	154	71	57	79	Otonokizaka	3
\.


--
-- Data for Name: events; Type: TABLE DATA; Schema: public; Owner: hiraki
--

COPY public.events (day, month, type, details, short_note, note, notified) FROM stdin;
1	1	BD	Kurosawa Dia			f
6	1	AN	SIP S1 E1	S. Tomorrow	Susume Tomorrow	f
17	1	BD	Koizumi Hanayo			f
20	1	AN	SIP S1 E3	S. Dash	START: DASH	f
23	1	BD	Nakasu Kasumi			f
22	2	BD	Kusunoki Tomori	Setsuna	Setsuna's Seiyuu	f
25	2	BD	Arashi Chisato			f
27	2	BD	Koizumi Moeka	Shioriko	Shioriko's Seiyuu	f
1	3	BD	Uehara Ayumu			f
2	3	RE	Moment Ring	µ'sic forever	µ's Final Single	f
3	3	AN	SIP S1 E9	W. Zone	Wonder Zone	f
4	3	BD	Kunikida Hanamaru			f
15	3	BD	Sonoda Umi			f
17	3	AN	SIP S1 E11	N. B. Girls	No Brand Girl	f
25	3	PV	A song for You! You? You!!	2020	2020	f
3	4	BD	Osaka Shizuku			f
5	4	PV	HAPPY PARTY TRAIN	2017	2017	f
6	4	AN	SIP S2 E1	K. no LL	Koremade no Love Live	f
15	4	SP	SIF Birthday			f
17	4	BD	Watanabe You			f
17	4	BD	Sagara Mayu	Kasumin	Kasumin's Seiyuu	f
19	4	BD	Nishikino Maki			f
24	4	PV	Koi ni Naritai Aquarium	2016	2016	f
25	4	BD	Maeda Kaori	Shizuku	Shizuku's Seiyuu	f
1	5	BD	Shibuya Kanon			f
2	5	BD	Pile	Maki	Maki's Seiyuu	f
2	5	BD	Oonishi Aguri	Ayumu	Ayumu's Seiyuu	f
4	5	AN	SIP S2 E5	L. W. Bell	Love Wing Bell	f
11	5	AN	SIP S2 E6	D. S On Me	Dancing Stars on Me	f
19	5	BD	Kubo Yurika	Hanayo	Hanayo's Seiyuu	f
30	5	BD	Miyashita Ai			f
9	6	BD	Toujou Nozomi			f
26	6	BD	Asaka Karin			f
28	6	BD	Mimori Suzuko	Umi	Umi's Seiyuu	f
30	6	SP	Love Live! Debut	2010		f
2	7	AN	SS S1 E1	K. Hand in Hand	Kimetayo Hand in Hand	f
7	7	BD	Thảng Khửa Khừa			f
12	7	BD	Nanjou Yoshino	Eli	Eli's Seiyuu	f
13	7	BD	Tsushima Yoshiko			f
16	7	AN	SS S1 E3	D. D. Daijoubu	Daisuki Dattara Daijoubu	f
3	8	BD	Kousaka Honoka	HONKKK	HONKKK	f
6	8	AN	SS S1 E6	Y. Y. Terashitai	Yume wa Yozora de Terashitai	f
8	8	BD	Yuuki Setsuna			f
8	8	BD	Aida Rikako	Riko	Riko's Seiyuu	f
16	8	BD	Saito Shuka	You	You's Seiyuu	f
24	8	PV	Natsuiro Egao de 1 2 Jump!	2011	2011	f
25	8	PV	Bokura no LIVE Kimi tono LIFE	2010	2010	f
27	8	AN	SS S1 E9	M. Dreamer	Mijuku Dreamer	f
1	9	AN	SIP S2 E9	S. Halation	Snow Halation	f
5	9	PV	Wonderful Rush	2012	2012	f
7	9	BD	Murakami Natsumi	Miyashita Ai	Miyashita Ai's Seiyuu	f
10	9	AN	SS S1 E11	O. H. ni Nare	Omoiyo Hitotsu ni Nare	f
12	9	BD	Minami Kotori			f
19	9	BD	Sakurauchi Riko			f
24	9	AN	SS S1 E13	Mirai Ticket	Mirai Ticket	f
25	9	PV	Mitaiken Horizon	2019	2019	f
25	9	BD	Takatsuki Kanako	Hanamaru	Hanamaru's Seiyuu	f
26	9	SP	SIFAS Birthday			f
28	9	BD	Heanna Sumire			f
5	10	BD	Mifune Shioriko			f
6	10	BD	Tanaka Chiemi	Rina	Rina's Seiyuu	f
7	10	PV	Kimi no Kokoro ga Kagayaiteru kai?	2015	2015	f
7	10	AN	SS S2 E1			f
16	10	BD	Kitoo Akari	Kanata	Kanata's Seiyuu	f
21	10	BD	Ayase Eli			f
21	10	AN	SS S2 E3	M. M. Tonight	My Mai Tonight	f
23	10	BD	Kobayashi Aika	YOHANE	YOHANE's Seiyuu	f
26	10	BD	Iida Riho	Rin	Rin's Seiyuu	f
28	10	RE	Hear to Heart			f
30	10	PV	KOKORO Magic A to Z	2019	2019	f
1	11	BD	Hoshizora Rin			f
2	11	BD	Suwa Nanaka	Kanan	Kanan's Seiyuu	f
11	11	AN	SS S2 E6	M. Wave	Miracle Wave	f
13	11	BD	Tennoji Rina			f
18	11	AN	SS S2 E7	Sora mKmH kara	Sora mo Kokoro mo Hareru kara	f
24	11	BD	Hazuki Ren			f
27	11	AN	SIP OVA	M. START	MUSIC S.T.A.R.T	f
27	11	PV	Music START	µ's 6th	µ's 6th	f
2	12	AN	SS S2 E9	Aw. the Power	Awaken the Power	f
10	12	BD	Nitta Emi	Honoka	Honoka's Seiyuu	f
15	12	RE	Korekara			f
16	12	BD	Konoe Kanata			f
22	12	RE	Snow Halation	2010	2010	f
23	12	AN	SS S2 E12	WB NEW WORLD	WATER BLUE NEW WORLD	f
26	12	BD	Tokui Sora	Nico	Nico's Seiyuu	f
30	12	AN	SS S2 E13	WON. STORIES	WONDERFUL STORIES	f
5	3	BD	Yano Hinaki	Yuu	Takasaki Yuu	f
9	1	BD	Liyuu	Keke	Thảng Khửa Khừa	f
30	9	BD	Date Sayuri	Kanon	Shibuya Kanon	f
8	3	BD	Misaki Nako	Chisato	Arashi Chisato	f
16	5	BD	Aoyama Nagisa	Ren	Hazuki Ren	f
1	7	BD	Payton Naomi	Sumire	Heanna Sumire	f
23	7	BD	Suzuki Aina	Mari	Mari's Seiyuu	f
23	7	BD	Uchida Aya	Kotori	Kotori's Seiyuu	f
29	7	AN	SIP S2 E13	H. Maker	Happy Maker	f
1	8	BD	Takami Chika			f
20	9	BD	Sashide Maria	Emma	Emma's Seiyuu	t
21	9	BD	Kurosawa Ruby			t
31	1	BD	Kubota Miyu	Karin	Karin's Seiyuu	f
1	2	BD	Kusuda Aina	Nozomi	Nozomi's Seiyuu	f
5	2	BD	Emma Verde			f
5	2	BD	Komiya Arisa	Dia	Dia's Seiyuu	f
7	2	BD	Inami Anju	Chika	Chika's Seiyuu	f
10	2	BD	Matsuura Kanan			f
10	2	AN	SIP S1 E6	K. Someday	Korekara no Someday	f
15	2	PV	Mogyutto Love de Sekkinchuu!	2012	2012	f
19	2	BD	Furihata Ai	Ruby	Ruby's Seiyuu	f
\.


--
-- Data for Name: settings; Type: TABLE DATA; Schema: public; Owner: hiraki
--

COPY public.settings (field, value) FROM stdin;
pre-notify-channel-id	"694199808432537672"
notify-channel-id	"694843380844331038"
admin-roles-ids	["703534853001314344","694197858127052810"]
debug-channel-id	"749823581092839424"
emoji-react-signs	["ponk", "chonk", "yuusuffer", "marikek", "kanatasleep", "rikohmm", "makihuh"]
random-resp-signs	{"694191159949393980":{"threshold":1,"replies":["J kêu cc","J kêu gì","J"]},"hello":{"threshold":0.7,"replies":["Lô lô cc","Konnichiwa~"]},"g9|good night|oyasumi|đi ngủ":{"threshold":1,"replies":["Oyasuminasaiiiii~","J ngủ ngon","J chúc gặp nhiều ác mộng nha","J giờ này mà ngủ à. Sớm thế"]},"bye":{"threshold":1,"replies":["Mata ne~~","Jaa ne~","Byeee~","J đi luôn đi"]},"đảng|đcs|cộng sản":{"threshold":0.5,"replies":["<:dang:694251236895227965> <:dang:694251236895227965> <:dang:694251236895227965>"]}}
server-owner-id	"526086033025269760"
\.


--
-- Data for Name: systemlog; Type: TABLE DATA; Schema: public; Owner: hiraki
--

COPY public.systemlog (id, "time", content) FROM stdin;
\.


--
-- Name: systemlog_id_seq; Type: SEQUENCE SET; Schema: public; Owner: hiraki
--

SELECT pg_catalog.setval('public.systemlog_id_seq', 193, true);


--
-- Name: body pk_body; Type: CONSTRAINT; Schema: public; Owner: hiraki
--

ALTER TABLE ONLY public.body
    ADD CONSTRAINT pk_body PRIMARY KEY (name);


--
-- Name: events pk_events; Type: CONSTRAINT; Schema: public; Owner: hiraki
--

ALTER TABLE ONLY public.events
    ADD CONSTRAINT pk_events PRIMARY KEY (day, month, details);


--
-- Name: settings settings_pkey; Type: CONSTRAINT; Schema: public; Owner: hiraki
--

ALTER TABLE ONLY public.settings
    ADD CONSTRAINT settings_pkey PRIMARY KEY (field);


--
-- Name: systemlog systemlog_pkey; Type: CONSTRAINT; Schema: public; Owner: hiraki
--

ALTER TABLE ONLY public.systemlog
    ADD CONSTRAINT systemlog_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

