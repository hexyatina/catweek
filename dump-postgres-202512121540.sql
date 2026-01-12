--
-- PostgreSQL database dump
--

\restrict E1ftm9rscs6jC7hPNY5DA7ffmEMfWZAWCoLd0ZNjMqrzVfrgV4KY1EAd54Ce9g6

-- Dumped from database version 18.1
-- Dumped by pg_dump version 18.1

-- Started on 2025-12-12 15:40:35

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 219 (class 1259 OID 16617)
-- Name: days; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.days (
    dayid integer NOT NULL,
    dayname character varying(100),
    weekid integer
);


--
-- TOC entry 220 (class 1259 OID 16623)
-- Name: ipz_groups; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ipz_groups (
    groupid integer NOT NULL,
    groupname character varying(100)
);


--
-- TOC entry 221 (class 1259 OID 16629)
-- Name: lecturers; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.lecturers (
    lecturerid integer NOT NULL,
    lecturername character varying(100) NOT NULL
);


--
-- TOC entry 222 (class 1259 OID 16636)
-- Name: lessons; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.lessons (
    lessonid integer NOT NULL,
    lessonname character varying(100) NOT NULL
);


--
-- TOC entry 225 (class 1259 OID 16657)
-- Name: overall; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.overall (
    lessontime integer,
    groupnames integer,
    lesson integer,
    dayname integer,
    lecturer integer,
    place integer
);


--
-- TOC entry 223 (class 1259 OID 16643)
-- Name: places; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.places (
    placeid integer NOT NULL,
    cabinet character varying(100),
    url character varying(100)
);


--
-- TOC entry 224 (class 1259 OID 16649)
-- Name: times; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.times (
    timeid integer NOT NULL,
    timestart time without time zone NOT NULL,
    timeend time without time zone NOT NULL
);


--
-- TOC entry 5038 (class 0 OID 16617)
-- Dependencies: 219
-- Data for Name: days; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.days VALUES (500, 'Понеділок', 10001);
INSERT INTO public.days VALUES (501, 'Вівторок', 10001);
INSERT INTO public.days VALUES (502, 'Середа', 10001);
INSERT INTO public.days VALUES (503, 'Четвер', 10001);
INSERT INTO public.days VALUES (504, 'Пятниця', 10001);
INSERT INTO public.days VALUES (505, 'Понеділок', 10002);
INSERT INTO public.days VALUES (506, 'Вівторок', 10002);
INSERT INTO public.days VALUES (507, 'Середа', 10002);
INSERT INTO public.days VALUES (508, 'Четвер', 10002);
INSERT INTO public.days VALUES (509, 'Пятниця', 10002);


--
-- TOC entry 5039 (class 0 OID 16623)
-- Dependencies: 220
-- Data for Name: ipz_groups; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.ipz_groups VALUES (1001, 'IPZ-31');
INSERT INTO public.ipz_groups VALUES (1002, 'IPZ-32');
INSERT INTO public.ipz_groups VALUES (1003, 'IPZ-33');


--
-- TOC entry 5040 (class 0 OID 16629)
-- Dependencies: 221
-- Data for Name: lecturers; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.lecturers VALUES (101, 'Затула');
INSERT INTO public.lecturers VALUES (102, 'Капічина');
INSERT INTO public.lecturers VALUES (103, 'Степанюк');
INSERT INTO public.lecturers VALUES (104, 'Ходжаєв');
INSERT INTO public.lecturers VALUES (105, 'Головай');
INSERT INTO public.lecturers VALUES (106, 'Руденко');
INSERT INTO public.lecturers VALUES (107, 'Тільга');
INSERT INTO public.lecturers VALUES (108, 'Таран');
INSERT INTO public.lecturers VALUES (109, 'Мироненко');
INSERT INTO public.lecturers VALUES (110, 'Герасимович');
INSERT INTO public.lecturers VALUES (111, 'Гаращенкo');
INSERT INTO public.lecturers VALUES (112, 'Коваль');


--
-- TOC entry 5041 (class 0 OID 16636)
-- Dependencies: 222
-- Data for Name: lessons; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.lessons VALUES (1, 'Математичний аналіз');
INSERT INTO public.lessons VALUES (2, 'Лінійна алгебра');
INSERT INTO public.lessons VALUES (3, 'ІПЗ');
INSERT INTO public.lessons VALUES (4, 'Середовище розробки ПЗ');
INSERT INTO public.lessons VALUES (5, 'Українська мова');
INSERT INTO public.lessons VALUES (6, 'Англійська мова');
INSERT INTO public.lessons VALUES (7, 'Французька мова');
INSERT INTO public.lessons VALUES (8, 'ОПАМ');
INSERT INTO public.lessons VALUES (9, 'Фіз. виховання');
INSERT INTO public.lessons VALUES (10, 'АККС');
INSERT INTO public.lessons VALUES (11, 'Теорія ймовірності');
INSERT INTO public.lessons VALUES (12, 'Дискретна математика');


--
-- TOC entry 5044 (class 0 OID 16657)
-- Dependencies: 225
-- Data for Name: overall; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.overall VALUES (900, 1002, 1, 505, 101, 610);
INSERT INTO public.overall VALUES (901, 1002, 7, 505, 109, 611);
INSERT INTO public.overall VALUES (902, 1002, 2, 505, 102, 612);
INSERT INTO public.overall VALUES (903, 1002, 6, 505, 106, 613);
INSERT INTO public.overall VALUES (900, 1002, 12, 506, 102, 612);
INSERT INTO public.overall VALUES (901, 1002, 5, 506, 105, 614);
INSERT INTO public.overall VALUES (902, 1002, 8, 506, 103, 615);
INSERT INTO public.overall VALUES (900, 1002, 12, 507, 102, 612);
INSERT INTO public.overall VALUES (901, 1002, 11, 507, 101, 610);
INSERT INTO public.overall VALUES (903, 1002, 9, 507, 107, 616);
INSERT INTO public.overall VALUES (901, 1002, 8, 508, 103, 615);
INSERT INTO public.overall VALUES (902, 1002, 10, 508, 108, 617);
INSERT INTO public.overall VALUES (901, 1002, 5, 509, 105, 614);
INSERT INTO public.overall VALUES (902, 1002, 4, 509, 104, 618);
INSERT INTO public.overall VALUES (903, 1002, 3, 509, 103, 615);
INSERT INTO public.overall VALUES (904, 1002, 11, 509, 101, 610);
INSERT INTO public.overall VALUES (900, 1002, 1, 500, 101, 600);
INSERT INTO public.overall VALUES (901, 1002, 2, 500, 102, 601);
INSERT INTO public.overall VALUES (901, 1002, 3, 501, 103, 603);
INSERT INTO public.overall VALUES (902, 1002, 4, 501, 104, 604);
INSERT INTO public.overall VALUES (903, 1002, 5, 501, 105, 605);
INSERT INTO public.overall VALUES (900, 1002, 6, 502, 106, 608);
INSERT INTO public.overall VALUES (901, 1002, 8, 502, 103, 606);
INSERT INTO public.overall VALUES (900, 1002, 9, 503, 107, 607);
INSERT INTO public.overall VALUES (901, 1002, 3, 503, 103, 604);
INSERT INTO public.overall VALUES (902, 1002, 10, 503, 108, 603);
INSERT INTO public.overall VALUES (903, 1002, 11, 503, 101, 609);
INSERT INTO public.overall VALUES (900, 1002, 12, 504, 102, 601);
INSERT INTO public.overall VALUES (901, 1002, 7, 504, 109, 602);
INSERT INTO public.overall VALUES (901, 1003, 1, 505, 101, 610);
INSERT INTO public.overall VALUES (902, 1003, 7, 505, 109, 611);
INSERT INTO public.overall VALUES (903, 1003, 2, 505, 102, 612);
INSERT INTO public.overall VALUES (904, 1003, 11, 505, 101, 610);
INSERT INTO public.overall VALUES (901, 1003, 8, 506, 103, 615);
INSERT INTO public.overall VALUES (902, 1003, 5, 506, 110, 620);
INSERT INTO public.overall VALUES (903, 1003, 12, 506, 102, 612);
INSERT INTO public.overall VALUES (901, 1003, 12, 507, 102, 612);
INSERT INTO public.overall VALUES (902, 1003, 6, 507, 106, 613);
INSERT INTO public.overall VALUES (903, 1003, 9, 507, 107, 616);
INSERT INTO public.overall VALUES (900, 1003, 10, 508, 108, 617);
INSERT INTO public.overall VALUES (901, 1003, 5, 508, 110, 620);
INSERT INTO public.overall VALUES (902, 1003, 8, 508, 103, 615);
INSERT INTO public.overall VALUES (901, 1003, 3, 509, 103, 615);
INSERT INTO public.overall VALUES (902, 1003, 11, 509, 101, 610);
INSERT INTO public.overall VALUES (903, 1003, 4, 509, 104, 618);
INSERT INTO public.overall VALUES (902, 1003, 1, 500, 101, 600);
INSERT INTO public.overall VALUES (903, 1003, 2, 500, 102, 622);
INSERT INTO public.overall VALUES (900, 1003, 12, 501, 102, 601);
INSERT INTO public.overall VALUES (901, 1003, 5, 501, 110, 600);
INSERT INTO public.overall VALUES (902, 1003, 3, 501, 103, 606);
INSERT INTO public.overall VALUES (903, 1003, 4, 501, 104, 604);
INSERT INTO public.overall VALUES (901, 1003, 8, 502, 103, 606);
INSERT INTO public.overall VALUES (902, 1003, 6, 502, 106, 608);
INSERT INTO public.overall VALUES (902, 1003, 7, 502, 109, 623);
INSERT INTO public.overall VALUES (902, 1003, 9, 502, 107, 607);
INSERT INTO public.overall VALUES (902, 1003, 10, 503, 108, 603);
INSERT INTO public.overall VALUES (902, 1003, 11, 503, 101, 624);
INSERT INTO public.overall VALUES (902, 1003, 3, 503, 103, 604);
INSERT INTO public.overall VALUES (901, 1001, 1, 500, 101, 600);
INSERT INTO public.overall VALUES (902, 1001, 2, 500, 102, 601);
INSERT INTO public.overall VALUES (903, 1001, 11, 500, 101, 600);
INSERT INTO public.overall VALUES (900, 1001, 3, 501, 103, 603);
INSERT INTO public.overall VALUES (901, 1001, 4, 501, 104, 603);
INSERT INTO public.overall VALUES (902, 1001, 8, 502, 103, 606);
INSERT INTO public.overall VALUES (903, 1001, 6, 502, 106, 608);
INSERT INTO public.overall VALUES (900, 1001, 3, 503, 103, 604);
INSERT INTO public.overall VALUES (901, 1001, 10, 503, 108, 603);
INSERT INTO public.overall VALUES (902, 1001, 9, 503, 111, 607);
INSERT INTO public.overall VALUES (903, 1001, 12, 503, 102, 609);
INSERT INTO public.overall VALUES (902, 1001, 5, 504, 112, 622);
INSERT INTO public.overall VALUES (903, 1001, 7, 504, 109, 602);
INSERT INTO public.overall VALUES (901, 1001, 2, 505, 102, 612);
INSERT INTO public.overall VALUES (902, 1001, 6, 505, 106, 613);
INSERT INTO public.overall VALUES (903, 1001, 1, 505, 101, 610);
INSERT INTO public.overall VALUES (902, 1001, 7, 506, 109, 611);
INSERT INTO public.overall VALUES (903, 1001, 8, 506, 103, 615);
INSERT INTO public.overall VALUES (902, 1001, 12, 507, 102, 612);
INSERT INTO public.overall VALUES (903, 1001, 9, 507, 111, 619);
INSERT INTO public.overall VALUES (904, 1001, 11, 507, 101, 610);
INSERT INTO public.overall VALUES (900, 1001, 8, 508, 103, 615);
INSERT INTO public.overall VALUES (901, 1001, 10, 508, 108, 617);
INSERT INTO public.overall VALUES (902, 1001, 2, 508, 102, 612);
INSERT INTO public.overall VALUES (903, 1001, 5, 508, 112, 621);
INSERT INTO public.overall VALUES (900, 1001, 5, 509, 112, 621);
INSERT INTO public.overall VALUES (901, 1001, 4, 509, 104, 618);
INSERT INTO public.overall VALUES (902, 1001, 3, 509, 103, 615);
INSERT INTO public.overall VALUES (903, 1001, 11, 509, 101, 610);


--
-- TOC entry 5042 (class 0 OID 16643)
-- Dependencies: 223
-- Data for Name: places; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.places VALUES (600, '14', NULL);
INSERT INTO public.places VALUES (601, '41', NULL);
INSERT INTO public.places VALUES (602, '10', NULL);
INSERT INTO public.places VALUES (603, '25', NULL);
INSERT INTO public.places VALUES (604, '26', NULL);
INSERT INTO public.places VALUES (605, '35', NULL);
INSERT INTO public.places VALUES (606, '31', NULL);
INSERT INTO public.places VALUES (607, 'C3', NULL);
INSERT INTO public.places VALUES (608, '39', NULL);
INSERT INTO public.places VALUES (609, '37', NULL);
INSERT INTO public.places VALUES (610, NULL, 'https://us04web.zoom.us/j/79893401746?pwd=lis2aFba6MbmaEhCykzjgSdl0UK95C.1');
INSERT INTO public.places VALUES (611, NULL, 'https://us04web.zoom.us/j/79893401746?pwd=lis2aFba6MbmaEhCykzjgSdl0UK95C.1');
INSERT INTO public.places VALUES (612, NULL, 'https://discord.gg/SSFzX8a3');
INSERT INTO public.places VALUES (613, NULL, 'https://us05web.zoom.us/j/6678001520?pwd=bDFQejZyVFRmZlJ1eTh6YzIzcVBzZz09');
INSERT INTO public.places VALUES (614, NULL, 'https://us05web.zoom.us/j/83162010843?pwd=T0Jab1ZFMm4wMzdZYlZNZXhBb1BzUT09');
INSERT INTO public.places VALUES (615, NULL, 'https://docs.google.com/document/d/1r4HsNPDvVTG1rOkAklezFvXB1oPsMUvJg3qxhBnJVp0/edit?usp=sharing');
INSERT INTO public.places VALUES (616, NULL, 'https://us04web.zoom.us/j/74196688557?pwd=gr3YYdEnjDm2kwmG0UbG2EU50WAInI.1');
INSERT INTO public.places VALUES (617, NULL, 'https://us05web.zoom.us/j/89525632789?pwd=lvsjsxPulwqMMtIbB5yWCYP4ayMtUW.1');
INSERT INTO public.places VALUES (618, NULL, 'https://docs.google.com/document/d/1JDBdJ1BZ_Bm7qTCXCF49BIqPe14wj3B3AxJIdUEnUAM/edit?usp=sharing');
INSERT INTO public.places VALUES (619, NULL, 'https://us05web.zoom.us/j/9932278470?pwd=M0loWDJDNEZzOGFCTkhpNXZac1JVZz09');
INSERT INTO public.places VALUES (620, NULL, 'https://us04web.zoom.us/j/2559271800?pwd=aZbUrNEP9djKmbPQOP0IVQn3zWXAw0.1');
INSERT INTO public.places VALUES (621, NULL, 'https://us04web.zoom.us/j/72319798337?pwd=acAFeBjoF6wKUFFYtWETu8iLwNrx6L.1');
INSERT INTO public.places VALUES (622, '34', NULL);
INSERT INTO public.places VALUES (623, '20', NULL);
INSERT INTO public.places VALUES (624, '30', NULL);


--
-- TOC entry 5043 (class 0 OID 16649)
-- Dependencies: 224
-- Data for Name: times; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.times VALUES (900, '09:00:00', '10:20:00');
INSERT INTO public.times VALUES (901, '10:30:00', '11:50:00');
INSERT INTO public.times VALUES (902, '12:10:00', '13:30:00');
INSERT INTO public.times VALUES (903, '13:40:00', '15:00:00');
INSERT INTO public.times VALUES (904, '15:10:00', '16:30:00');


--
-- TOC entry 4880 (class 2606 OID 16622)
-- Name: days days_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.days
    ADD CONSTRAINT days_pkey PRIMARY KEY (dayid);


--
-- TOC entry 4882 (class 2606 OID 16628)
-- Name: ipz_groups ipz_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ipz_groups
    ADD CONSTRAINT ipz_groups_pkey PRIMARY KEY (groupid);


--
-- TOC entry 4884 (class 2606 OID 16635)
-- Name: lecturers lecturers_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.lecturers
    ADD CONSTRAINT lecturers_pkey PRIMARY KEY (lecturerid);


--
-- TOC entry 4886 (class 2606 OID 16642)
-- Name: lessons lessons_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.lessons
    ADD CONSTRAINT lessons_pkey PRIMARY KEY (lessonid);


--
-- TOC entry 4888 (class 2606 OID 16648)
-- Name: places places_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.places
    ADD CONSTRAINT places_pkey PRIMARY KEY (placeid);


--
-- TOC entry 4890 (class 2606 OID 16656)
-- Name: times times_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.times
    ADD CONSTRAINT times_pkey PRIMARY KEY (timeid);


-- Completed on 2025-12-12 15:40:35

--
-- PostgreSQL database dump complete
--

\unrestrict E1ftm9rscs6jC7hPNY5DA7ffmEMfWZAWCoLd0ZNjMqrzVfrgV4KY1EAd54Ce9g6

