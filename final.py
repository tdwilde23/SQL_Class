import sqlite3
from bottle import route, run, template, get, post, request, redirect

con = sqlite3.connect("hospital.db")
cur = con.cursor()

specialties = ['','Allergy and immunology','Anesthesiology','Dermatology','Diagnostic radiology','Emergency medicine', \
    'Family medicine','Internal medicine','Medical genetics','Neurology','Nuclear medicine','Obstetrics and gynecology', \
    'Ophthalmology','Pathology','Pediatrics','Physical medicine and rehabilitation','Preventive medicine','Psychiatry', \
    'Radiation oncology','Surgery','Urology']

@route('/', method=['GET', 'POST'])
def homepage():
    return template('main', specialties = specialties)

@route('/listall', method = 'GET')
def listall():
    try:
        head = "All Doctors"
        headers = [header [1] for header in cur.execute('PRAGMA table_info(doctors)')]
        headers.pop()
        headers.append("dep_name")
        search_results = cur.execute('SELECT d_id, first_name, last_name, specialty, pager_num, dep_name FROM doctors JOIN departments USING(dep_id) LIMIT 20')
        return template('results', table=search_results, headers = headers, title="All Doctors", head=head)
    except:
        return template('error')

@route('/delete/<d_id>', method = 'GET')
def delete(d_id):
    try:
        doctor_ids = list(cur.execute('SELECT d_id FROM doctors'))
        if (int(d_id),) not in doctor_ids:
            return template('page_not_exist')
        deleted_doctor = cur.execute(f'SELECT d_id, first_name, last_name, specialty, pager_num, dep_name FROM doctors JOIN departments USING(dep_id) WHERE d_id = {d_id}')
        doctor = list(deleted_doctor)[0]
        head = f" {doctor[1]} {doctor[2]} with id {doctor[0]}"
        cur.execute(f'DELETE FROM doctors WHERE d_id = {d_id}')
        con.commit()
        return template("delete",title=f"Delete Dr.{doctor[2]}",head=head)
    except:
        return template('error')

@route('/search', method=['GET', 'POST'])
def search():
    firstname = request.forms.get('firstname')
    specialty = request.forms.get('specialty')
    headers = [header [1] for header in cur.execute('PRAGMA table_info(doctors)')]
    headers.pop()
    headers.append("dep_name")
    head = "Here are your search results"
    search_results = []
    if specialty == "" and firstname == "":
        redirect("/listall")
    elif specialty == "":
        search_results = cur.execute(f'SELECT d_id, first_name, last_name, specialty, pager_num, dep_name FROM doctors JOIN departments USING(dep_id) WHERE LOWER(first_name) LIKE LOWER(?) LIMIT 20',[f"%{firstname}%"])
        if list(search_results) == []:
            head = f"Your search did not return any results"
        search_results = cur.execute(f'SELECT d_id, first_name, last_name, specialty, pager_num, dep_name FROM doctors JOIN departments USING(dep_id) WHERE LOWER(first_name) LIKE LOWER(?) LIMIT 20',[f"%{firstname}%"])
    elif firstname == "":
        search_results = cur.execute(f'SELECT d_id, first_name, last_name, specialty, pager_num, dep_name FROM doctors JOIN departments USING(dep_id) WHERE LOWER(specialty) = LOWER("{specialty}") LIMIT 20')
    else:
        search_results = cur.execute(f'SELECT d_id, first_name, last_name, specialty, pager_num, dep_name FROM doctors JOIN departments USING(dep_id) WHERE LOWER(specialty) = LOWER("{specialty}") and LOWER(first_name) LIKE LOWER(?) LIMIT 20',[f"%{firstname}%"])
        if list(search_results) == []:
            head = f"Your search did not return any results"
        search_results = cur.execute(f'SELECT d_id, first_name, last_name, specialty, pager_num, dep_name FROM doctors JOIN departments USING(dep_id) WHERE LOWER(specialty) = LOWER("{specialty}") and LOWER(first_name) LIKE LOWER(?) LIMIT 20',[f"%{firstname}%"])
    return template('results', table=search_results, headers = headers, title="Search", head=head)

@route('/patients/<d_id>', method=['GET', 'POST'])
def patients(d_id):
    try:
        doctor_ids = list(cur.execute('SELECT d_id FROM doctors'))
        if (int(d_id),) not in doctor_ids:
            return template('page_not_exist')
        if request.method == 'POST':
            firstname = request.forms.get('firstname')
            lastname = request.forms.get('lastname')
            r_number = request.forms.get('r_number')
            dep = list(cur.execute(f"SELECT dep_id FROM doctors WHERE d_id = {d_id}"))[0][0]
            cur.execute(f"INSERT INTO patients(first_name, last_name, r_number, dep_id) VALUES (?,?,?,{dep})",[f'{firstname}',f'{lastname}',r_number])
            p_id = list(cur.execute(f"SELECT max(p_id) FROM patients"))[0][0]
            cur.execute(f"INSERT INTO patient_doctor VALUES ({p_id},{d_id})")
            con.commit()
        headers = ['p_id','first_name','last_name','room number']
        doctor = list(cur.execute(f'SELECT last_name FROM doctors WHERE d_id = {d_id}'))[0][0]
        head = f"patients for Dr.{doctor}"
        search_results = cur.execute(f"SELECT patients.p_id, patients.first_name, patients.last_name, patients.r_number FROM doctors JOIN patient_doctor USING(d_id) JOIN patients USING(p_id) WHERE d_id = {d_id}")
        return template('patients', table=search_results, headers = headers, title=f"Dr.{doctor}'s Patients", head=head, id=d_id)
    except:
        return template('error')

@route('/patients/<d_id>/add', method=['GET', 'POST'])
def patients(d_id):
    try:
        doctor_ids = list(cur.execute('SELECT d_id FROM doctors'))
        if (int(d_id),) not in doctor_ids:
            return template('page_not_exist')
        headers = ['p_id','first_name','last_name','room number']
        doctor = list(cur.execute(f'SELECT last_name FROM doctors WHERE d_id = {d_id}'))[0][0]
        search_results = cur.execute(f"SELECT patients.p_id, patients.first_name, patients.last_name, patients.r_number\
            FROM patients WHERE patients.p_id NOT IN \
            (SELECT patients.p_id FROM patients JOIN patient_doctor USING(p_id) JOIN doctors USING(d_id) WHERE d_id == {d_id})")
        return template('add_patient', title = f"Add Patient for Dr.{doctor}", table = search_results, headers=headers, id=d_id)
    except:
        return template('error')

@route('/patients/<d_id>/switch/<p_id>', method=['GET', 'POST'])
def patients(d_id, p_id):
    cur.execute(f"INSERT INTO patient_doctor VALUES ({p_id},{d_id})")
    con.commit()
    redirect(f"/patients/{d_id}")

@route('/patients/<d_id>/remove/<p_id>', method=['GET', 'POST'])
def patients(d_id, p_id):
    cur.execute(f'DELETE FROM patient_doctor WHERE d_id = {d_id} AND p_id = {p_id}')
    con.commit()
    redirect(f"/patients/{d_id}")

@post('/update/<d_id>')
def update(d_id):
    try:
        firstname = request.forms.get('firstname')
        lastname = request.forms.get('lastname')
        specialty = request.forms.get('specialty')
        pager_num = request.forms.get('page_num')
        dep = request.forms.get('dep')
        extra = ''
        if pager_num != '':
            pager_num = int(pager_num)
            if (pager_num,) in list(cur.execute(f"SELECT pager_num FROM doctors WHERE d_id <> {d_id}")):
                extra = f"This pager number ({pager_num}) is already in use"
                pager_num = ''
        if firstname != '' or lastname != '' or specialty != '' or pager_num != '' or dep != '':
            dep_id = ''
            if dep != '':
                dep_id = list(cur.execute(f'SELECT dep_id FROM departments WHERE dep_name = "{dep}"'))[0][0]
            info = [firstname, lastname, specialty, pager_num, dep_id]
            names = ["first_name","last_name","specialty","pager_num","dep_id"]
            query = 'UPDATE doctors SET'
            params = []
            first = True
            for attr,value in zip(names,info):
                if value == "":
                    continue
                else:
                    if type(value) == int:
                        if first:
                            query += f' {attr} = ?'
                            params.append(value)
                            first = False
                        else:
                            query += f', {attr} = ?'
                            params.append(value)
                    else:
                        if first:
                            query += f' {attr} = ?'
                            params.append(f"{value}")
                            first = False
                        else:
                            query += f', {attr} = ?'
                            params.append(f"{value}")
            query += f" WHERE d_id = {d_id}"
            cur.execute(query,params)
            con.commit()
        head = f"Update the doctor's information using the form below"
        headers = [header[1] for header in cur.execute('PRAGMA table_info(doctors)')]
        headers.pop()
        headers.append("dep_name")
        departments = [department[0] for department in cur.execute('SELECT dep_name FROM departments')]
        print(extra)
        search_results = cur.execute(f'SELECT d_id, first_name, last_name, specialty, pager_num, dep_name FROM doctors JOIN departments USING(dep_id) WHERE d_id = {d_id}')
        return template('doc_update', table=search_results, headers = headers, title="Update Doctor", head=head, id=d_id, departments = departments, specialties = specialties, extra = extra)
    except:
        return template('error')

@get('/update/<d_id>')
def view(d_id):
    try:
        doctor_ids = list(cur.execute('SELECT d_id FROM doctors'))
        if (int(d_id),) not in doctor_ids:
            return template('page_not_exist')
        head = f"Update the doctor's information using the form below"
        headers = [header[1] for header in cur.execute('PRAGMA table_info(doctors)')]
        headers.pop()
        headers.append("dep_name")
        extra = ''
        departments = [department[0] for department in cur.execute('SELECT dep_name FROM departments')]
        search_results = cur.execute(f'SELECT d_id, first_name, last_name, specialty, pager_num, dep_name FROM doctors JOIN departments USING(dep_id) WHERE d_id = {d_id}')
        return template('doc_update', table=search_results, headers = headers, title="Update Doctor", head=head, id=d_id, departments = departments, specialties = specialties, extra = extra)
    except:
        return template('error')

@route('/insert', method=['GET', 'POST'])
def insert():
    try:
        extra = ''
        if request.method == "POST":
            firstname = request.forms.get('firstname')
            lastname = request.forms.get('lastname')
            specialty = request.forms.get('specialty')
            pager_num = request.forms.get('page_num')
            dep = request.forms.get('dep')
            dep_id = ''
            if pager_num != '':
                pager_num = int(pager_num)
                if (pager_num,) in list(cur.execute(f"SELECT pager_num FROM doctors")):
                    extra = f"This pager number ({pager_num}) is already in use. Data was input without pager number"
                    pager_num = ''
            if dep != '':
                dep_id = list(cur.execute(f'SELECT dep_id FROM departments WHERE dep_name = "{dep}"'))[0][0]
            info = [firstname, lastname, specialty, pager_num, dep_id]
            names = ["first_name","last_name","specialty","pager_num","dep_id"]
            args = 'INSERT INTO doctors('
            vals = 'VALUES ('
            params = []
            first = True
            for attr,value in zip(names,info):
                if value == "":
                    continue
                else:
                    if type(value) == int:
                        if first:
                            args += f' {attr}'
                            vals += f' ?'
                            params.append(value)
                            first = False
                        else:
                            args += f', {attr}'
                            vals += f', ?'
                            params.append(value)
                    else:
                        if first:
                            args += f' {attr}'
                            vals += f' ?'
                            params.append(f"{value}")
                            first = False
                        else:
                            args += f', {attr}'
                            vals += f', ?'
                            params.append(f"{value}")
            query = args + ") " + vals + ")"
            print(query)
            print(params)
            cur.execute(query,params)
            con.commit()
        head = f"Insert the new doctor's information using the form below"
        headers = [header[1] for header in cur.execute('PRAGMA table_info(doctors)')]
        headers.pop()
        headers.append("dep_name")
        departments = [department[0] for department in cur.execute('SELECT dep_name FROM departments')]
        return template('add_doc', headers = headers, title="Add Doctor", head=head, departments = departments, specialties = specialties, extra=extra)
    except:
        return template('error')

run(host='localhost', port=8080, debug=True, reloader=True)