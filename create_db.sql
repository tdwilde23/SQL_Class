----

--
-- Name: departments; Type: TABLE; Schema:
--

CREATE TABLE departments (
    dep_id INTEGER PRIMARY KEY,
    dep_name varchar NOT NULL
);

--
-- Name: doctors; Type: TABLE; Schema:
--

CREATE TABLE doctors (
    d_id INTEGER PRIMARY KEY,
    first_name varchar NOT NULL,
    last_name varchar NOT NULL,
    specialty varchar,
    pager_num int,
    dep_id REFERENCES deparments(dep_id)
);

--
-- Name: nurses; Type: TABLE; Schema:
--

CREATE TABLE nurses (
    n_id INTEGER PRIMARY KEY,
    first_name varchar NOT NULL,
    last_name varchar NOT NULL,
    pager_num int,
    dep_id REFERENCES deparments(dep_id)
);

--Medications(id int pkey, name string [not null], type string [not null], common use string)

CREATE TABLE medications (
    m_id INTEGER PRIMARY KEY,
    med_name varchar NOT NULL,
    med_type varchar NOT NULL,
    common_use varchar
);

--
-- Name: rooms; Type: TABLE; Schema:
--

CREATE TABLE rooms (
    r_number INTEGER PRIMARY KEY,
    dep_id REFERENCES departments(dep_id),
    n_id REFERENCES nurses(n_id)
);

--
-- Name: patients; Type: TABLE; Schema:
--

CREATE TABLE patients (
    p_id INTEGER PRIMARY KEY,
    first_name varchar NOT NULL,
    last_name varchar NOT NULL,
    r_number REFERENCES rooms (r_number),
    dep_id REFERENCES deparments (dep_id)
);

--Diagnoses(id int pkey, name string [not null], typical treatment, department fkey(department))

CREATE TABLE diagnoses (
    diag_id INTEGER PRIMARY KEY,
    diag_name VARCHAR NOT NULL,
    treatment VARCHAR NOT NULL,
    dep_id REFERENCES departments (dep_id) 
);

--Visitors(id int pkey, first_name string [not null], last_name varchar [not null], 
--time_in int [not null], time_out int, fkey(patients))

CREATE TABLE visitors (
    v_id INTEGER PRIMARY KEY,
    first_name varchar NOT NULL,
    last_name varchar NOT NULL,
    time_in time NOT NULL,
    time_out time,
    p_id REFERENCES patients (p_id)
);

--patient_doctor(patient fkey(patients(p_id)), doctor fkey(doctors))

CREATE TABLE patient_doctor (
    p_id REFERENCES patients (p_id),
    d_id REFERENCES doctors (d_id)
);

--nurse_dep(department fkey(departments), nurse fkey(nurses))

CREATE TABLE nurse_rooms (
    n_id REFERENCES nurses (n_id),
    r_number REFERENCES rooms (r_number)

);

--diagnosis(patient fkey(patients), diagnosis fkey(diagnoses))

CREATE TABLE diagnosis (
    p_id REFERENCES patients (p_id),
    diag_id REFERENCES diagnoses (diag_id)

);


--prescription(patient fkey(patients), prescription fkey(medications))

CREATE TABLE prescriptions (
    p_id REFERENCES patients (p_id),
    m_id REFERENCES medications (m_id)

);