from flask import (
    Blueprint, render_template, jsonify, request, redirect, url_for, flash, session
)
import library_final.services.user as svc_user
import library_final.services.category as svc_category
import library_final.services.book as svc_book

bp = Blueprint('user', __name__, url_prefix='/')


@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    error = ''
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']
        data = {
            'name': name.strip(),
            'username': username.strip(),
            'password': password.strip(),
        }
        _, error = svc_user.save(data)
        if not error:
            return redirect(url_for('home'))

        flash(error)

    return render_template('signup.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    error = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        data = {
            'username': username.strip(),
            'password': password.strip(),
        }
        _, error = svc_user.get_user(data)
        if not error and username == 'admin':
            return redirect(url_for('user.admin'))
        if not error and not username == 'admin':
            return redirect(url_for('home'))

        flash(error)

    return render_template('login.html')


@bp.route('/logout', methods=['GET', 'POST'])
def logout():
    """ function to do logout """
    session.clear()  # clear all sessions
    return redirect(url_for('home'))


@bp.route('/admin/dashboard', methods=['GET', 'POST'])
def admin():
    if not session:
        return redirect(url_for('home'))

    results_categories, error = svc_category.count()
    results_books, error = svc_book.count()
    results_users, error = svc_user.count()
    flash(error)

    return render_template('admin/dashboard.html', results_categories=results_categories[-1][-1], results_books=results_books[-1][-1], results_users=results_users[-1][-1])


@bp.route('/student_list', methods=['GET', 'POST'])
def list_all_students():
    if session.get('username') != 'admin':
        return redirect(url_for('home'))
        
    students, error = svc_user.list_all_students()
    flash(error)
    return render_template('admin/student_list.html', students=students)

