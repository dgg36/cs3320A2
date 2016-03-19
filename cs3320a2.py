from flask import Flask
import flask

app = Flask(__name__)

app.config.from_pyfile('settings.py')



@app.route('/')
def index():
    return flask.render_template('index.html')

@app.route('/login.html')
def login():
    return flask.render_template('login.html')

@app.route('/new_post.html')
def new_post():
    return flask.render_template('new_post.html')

@app.route('/posts.html')
def posts():
    return flask.render_template('posts.html')

@app.route('/add', methods=['POST'])
def add_animal():
    title = flask.request.form['title']
    blog = flask.request.form['blog']

    return flask.redirect(flask.url_for('posts'), code=303)

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