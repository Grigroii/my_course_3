import json
from json import JSONDecodeError


def get_posts_all(file_name='C:\python\pythonEducation\pythonProject5\Home_work_3\data\data.json'):
    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            items = json.load(file)
            bookmarks = get_bookmarks()
            for item in items:
                item['is_bookmark'] = item['pk'] in bookmarks


    except (FileNotFoundError, JSONDecodeError):
        raise ValueError('Файл не найден')
    return items


def get_posts_in_bookmarks():
    try:
        with open('C:\python\pythonEducation\pythonProject5\Home_work_3\data\data.json', 'r', encoding='utf-8') as file:
            items = json.load(file)
            bookmarks = get_bookmarks()
            items = [item for item in items if item['pk'] in bookmarks]

    except (FileNotFoundError, JSONDecodeError):
        raise ValueError('Файл не найден')
    return items


def get_users():
    users = set()
    for item in get_posts_all():
        users.add(item['poster_name'])
    return list(users)


def get_users_by_id():
    users = set()
    for item in get_posts_all():
        users.add(item['pk'])
    return users


def get_comments():
    with open('C:\python\pythonEducation\pythonProject5\Home_work_3\data\comments.json', 'r', encoding='utf-8') as file:
        items = json.load(file)
        return items


def get_posts_by_user(user_name):
    result = []
    for item in get_posts_all():
        if user_name.lower() in item["poster_name"].lower():
            result.append(item)
    return result


def get_comments_by_post_id(post_id):
    result = []
    for item in get_comments():
        if post_id == item["post_id"]:
            result.append(item)
    return result


def search_for_posts(query: str):
    result = []
    for item in get_posts_all():
        if query.lower() in item["content"].lower():
            result.append(item)
    return result


def get_post_by_pk(pk):
    all_posts = get_posts_all()

    for item in all_posts:
        if pk == item["pk"]:
            return item
    raise ValueError


def get_bookmarks():
    with open('C:\python\pythonEducation\pythonProject5\Home_work_3\data/bookmarks.json', 'r',
              encoding='utf-8') as file:
        items = json.load(file)
    return items


def add_bookmark(id):
    items = get_bookmarks()
    items.append(id)
    items = list(set(items))

    with open('C:\python\pythonEducation\pythonProject5\Home_work_3\data/bookmarks.json', 'w',
              encoding='utf-8') as file:
        json.dump(items, file)
    return True


def del_bookmark(id):
    items = get_bookmarks()
    items.remove(id)
    items = list(set(items))

    with open('C:\python\pythonEducation\pythonProject5\Home_work_3\data/bookmarks.json', 'w',
              encoding='utf-8') as file:
        json.dump(items, file)
    return True


def show_bookmarks():
    result = []
    posts = get_posts_all()
    items = get_bookmarks()
    for post in posts:
        if post['pk'] in items:
            result.append(post)
    return result
