from turtle import title
from flask import (
    Blueprint, render_template, jsonify, request, redirect, url_for, flash, session
)
import library_final.services.book as svc_book
import library_final.services.category as svc_category


bp = Blueprint('book', __name__, url_prefix='/book')


# HTML related routes
@bp.route('/', methods=['GET'])
def home():
    books, error = svc_book.get_all()
    flash(error)
    return render_template('book/index.html', books=books)


@bp.route('/create', methods=['GET', 'POST'])
def create():
    if session.get('username') != 'admin':
        return redirect(url_for('home'))

    err = ''
    categories, _ = svc_category.get_all()
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        category_id = request.form['category_id']
        data = {
            'title': title.strip(),
            'author': author.strip(),
            'category_id': int(category_id),
        }
        _, error = svc_book.save(data)
        if not error:
            return redirect(url_for('book.home'))

        flash(err)

    return render_template('book/create.html', categories=categories)


@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    if session.get('username') != 'admin':
        return redirect(url_for('home'))

    err = ''
    book, error = svc_book.get_by_id(id)
    categories, _ = svc_category.get_all()

    if request.method == 'POST':
        name = request.form['name']
        category_id = request.form['category_id']
        data = {
            'id': int(id),
            'name': name.strip(),
            'category_id': int(category_id),
        }
        _, error = svc_book.save(data)
        if not error:
            return redirect(url_for('book.home'))

        flash(err)

    return render_template('book/edit.html', book=book, categories=categories)


@bp.route('/borrow/<int:id>', methods=['GET', 'POST'])
def borrow(id):
    if session.get('username') == 'admin':
        return redirect(url_for('home'))
    
    if not session:
        return redirect(url_for('home'))

    book, error = svc_book.get_by_id(id)
    if request.method == 'POST':
        _, error = svc_book.borrow(id)
        if not error:
            return redirect(url_for('book.home'))

    flash(error)
    return render_template('book/borrow.html', book=book)


@bp.route('/return/<int:id>', methods=['GET', 'POST'])
def return_book(id):
    if session.get('username') == 'admin':
        return redirect(url_for('home'))
    
    if not session:
        return redirect(url_for('home'))

    book, error = svc_book.get_by_id(id)
    if request.method == 'POST':
        _, error = svc_book.return_book(id)
        if not error:
            return redirect(url_for('book.home'))

    flash(error)
    return render_template('book/return.html', book=book)


@bp.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    if session.get('username') != 'admin':
        return redirect(url_for('home'))

    book, error = svc_book.get_by_id(id)
    if request.method == 'POST':
        _, error = svc_book.delete(id)
        if not error:
            return redirect(url_for('book.home'))

    flash(error)
    return render_template('book/delete.html', book=book)
