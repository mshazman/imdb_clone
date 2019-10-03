from app import app
from app.forms import LoginForm, RegistrationForm, SearchForm
from flask import render_template, url_for, flash, redirect
from app.models import *
from app import db


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




