from flask import (
    Flask, request, render_template, session, flash, redirect, url_for, jsonify
)

from db import db_connection
import re


app = Flask(__name__)
app.secret_key = 'THISISMYSECRETKEY'  # create the unique one for yourself


@app.route('/login', methods=['GET', 'POST'])
def login():
    """ function to show and process login page """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = db_connection()
        cur = conn.cursor()
        sql = """
            SELECT id, username
            FROM users
            WHERE username = '%s' AND password = '%s'
        """ % (username, password)
        cur.execute(sql)
        user = cur.fetchone()

        error = ''
        if user is None:
            error = 'Wrong credentials. No user found'
        else:
            session.clear()
            session['user_id'] = user[0]
            session['username'] = user[1]
            return redirect(url_for('index'))

        flash(error)
        cur.close()
        conn.close()

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'name' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        name = request.form['name']
        # Check if account exists using MySQL
        conn = db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM users WHERE username = %s', (username,))
        account = cur.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.search(r'[A-Z]+', username):
            msg = 'Username must contain at least 1 uppercase character!'
        elif not re.search(r'[A-Z]+', password) or len(password) <= 4:
            # Yes, we cool 8D
            msg = 'Password must be at least 5 characters and 1 uppercase character'
        elif not username or not password or not name:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            sql = """
            INSERT INTO users (username, name, password) VALUES ('%s', '%s', '%s');
            """ % (username, name, password)
            cur.execute(sql)
            conn.commit()
            return redirect(url_for('index'))

    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)


@app.route('/logout')
def logout():
    """ function to do logout """
    session.clear()  # clear all sessions
    return redirect(url_for('login'))


@app.route('/')
def index():
    conn = db_connection()
    cur = conn.cursor()
    sql = """
        SELECT art.id, art.title, art.body, usr.username
        FROM articles art
        JOIN users usr ON usr.id = art.user_id
        ORDER BY art.title
    """
    cur.execute(sql)
    # [(1, "Article Title 1", "Art 1 content"), (2, "Title2", "Content 2"), ...]
    articles = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', articles=articles)


@app.route('/article/create', methods=['GET', 'POST'])
def create():
    # check if user is logged in
    if not session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        data = request.get_json() or {}
        # check existence of title and body
        if data.get('title') and data.get('body'):
            title = data.get('title', '')
            body = data.get('body', '')
            user_id = session.get('user_id')

            # strip() is to remove excessive whitespaces before saving
            title = title.strip()
            body = body.strip()

            conn = db_connection()
            cur = conn.cursor()
            # insert with the user_id
            sql = """
                INSERT INTO articles (title, body, user_id) VALUES ('%s', '%s', %d)
            """ % (title, body, user_id)
            cur.execute(sql)
            conn.commit()  # commit to make sure changes are saved
            cur.close()
            conn.close()
            # an example with redirect
            return jsonify({'status': 200, 'message': 'Success', 'redirect': '/'})

        # else will be error
        return jsonify({'status': 500, 'message': 'No Data submitted'})

    return render_template('create.html')


@app.route('/article/<int:article_id>', methods=['GET'])
def read(article_id):
    # find the article with id = article_id, return not found page if error
    conn = db_connection()
    cur = conn.cursor()
    sql = """
        SELECT art.title, art.body, usr.name
        FROM articles art
        JOIN users usr ON usr.id = art.user_id
        WHERE art.id = %s
    """ % article_id
    cur.execute(sql)
    article = cur.fetchone()
    cur.close()
    conn.close()
    return render_template('detail.html', article=article)


@app.route('/article/edit/<int:article_id>', methods=['GET', 'POST'])
def edit(article_id):
    # check if user is logged in
    if not session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        conn = db_connection()
        cur = conn.cursor()
        title = request.form['title']
        body = request.form['body']
        title = title.strip()
        body = body.strip()

        sql_params = (title, body, article_id)

        sql = "UPDATE articles SET title = '%s', body = '%s' WHERE id = %s" % sql_params
        print(sql)
        cur.execute(sql)
        cur.close()
        conn.commit()
        conn.close()
        # use redirect to go to certain url. url_for function accepts the
        # function name of the URL which is function index() in this case
        return redirect(url_for('index'))

    # find the record first
    conn = db_connection()
    cur = conn.cursor()
    sql = 'SELECT id, title, body FROM articles WHERE id = %s' % article_id
    cur.execute(sql)
    article = cur.fetchone()
    cur.close()
    conn.close()

    return render_template('edit.html', article=article)


@app.route('/article/delete/<int:article_id>', methods=['GET', 'POST'])
def delete(article_id):
    # check if user is logged in
    if not session:
        return redirect(url_for('login'))

    conn = db_connection()
    cur = conn.cursor()
    sql = 'DELETE FROM articles WHERE id = %s' % article_id
    cur.execute(sql)
    cur.close()
    conn.commit()
    conn.close()
    return jsonify({'status': 200, 'redirect': '/'})
