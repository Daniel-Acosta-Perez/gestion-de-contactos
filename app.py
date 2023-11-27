from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL


app = Flask(__name__)

#? MySQL conection

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'gestion_contactos'
mysql = MySQL(app)

# settings
app.secret_key = 'mysecretkey'

@app.route('/')
def Index():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM contacts')
    data = cursor.fetchall()
    return render_template('index.html', contacts = data)

@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email= request.form['email']
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO contacts (contact_name, contact_phone, contact_email) VALUES (%s, %s, %s)', (fullname, phone, email))
        mysql.connection.commit()
        flash('Contacto agregado succesfully')
        return redirect(url_for('Index'))

@app.route('/edit/<id>')
def get_contact(id):
    cursor = mysql.connection.cursor()
    cursor.execute(f'SELECT * FROM contacts WHERE contact_id = {id}')
    data = cursor.fetchall()
    return render_template('edit_contact.html', contact = data[0])

@app.route('/update/<id>', methods = ['POST'])
def update_contact(id):
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email= request.form['email']
        cursor = mysql.connection.cursor()
        cursor.execute("""
        UPDATE contacts
        SET contact_name = %s,
            contact_phone = %s,
            contact_email = %s
        WHERE contact_id = %s
        """, (fullname, phone, email, id))
        mysql.connection.commit()
        flash('Contacto actualizado')
        return redirect(url_for('Index'))


@app.route('/delete_contact/<string:id>')
def delete_contact(id):
    cursor = mysql.connection.cursor()
    cursor.execute(f'DELETE FROM contacts WHERE contact_id = {id}')
    mysql.connection.commit()
    flash('Contacto eliminado')
    return redirect(url_for('Index'))


if __name__ == "__main__":
    app.run(port=3000, debug=True )

