import sys
import logging
import datetime
import numpy as np
from flask import Flask, request, jsonify, render_template, flash, redirect, session, url_for
from flaskext.mysql import MySQL
from urllib.parse import urlsplit
#from flask_mysqldb import MySQL
from login import LoginForm
#from homepage import HomePageForm
# from addcorkboard import AddCorkBoardForm
# from populartags import PopularTagsForm
# from searchpushpins import SearchForm
# from viewpushpin import ViewPushPin
# from addpushpin import AddPushPinForm
# from viewcorkboard import ViewCorkBoard
# from functools import wraps
# from popularsites import PopularSitesForm
# from corkboardstat import CorkBoardStat
# from checkpassword import CheckPasswordForm


# logger = logging.getLogger("logger")
# logger.setLevel(logging.INFO)
# file_handler = logging.FileHandler(filename='./logs/log')
# logger.addHandler(file_handler)

secret_key = "secret123"


app = Flask(__name__)
app.config['SECRET_KEY'] = secret_key
mysql = MySQL(app)

# Main DB
# app.config['MYSQL_DATABASE_USER'] = 'sql3411464'
# app.config['MYSQL_DATABASE_PASSWORD'] = 'ZVfm84xHeJ'
# app.config['MYSQL_DATABASE_DB'] = 'sql3411464'
# app.config['MYSQL_DATABASE_HOST'] = 'sql3.freemysqlhosting.net'

app.config['MYSQL_DATABASE_USER'] = 'sql3411464'
app.config['MYSQL_DATABASE_PASSWORD'] = 'ZVfm84xHeJ'
app.config['MYSQL_DATABASE_DB'] = 'sql3411464'
app.config['MYSQL_DATABASE_HOST'] = 'sql3.freemysqlhosting.net'

mysql.init_app(app)

# default route
@app.route('/')
def Home():
    cur = mysql.get_db().cursor()
    cur.execute("SELECT O.post_date,I.industry, O.count_id_indexed AS overall_count, I.count_id_indexed AS industry_count FROM Overall_count AS O INNER JOIN Industry_count AS I ON O.post_date = I.post_date GROUP BY I.industry")
    fetchdata = cur.fetchall()
    cur.close()
    
    return render_template('home.html', data=fetchdata)


# Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    session['logged_in'] = False
    login = LoginForm()
    if request.method == 'POST':
        if login.validate_on_submit():
            # Get Form Fields
            email = login.username.data
            password_candidate = login.password.data
            # Create Cursor
            cur = mysql.get_db().cursor()
            # Get user by name
            result = cur.execute ("SELECT * FROM User WHERE email = '%s'" % email)
            if result > 0:
                # Get stored pin
                data = cur.fetchone()
                password = data[1]
                # Compare Passwords
                if password_candidate == password:
                    # Passed
                    session['logged_in'] = True
                    session['email'] = email
                    return redirect('/index')
                else:
                    error = 'Invalid login.'
                    return render_template('Login.html', error=error, form=login)
                # Close connection
                cur.close()
            else:
                error = 'User not found.'
                return render_template('Login.html', error=error, form=login)
    return render_template('Login.html', title='Sign In', form=login)

if __name__ == '__main__':
    app.secret_key = secret_key
    app.run(debug = True)