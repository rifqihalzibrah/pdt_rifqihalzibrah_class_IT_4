from flask import session
from library_final.db import get_db


def get_all_books():
    """ function to get all of the books in database """
    error = ''
    db = get_db()
    cur = db.cursor()
    sql = """
        SELECT book.id, book.title, book.author, category.name, book.status
        FROM books book
        JOIN categories category ON category.id = book.category_id
        ORDER BY book.title
    """
    cur.execute(sql)
    books = cur.fetchall()
    cur.close()

    if not books:
        error = 'No book found'

    return books, error


def count_books():
    """ function to count all of the books in database """
    error = ''
    db = get_db()
    cur = db.cursor()
    sql = """
        SELECT count(*) FROM books
    """
    cur.execute(sql)
    results_books = cur.fetchall()
    cur.close()

    if not results_books:
        error = '0'

    return results_books, error


def get_book_by_id(id):
    """ function to get book by id """
    error = ''
    db = get_db()
    cur = db.cursor()
    sql = """
        SELECT id, title, author, category_id FROM books WHERE id = %d
    """ % (int(id))
    cur.execute(sql)
    book = cur.fetchone()
    cur.close()

    if not book:
        error = 'Invalid book with id: %d' % id

    return book, error


def create_book(data):
    """ function to create book based on data dict """
    # trust that data is already complete
    error = ''
    db = get_db()
    cur = db.cursor()
    try:
        sql = """
            INSERT INTO books (title, author, category_id) VALUES ('%s', '%s', %d)
        """ % (data.get('title'), data.get('author'), data.get('category_id'))
        cur.execute(sql)
        db.commit()
    except db.IntegrityError as e:
        error = e
    cur.close()
    return None, error


def update_book(data):
    """ function to update book based on data dict """
    # trust that data is already complete
    error = ''
    db = get_db()
    cur = db.cursor()
    try:
        sql = """
            UPDATE books
            SET title = '%s', author = '%s', category_id = %d
            WHERE id = %d
        """ % (data.get('title'), data.get('author'), data.get('category_id'), data.get('id'))
        cur.execute(sql)
        db.commit()
    except db.IntegrityError as e:
        error = e
    cur.close()
    return None, error


def borrow_book(id):
    """ function to borrow book """
    # trust that data is already complete
    error = ''
    db = get_db()
    cur = db.cursor()
    try:
        sql = """
            UPDATE books SET status = false WHERE id = %d;
            UPDATE users SET borrowing = true WHERE id = %d;
        """ % (int(id), session.get('user_id'))
        cur.execute(sql)
        db.commit()
    except db.IntegrityError as e:
        error = e
    cur.close()
    return None, error


def return_book(id):
    """ function to return book """
    # trust that data is already complete
    error = ''
    db = get_db()
    cur = db.cursor()
    try:
        sql = """
            UPDATE books SET status = true WHERE id = %d;
            UPDATE users SET borrowing = false WHERE id = %d;
        """ % (int(id), session.get('user_id'))
        cur.execute(sql)
        db.commit()
    except db.IntegrityError as e:
        error = e
    cur.close()
    return None, error


def delete_book(id):
    """ function to delete book based on id """
    error = ''
    db = get_db()
    cur = db.cursor()
    try:
        sql = """
            DELETE FROM books WHERE id = %d
        """ % (int(id))
        cur.execute(sql)
        db.commit()
    except db.IntegrityError as e:
        error = e
    except db.DatabaseError as e:
        error = e

    cur.close()
    return None, error
