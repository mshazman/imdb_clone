from app import app
from app.forms import LoginForm, RegistrationForm, SearchForm
from flask import render_template, url_for, flash, redirect, Response, jsonify
from app.models import *
from app import db
from app import celery
from app.tasks import *


@app.route('/')
@app.route('/index')
def index():
    movie = Movie.query.all()
    login_form = LoginForm()
    signup_form = RegistrationForm()
    search_form = SearchForm()
    return render_template('index.html', movies=movie, login_form=login_form, signup_form=signup_form, search_form=search_form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    signup_form = RegistrationForm()
    login_form = LoginForm()
    if signup_form.validate_on_submit():
        user = User(username=signup_form.username.data, email=signup_form.email.data)
        user.set_password(signup_form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('index'))

    return render_template('index.html', signup_form=signup_form, login_form=login_form)

@app.route('/search', methods=['GET', 'POST'])
def search():
    search_form = SearchForm()
    print(search_form.search_query.data)
    if search_form.validate_on_submit():
        query = search_form.search_query.data
        movies, total = Movie.search(query, 1, 8)
    print(search_form.errors)
    return render_template('search_result.html', movies=movies, total=total, search_form=search_form)


@app.route('/extract/<movie_id>')
def extract(movie_id):
    task = extract_movies.delay([movie_id])
    dic = {}
    dic['id'] = task.id
    # return jsonify(dic)
    flash(f'Task Created...{task.id}')
    return jsonify(dic)
    # return redirect(url_for('index'))

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