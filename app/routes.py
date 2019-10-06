from app import app
from app.forms import LoginForm, RegistrationForm, SearchForm
from flask import render_template, url_for, flash, redirect, Response, jsonify, g
from app.models import *
from app import db
from flask_login import current_user
from app.tasks import *


@app.before_request
def before_request():
    g.search_form = SearchForm()
    if current_user.is_anonymous:
        g.login_form = LoginForm()
        g.signup_form = RegistrationForm()


@app.route('/')
@app.route('/index')
def index():
    movie = Movie.query.all()
    return render_template('index.html', movies=movie)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    g.signup_form = RegistrationForm()
    if g.signup_form.validate_on_submit():
        user = User(username=g.signup_form.username.data, email=g.signup_form.email.data)
        user.set_password(g.signup_form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('index'))
    return render_template('index.html')


@app.route('/search', methods=['GET', 'POST'])
def search():
    if g.search_form.validate_on_submit():
        query = g.search_form.search_query.data
        movies, total = Movie.search(query, 1, 8)
    print(g.search_form.errors)
    return render_template('search_result.html', movies=movies, total=total)


@app.route('/extract/<movie_id>')
def extract(movie_id):
    task = extract_movies.delay([movie_id])
    dic = {}
    dic['id'] = task.id
    return jsonify(dic)


@app.route('/task/status/<task_id>')
def status(task_id):
    status = task_status(task_id)
    return jsonify(status)


@app.route('/task/result/<task_id>')
def result(task_id):
    task = celery.AsyncResult(task_id)
    print(task.state)
    if task.state=='PENDING':
        return "Task is Being Executed"
    elif task.state=='SUCCESS':
        path = './app/files/'+ task.result
        with open(path, 'r') as file:
            return Response(file.read(),
                            mimetype="json",
                            headers={"Content-disposition":
                            "attachment; filename="+task.result})
    else:
        return task.info
    return "Some Error"