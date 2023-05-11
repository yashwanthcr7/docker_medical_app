from flask import Flask, render_template, request
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'my-mysql-container'
app.config['MYSQL_USER'] = 'myuser'
app.config['MYSQL_PASSWORD'] = 'mypassword'
app.config['MYSQL_DB'] = 'mydb'

mysql = MySQL(app)

@app.route('/')
def home():
    cur = mysql.connection.cursor()
    cur.execute("""
            CREATE TABLE IF NOT EXISTS patients (
            id INT AUTO_INCREMENT PRIMARY KEY,
            first_name VARCHAR(255),
            last_name VARCHAR(255),
            dob DATE,
            gender VARCHAR(10),
            diagnosis VARCHAR(255),
            covid VARCHAR(255),
            address VARCHAR(255)
        )
    """)
    mysql.connection.commit()
    cur.close()
    return render_template('home.html')

@app.route('/add_patient', methods=['GET', 'POST'])
def add_patient():
    if request.method == 'POST':
        # get form data
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        dob = request.form['dob']
        gender = request.form['gender']
        diagnosis = request.form['diagnosis']
        covid = request.form['covid']
        address = request.form['address']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO patients (first_name, last_name, dob, gender, diagnosis, covid, address) VALUES (%s, %s, %s, %s, %s, %s, %s)", (first_name, last_name, dob, gender, diagnosis, covid, address))
        mysql.connection.commit()
        cur.close()
        return 'Patient added successfully'
    else:
        return render_template('add_patient.html')

@app.route('/view_patients')
def view_patients():
    cur = mysql.connection.cursor()

    cur.execute("SELECT * FROM patients")

    patients = cur.fetchall()

    cur.close()
    return render_template('view_patients.html', patients=patients)

if __name__ == '__main__':
    app.run(host='0.0.0.0')


