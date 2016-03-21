from flask import Flask
import flask

app = Flask(__name__)

app.config.from_pyfile('settings.py')

blog_list = []


@app.route('/')
def index():
    return flask.render_template('index.html')

@app.route('/login.html')
def login():
    return flask.render_template('login.html')

@app.route('/posts/<int:pid>')
def new_post(pid):
    #if pid < 0 or pid >= len(posts):
        #flask.abort(404)

    blog_post = blog_list[pid]
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
    blog = flask.request.form['blog']
    pid = len(blog_list)
    blog_list.append({'title': title, 'blog': blog})
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

if __name__ == '__main__':
    app.run()