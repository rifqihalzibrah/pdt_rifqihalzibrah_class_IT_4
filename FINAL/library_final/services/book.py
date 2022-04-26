def get_all():
    from library_final.models.book import get_all_books
    books, error = get_all_books()
    return books, error


def count():
    from library_final.models.book import count_books
    results_books, error = count_books()
    return results_books, error


def get_by_id(id):
    from library_final.models.book import get_book_by_id
    book, error = get_book_by_id(id)
    return book, error


def borrow(id):
    from library_final.models.book import borrow_book
    status, error = borrow_book(id)
    return status, error


def return_book(id):
    from library_final.models.book import return_book
    status, error = return_book(id)
    return status, error


def save(data: dict):
    from library_final.models.book import create_book, update_book
    error = ''
    if data:
        if data.get('title') and data.get('author') and data.get('category_id') and not data.get('id'):
            _, error = create_book(data)
        if data.get('title') and data.get('author') and data.get('id'):
            _, error = update_book(data)
    return _, error


def delete(id):
    from library_final.models.book import delete_book
    book, error = delete_book(id)
    return book, error
