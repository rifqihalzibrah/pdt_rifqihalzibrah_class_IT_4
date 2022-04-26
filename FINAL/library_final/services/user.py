from cmath import log


def save(data: dict):
    from library_final.models.user import signup
    error = ''
    if data:
        if data.get('name') and data.get('username') and data.get('password') and not data.get('id'):
            _, error = signup(data)
    return _, error


def get_user(data: dict):
    from library_final.models.user import login
    error = ''
    if data:
        if data.get('username') and data.get('password'):
            _, error = login(data)
    return _, error


def list_all_students():
    from library_final.models.user import list_all_students
    students, error = list_all_students()
    return students, error


def count():
    from library_final.models.user import count_users
    results_users, error = count_users()
    return results_users, error
