from app import app
from flask import render_template, url_for, flash, redirect, abort
from app.forms import *
from app.models import *
from app import db
from flask_login import current_user, login_user, logout_user, login_required
from wtforms import ValidationError
from werkzeug.utils import secure_filename
from sqlalchemy import desc


@app.route('/movie', methods=['GET','POST'])
def add_movie():
    movie_form = UploadMovie()
    # try:
    if movie_form.validate_on_submit():
        movie = Movie(title=movie_form.title.data,
                      industry=movie_form.industry.data,
                      description=movie_form.description.data,
                      writer=movie_form.writer.data,
                      director=movie_form.director.data,
                      storyline=movie_form.storyline.data,
                      country=movie_form.country.data,
                      languages=movie_form.languages.data,
                      release_date=movie_form.release_date.data,
                      genres=movie_form.genres.data,
                      budget=movie_form.budget.data,
                      box_office_domestic=movie_form.box_office_domestic.data,
                      box_office_gross=movie_form.box_office_gross.data,
                      production_company=movie_form.production_company.data,
                      run_time=movie_form.run_time.data,
                      youtube=movie_form.youtube_trailer.data)
        db.session.add(movie)
        db.session.commit()
        flash("Movie Added Succefully")
        return redirect(url_for('index'))
    print(movie_form.release_date.data)
    print(movie_form.errors)
    flash("Please fill all mandatory fields", movie_form.errors)

    return redirect(url_for('admin'))


@app.route('/movie/<movie_id>/cast', methods=['GET', 'POST'])
def add_cast(movie_id):
    movie = Movie.query.filter_by(id=movie_id).first()
    if not movie:
        return render_template('404.html')
    form = UploadCast()
    # try:
    if form.validate_on_submit():
        actor_name = form.actor_name.data
        actor = Actor.query.filter_by(name=actor_name).first()
        if actor:
            cast = Cast(role_name=form.role.data,
                        actor_name= actor_name,
                        actor_id=actor.id,
                        movie_id=movie_id)
        else:
            cast = Cast(role_name=form.role.data,
                        actor_name=actor_name,
                        movie_id=movie_id)
        print("Cast after: ", cast)
        db.session.add(cast)
        db.session.commit()
        flash(f'{actor_name} Added Succefully')
        return redirect(url_for('index'))
    # except Exception:
    #     flash("Error Occured, Cast not Added")
    #     return redirect(url_for('index'))
    return redirect(url_for('movie', movie_id))

@app.route('/movie/<movie_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_movie(movie_id):
    if not current_user.is_admin():
        abort(401)
    movie = Movie.query.get(movie_id)
    form = EditMovie()
    if form.validate_on_submit():
        movie.title = form.title.data
        movie.industry = form.industry.data
        movie.description =form.description.data
        movie.writer = form.writer.data
        movie.director = form.director.data
        movie.storyline = form.storyline.data
        movie.country = form.country.data
        movie.languages = form.languages.data
        movie.genres = form.genres.data
        movie.budget = form.budget.data
        movie.box_office_domestic =form.box_office_domestic.data
        movie.box_office_gross = form.box_office_gross.data
        movie.production_company = form.production_company.data
        movie.run_time= form.run_time.data
        movie.youtube = form.youtube_trailer.data

        db.session.commit()
        flash("Your Changes have been Saved")

        return redirect(url_for('movie', movie_id=movie_id))

    return redirect(url_for('movie', movie_id))


@app.route('/movie/<movie_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_movie(movie_id):
    if not current_user.is_admin():
        abort(401)
    movie = Movie.query.get(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash("Movie Deleted")
    return redirect(url_for('admin'))


@app.route('/movies', methods=['GET'])
def movies():
    # data = {}
    movies = Movie.query.all()
    login_form = LoginForm()
    signup_form = RegistrationForm()
    # for movie in movies:
    #     data[movie.id] = {}
    #     data[movie.id]['title'] = movie.title
    #     data[movie.id]['link'] = f"{app.config['SERVER_NAME']}/{movie.id}"
    return render_template('movies.html', movies=movies, title='Movies', login_form=login_form, signup_form=signup_form)

@app.route('/movie/<movie_id>', methods=['GET'])
def movie(movie_id):
    cast_form = UploadCast()
    login_form = LoginForm()
    signup_form = RegistrationForm()
    edit_movie_form = EditMovie()
    movie = Movie.query.get(movie_id)
    rating_form = UploadRating()
    if not movie:
        abort(400)
    else:
        return render_template('movie.html', movie=movie, rating_form=rating_form, cast_form=cast_form, login_form=login_form, signup_form=signup_form, edit_movie_form=edit_movie_form)

