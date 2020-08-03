import json
import dbconnection
from flask import Flask, request, Response, render_template, redirect, url_for,session,flash
from functools import wraps
import bcrypt
app = Flask(__name__)

users = []

def init_list():

    users[:] = []
    dbconnection.db_conn.init_app(app)
    cursor = dbconnection.db_conn.get_cursor()
    cursor.execute('''SELECT * FROM Users''')
    for row in cursor:
        user = {"id":row[0], "name":row[1], "email":row[2], "leavestaken":row[3], "leavesleft":row[4]}
        users.append(user)
    dbconnection.db_conn.commit()
    dbconnection.db_conn.close_connection()


# index
@app.route('/users/index')
def index():
    init_list()
    return render_template('index.html', result = index)



@app.route('/users/all')
def get_users():
    init_list()
    return render_template('users.html', result = users)



# find user by id
@app.route('/users/<id>')
def edit_user(id):
    dbconnection.db_conn.init_app(app)
    cursor = dbconnection.db_conn.get_cursor()
    cursor.execute('''SELECT * FROM Users WHERE Id = ? ''', (id,))
    row = cursor.fetchone()
    user = {"id":row[0], "name":row[1], "email":row[2], "leavestaken":row[3], "leavesleft":row[4]}
    dbconnection.db_conn.commit()
    dbconnection.db_conn.close_connection()
    return render_template('user.html', user = user)

# new user form
@app.route('/users/newuser')
def new_user():
    return render_template('newuser.html')


# add user to database
@app.route('/users/newuser/add', methods = ['POST'])
def add_new_user():
    user = request.form
    dbconnection.db_conn.init_app(app)
    cursor = dbconnection.db_conn.get_cursor()
    fname = str(user['name'])
    email = str(user['email'])
    ltake = str(user['leavestaken'])
    lleft = str(user['leavesleft'])
    cursor.execute('''INSERT INTO Users(Name, Email, LeavesTaken, LeavesLeft) VALUES(?, ?, ?, ?)''', (fname, email, ltake, lleft))
    dbconnection.db_conn.commit()
    dbconnection.db_conn.close_connection()
    return redirect(url_for('get_users'))

# update user information
@app.route('/users/update', methods = ['PUT', 'POST'])
def update_user():
    user = request.form
    dbconnection.db_conn.init_app(app)
    cursor = dbconnection.db_conn.get_cursor()
    fname = str(user['name'])
    email = str(user['email'])
    ltake = str(user['leavestaken'])
    lleft = str(user['leavesleft'])
    cursor.execute('''UPDATE Users SET Name = ?, Email = ?, LeavesTaken = ?, LeavesLeft = ? WHERE Id = ? ''', (fname, email, ltake, lleft, user['id']))
    dbconnection.db_conn.commit()
    dbconnection.db_conn.close_connection()
    return redirect(url_for('get_users'))

@app.route('/users/delete', methods = ['DELETE', 'POST'])
def delete_user():
    user = request.form
    dbconnection.db_conn.init_app(app)
    dbconnection.db_conn.connection.execute('''DELETE FROM Users WHERE Id = ? ''', (user['id'],))
    dbconnection.db_conn.commit()
    dbconnection.db_conn.close_connection()
    return redirect(url_for('get_users'))

@app.route('/users/json/all')
def get_users_json():
    init_list()
    u = json.dumps(users, indent=True)
    resp = Response(u, status=200, mimetype='application/json')
    return resp

@app.route('/users/json/<username>')
def get_user_json(username):
    dbconnection.db_conn.init_app(app)
    cursor = dbconnection.db_conn.get_cursor()
    cursor.execute('''SELECT * FROM Users WHERE Username = ? ''', (username,))
    dbconnection.db_conn.commit()
    row = cursor.fetchone()
    return json.dumps({"id":row[0], "name":row[1], "email":row[2], "leavestaken":row[3], "leavesleft":row[4]}, indent=True)

@app.route('/users/json/add', methods = ['POST'])
def add_new_user_json():
    user = request.get_json(force=True)
    dbconnection.db_conn.init_app(app)
    cursor = dbconnection.db_conn.get_cursor()
    fname = str(user['name'])
    email = str(user['email'])
    ltake = str(user['leavestaken'])
    lleft = str(user['leavesleft'])
    cursor.execute('''INSERT INTO Users(Name, Email, LeavesTaken, LeavesLeft) VALUES(?, ?, ?, ?)''', (fname, email, ltake, lleft))
    dbconnection.db_conn.commit()
    dbconnection.db_conn.close_connection()
    return json.dumps(user, indent=True)

@app.route('/users/json/update', methods = ['PUT', 'POST'])
def update_user_json():
    user = request.get_json(force=True)
    dbconnection.db_conn.init_app(app)
    cursor = dbconnection.db_conn.get_cursor()
    fname = str(user['name'])
    email = str(user['email'])
    ltake = str(user['leavestaken'])
    lleft = str(user['leavesleft'])
    cursor.execute('''UPDATE Users SET Name = ?, Email = ?, LeavesTaken = ?, LeavesLeft = ? WHERE Id = ? ''', (fname, email, ltake, lleft, user['id']))
    dbconnection.db_conn.commit()
    dbconnection.db_conn.close_connection()
    return json.dumps(user, indent=True)

@app.route('/users/json/delete', methods = ['DELETE','POST'])
def delete_user_json():
    user = request.get_json(force = True)
    dbconnection.db_conn.init_app(app)
    dbconnection.db_conn.connection.execute('''DELETE FROM Users WHERE Id = ? ''', (user['id'],))
    dbconnection.db_conn.commit()
    dbconnection.db_conn.close_connection()
    return "Success!"


# for easy routing
@app.route('/')
def index_site():
    return redirect(url_for('index'))

@app.route('/users')
def user_index():
    return redirect(url_for('get_users'))

if __name__ == '__main__':
    app.run(debug = True)
