import os

import sqlite3

from flask import Flask, flash, redirect, render_template, request, session, jsonify, g
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# auto-reloaded templates
app.config["TEMPLATES_AUTO_RELOAD"] = True

# no cache
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# configure basic database
DATABASE = 'test.db'

@app.route("/")
@login_required
def index():

    return render_template("index.html")


@app.route("/hash")
@login_required
def hash():

    #confirm current user from session data
    cur_id = session["user_id"]

    return render_template("hash.html")

    # User reached route via POST (as by submitting a form via POST)
    #if request.method == "POST":



    #else render_template("hash.html")
    #basic schema for page
    # 1. drag and drop javascript box
    # 2. circle stating how many file hashes completed


@app.route("/login", methods=["GET", "POST"])
def login():
    
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)
        
        def dict_factory(cursor, row):
            d = {}
            for idx, col in enumerate(cursor.description):
                d[col[0]] = row[idx]
            return d
        
        #connect to database
        con = sqlite3.connect('test.db')
        con.row_factory = dict_factory
        cur = con.cursor()

        # Query database for username
        cur.execute("SELECT * FROM users WHERE username = ?", [request.form.get("username")])
        rows = cur.fetchall()

        con.commit()
        con.close()

        # Ensure username exists and password is correct
        
        
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
        
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        flash("logged in")
        # Redirect user to home page
        return redirect("/")
        
    # User reached route via GET (as by clicking a link or via redirect)
    else:

        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "GET":
        return render_template("register.html")

    elif request.method =="POST":
        #username blank

        if not request.form.get("username"):
            return apology("must provide a username")
        #pw or confirmation blank
        if not request.form.get("password") or not request.form.get("confirmation"):
            return apology("missing password and/or confirmation")

        if not request.form.get("email"):
            return apology("must provide an email")

        #allocate python variables for form content
        username = request.form.get("username")
        email = request.form.get("email")
        
        #query database for username
        con = sqlite3.connect('test.db')

        cur = con.cursor()

        cur.execute("SELECT * FROM users WHERE username = ?", [username])

        rows = cur.fetchall()

        con.commit()

        # check if username already exists
        if len(rows) != 0:
            return apology("that username is taken, try another")

        #pw and confirmation don't match
        if not request.form.get("password") == request.form.get("confirmation"):
            return apology("username and passwords do not match")

        cur.execute("SELECT * FROM users WHERE email = ?", [email])

        rows = cur.fetchall()

        con.commit()

        if len(rows) != 0:
            return apology("that email is taken, try another")

        #successful registration
        else:
            
            #get pw hash
            pwhash = generate_password_hash(request.form.get("password"))

            cur.execute("INSERT INTO users (username, hash, email) VALUES (?, ?, ?)", [username, pwhash, email])

            con.commit()

            con.close()
            #display message showing registration success
            flash("successfully registered")

    #redirect to login page
    return render_template("login.html")

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)