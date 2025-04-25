from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'flash message'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'foo'
app.config['MYSQL_PASSWORD'] = 'foo123'
app.config['MYSQL_DB'] = 'curd_flask'

mysql = MySQL(app)


@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM students")
    data = cur.fetchall()
    cur.close
    return render_template('app.html', students=data)


@app.route('/add', methods=['POST'])
def add():
    if request.method == 'POST':
        flash('Data Inserted Successfully')
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        city = request.form['city']
        pincode = request.form['pincode']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO students (name, email, phone, address, city, pincode) VALUES (%s, %s, %s, %s, %s, %s)',
                    (name, email, phone, address, city, pincode))
        mysql.connection.commit()
        return redirect(url_for('index'))


@app.route('/update', methods=['POST', 'GET'])
def update():
    if request.method == 'POST':
        id_data = request.form['id']
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        city = request.form['city']
        pincode = request.form['pincode']

        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE students
            SET name=%s,
                email=%s,
                phone=%s,
                address=%s,
                city=%s,
                pincode=%s
            WHERE id=%s
        """, (name, email, phone, address, city, pincode, id_data))
        flash("Data Updated Successfully")
        mysql.connection.commit()
        return redirect(url_for('index'))


@app.route('/delete/<string:id_data>', methods=['POST', 'GET'])
def delete(id_data):
    flash("Record Has Been Deleted Successfully")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM students WHERE id={0}".format(id_data))
    mysql.connection.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
