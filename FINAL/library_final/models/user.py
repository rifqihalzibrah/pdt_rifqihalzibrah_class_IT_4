from flask import session
from library_final.db import get_db


def signup(data):
    """ function to signup based on data dict """
    # trust that data is already complete
    error = ''
    db = get_db()
    cur = db.cursor()
    try:
        sql = """
            INSERT INTO users (name, username, password) VALUES ('%s', '%s', '%s')
        """ % (data.get('name'), data.get('username'), data.get('password'))
        cur.execute(sql)
        db.commit()
    except db.IntegrityError as e:
        error = e
    cur.close()
    return None, error


def login(data):
    """ function to get user by data """
    error = ''
    db = get_db()
    cur = db.cursor()
    sql = """
        SELECT id, username FROM users WHERE username = '%s' AND password = '%s'
    """ % (data.get('username'), data.get('password'))
    cur.execute(sql)
    user = cur.fetchone()
    cur.close()

    if user is None:
        error = 'Wrong credentials. No user found'
    else:
        session.clear()
        session['user_id'] = user[0]
        session['username'] = user[1]

    return user, error


def list_all_students():
    """ function to list all students in database """
    error = ''
    db = get_db()
    cur = db.cursor()
    sql = """
        SELECT id, username, name, password, borrowing FROM users WHERE id != 0
    """
    cur.execute(sql)
    students = cur.fetchall()
    cur.close()

    if not students:
        error = 'No Student Found'

    return students, error


def count_users():
    """ function to count all of the users except admin in database """
    error = ''
    db = get_db()
    cur = db.cursor()
    sql = """
        SELECT count(*) FROM users WHERE id != 0
    """
    cur.execute(sql)
    results_users = cur.fetchall()
    cur.close()

    if not results_users:
        error = '0'

    return results_users, error
