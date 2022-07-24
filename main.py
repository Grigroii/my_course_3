from flask import Flask, request, render_template, jsonify, abort, redirect
from utils import get_users_by_id, get_users, get_posts_all, get_comments_by_post_id, get_post_by_pk, search_for_posts, \
    get_posts_by_user, add_bookmark, del_bookmark, get_bookmarks, show_bookmarks
import logging

app = Flask(__name__)

logging.basicConfig(filename='logs/api.log', encoding='UTF-8', filemode='w', level=logging.INFO,
                    format='%(asctime)s [%(levelname)s] %(message)s')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('error404.html')


@app.errorhandler(500)
def page_error_handler(error):
    return render_template('error500.html')


@app.route('/')
def all_posts():
    list_of_posts = get_posts_all()
    logging.info('Список постов получен')
    return render_template('index.html', posts=list_of_posts)


@app.route('/posts/<int:uid>', methods=["GET"])
def get_post(uid):
    posts = get_post_by_pk(uid)
    comments = get_comments_by_post_id(uid)
    if len(comments) == 0:
        raise ValueError
    logging.info('Пост получен')
    return render_template('post.html', comments=comments,
                           posts=posts)


@app.route('/search/', methods=["GET"])
def search_page():
    max_posts = 10

    logging.info('Страница найдена')
    search_query = request.args.get('s', '')
    posts = search_for_posts(search_query)
    len_posts = len(posts)
    posts = posts[:max_posts]
    return render_template('search.html', search=search_query, posts=posts, len_posts=len_posts)


@app.route('/users/<username>', methods=["GET"])
def get_posters(username):
    posts = get_posts_by_user(username)
    if len(posts) == 0:
        raise ValueError
    logging.info('Получены посты конкретного пользователя')
    return render_template('user-feed.html', posters=posts)


app.config['JSON_AS_ASCII'] = False


@app.route('/api/posts', methods=["GET"])
def get_json_list():
    logging.info('Получен список постов в формате json')
    return jsonify(get_posts_all())


@app.route('/api/posts/<int:post_id>', methods=["GET"])
def get_json_post(post_id):
    logging.info('Получен пост по id пользователя в формате json')
    return jsonify(get_post_by_pk(post_id))


@app.route('/tag/<tagname>')
def get_tag(tagname):
    list_of_posts = get_posts_all()
    return render_template('tag.html', posts=list_of_posts)


@app.route('/book/<int:uid>')
def add_book(uid):
    add_bookmark(uid)
    return redirect('/')


@app.route('/del_book/<int:uid>')
def del_book(uid):
    del_bookmark(uid)
    return redirect('/')


@app.route('/api/post')
def api_posts():
    return jsonify(get_posts_all())


@app.route('/api/post/<int:pk>')
def api_post(pk):
    return jsonify(get_post_by_pk(pk))


@app.route('/bookmarks')
def get_bookmarks():
    bookmarks = show_bookmarks()
    return render_template('bookmarks.html', posts=bookmarks)


if __name__ == "__main__":
    app.run(debug=True)
