from flask import Flask, render_template, request, json, jsonify, redirect, url_for
from flask.ext.mysql import MySQL

app = Flask(__name__)
mysql = MySQL()

# MySql Configuration
app.config['MYSQL_DATABASE_USER'] = 'root'
# app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'Contacts'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

conn = mysql.connect()
cursor = conn.cursor()

# Creating a new route for home page
@app.route("/")
def main():
    try:
        query = '''select * from `Contacts`.`contact`;'''
        cursor.execute(query)
        alldata = cursor.fetchall()
        # print jsonify(data = alldata);
        # conn.commit()
        # cursor.close()
        return render_template('index.html',rows = alldata)
    except Exception as e:
        print e;
        return e;

# Creating a route with method as POST and it will get called when the user will post new contact data
@app.route("/addContact/", methods=['POST'])
def addContact():
    try:
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        phone = request.form['phone']
        skypeid = request.form['skypeid']

        if firstname and lastname and email and phone and skypeid:
            query = '''INSERT INTO `Contacts`.`contact` (user_firstname, user_lastname, email, phone, skypeid)
                          VALUES (%s,%s,%s,%d,%s)'''% ("'" + str(firstname) + "'", "'" + str(lastname) + "'", "'" +
                                str(email) + "'", int(phone), "'" + str(skypeid) + "'") + ';';
            cursor.execute(query)
            conn.commit()

            # Redirecting to the route '/'
            return redirect('/');
        else:
            return render_template('error.html', message='Enter all required fields');
    except Exception as e:
        print e;
        return e.message;
if __name__ == "__main__":
    app.run()
