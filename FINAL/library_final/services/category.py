def get_all():
    from library_final.models.category import get_all_categories
    categories, error = get_all_categories()
    return categories, error


def count():
    from library_final.models.category import count_categories
    results_categories, error = count_categories()
    return results_categories, error


def get_by_id(id):
    from library_final.models.category import get_category_by_id
    category, error = get_category_by_id(id)
    return category, error


def save(data: dict):
    from library_final.models.category import create_category, update_category
    error = ''
    if data:
        if data.get('name') and not data.get('id'):
            _, error = create_category(data)
        if data.get('name') and data.get('id'):
            _, error = update_category(data)
    return _, error


def delete(id):
    from library_final.models.category import delete_category
    category, error = delete_category(id)
    return category, error
