import flask
import json
from flask import Flask
import markdown
from markupsafe import Markup
import os
app = Flask(__name__)

app.config.from_pyfile('settings.py')

blog_list = []

if os.path.exists("posts_catalog.json"):
    with open('posts_catalog.json', 'r', encoding='utf-8') as yf:
        blog_list = json.load(yf)


@app.route('/')
def index():
    if blog_list:
        reverse_list = []
        reverse_list = blog_list
        reverse_list = list(reversed(reverse_list))
        i = 0

        while (i < len(reverse_list)):
            post = reverse_list[i]
            title = post['title']
            blog = Markup(markdown.markdown(post['blog'], output_format = 'html5'))
            id = len(reverse_list) - i
            id -= 1
            post.update({'title' : title, 'blog' : blog, 'id': id})
            i += 1



    else:
        blog_post = ""

    return flask.render_template('index.html', blog_list= reverse_list)


@app.route('/login.html')
def login():
    return flask.render_template('login.html')


@app.route('/posts/<int:pid>')
def new_post(pid):
    if pid < 0 or pid >= len(blog_list):
        flask.abort(404)

    temp = blog_list[pid]
    title = temp['title']
    blog = Markup(markdown.markdown(temp['blog'], output_format = 'html5'))
    blog_post = ({'title':title, 'blog':blog})
    # blog_post = blog_list[pid]
    return flask.render_template('posts.html', blog_post=blog_post)


@app.route('/posts.html')
def posts():
    return flask.render_template('posts.html')


@app.route('/add')
def add_form():
    return flask.render_template('new_post.html')


@app.route('/add', methods=['POST'])
def add_post():
    title = flask.request.form['title']
    blog = Markup(markdown.markdown(flask.request.form['blog'], output_format='html5'))
    pid = len(blog_list)
    blog_list.append({'title': title, 'blog': blog})

    # Write saved blog posts to a file.
    with open('posts_catalog.json', 'w') as file:
        json.dump(blog_list, file)

    return flask.redirect(flask.url_for('new_post', pid=pid), code=303)


@app.route('/login', methods=['POST'])
def handle_login():
    # POST request to /login - check user
    login = flask.request.form['user']
    password = flask.request.form['password']
    # try to find user
    if (app.config['ADMIN_PASSWORD'] == password) and (login == 'admin'):
        flask.session['auth_user'] = 'admin'
        return flask.redirect(flask.request.form['url'], 303)

    else:
        return flask.render_template('login.html', state='bad')


@app.route('/logout')
def handle_logout():
    # user wants to say goodbye, just forget about them
    del flask.session['auth_user']
    # redirect to specfied source URL, or / if none is present
    return flask.redirect(flask.request.args.get('url', '/'))


@app.errorhandler(404)
def bad_page(err):
    return flask.render_template('404.html', path=flask.request.path), 404

if __name__ == '__main__':
    app.run()