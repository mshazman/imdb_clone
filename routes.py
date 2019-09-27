from app import app
from flask import render_template, url_for, flash, redirect, abort
from app.forms import *
from app.models import *
from app import db
from flask_login import current_user, login_user, logout_user, login_required
from wtforms import ValidationError
from werkzeug.utils import secure_filename
from sqlalchemy import desc




@app.route('/')
@app.route('/index')
def index():
    movie = Movie.query.all()
    # movies = Movie.query.order_by(desc(Movie.get_rating()[0])).all()[:100]
    return render_template('index.html', movies=movie)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        print("hi, Im shazman")
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('registration.html', form=form)


@app.route('/login', methods=['POST', 'GET'])
def login():
    print("hii")
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        print("Button clicked")
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        flash("User Is loginned")
        return redirect(url_for('index'))
    print("Form is not validated", form.errors)
    return render_template("login.html", form=form)

@app.route('/movies', methods=['GET'])
def get_movies():
    data = {}
    movies = Movie.query.all()
    for movie in movies:
        data[movie.id] = {}
        data[movie.id]['title'] = movie.title
        data[movie.id]['link'] = f"{app.config['SERVER_NAME']}/{movie.id}"
    return data


@app.route('/movie', methods=['GET','POST'])
def upload_movie():
    form = UploadMovie()
    try:
        if form.validate_on_submit():
            movie = Movie(title=form.title.data,
                          industry=form.industry.data,
                          description=form.description.data,
                          writer=form.writer.data,
                          director=form.director.data,
                          storyline=form.storyline.data,
                          country=form.country.data,
                          languages=form.languages.data,
                          release_date=form.release_date.data,
                          genres=form.genres.data,
                          budget=form.budget.data,
                          box_office_domestic=form.box_office_domestic.data,
                          box_office_gross=form.box_office_gross.data,
                          production_company=form.production_company.data,
                          run_time=form.run_time.data,
                          youtube=form.youtube_trailer.data)
            db.session.add(movie)
            db.session.commit()
            flash("Movie Added Succefully")
            return redirect(url_for('index'))
    except ValidationError:
        flash(form.error)
    except Exception:
        flash(form.error)
    return render_template('upload_movie.html', form=form)


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
            print("Actor in database", actor)
            cast = Cast(role_name=form.role.data,
                        actor_name= actor_name,
                        actor_id=actor.id,
                        movie_id=movie_id)
            print("Hello")
        else:
            print("Actor not in database", actor)
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
    return render_template('upload.html', form=form, form_name='Add Cast')


@app.route('/movie/<movie_id>/review', methods=['POST', 'GET'])
@login_required
def add_review(movie_id):
    movie = Movie.query.filter_by(id=movie_id).first()
    if not movie:
        return render_template('404.html')
    else:
        review = movie.reviews.filter_by(user_id = current_user.id).first()
        if review:
            flash(review.review_text)
            return redirect(url_for('movie', movie_id=movie_id))
        else:
            form = UploadReview()
            if form.validate_on_submit():
                review = Reviews(review_text=form.review.data,
                                 movie_id=movie_id,
                                 user_id=current_user.id)
                db.session.add(review)
                db.session.commit()
                flash("Review Added Succfully")
                return redirect(url_for('movie', movie_id=movie_id))
            return render_template('upload.html', form=form, form_name='Add Review')


@app.route('/movie/<movie_id>/rating', methods=['POST', 'GET'])
@login_required
def rating(movie_id):
    movie = Movie.query.filter_by(id=movie_id).first()
    if not movie:
        return render_template('404.html')
    else:
        rating = movie.rating.filter_by(user_id = current_user.id).first()
        if rating:
            flash(f'You already have rated this movie {rating.rating}')
            return redirect(url_for('movie', movie_id=movie_id))
        else:
            form = UploadRating()
            if form.validate_on_submit():
                rating = Ratings(rating=int(form.rating.data),
                                 movie_id=movie_id,
                                 user_id=current_user.id)
                db.session.add(rating)
                db.session.commit()
                flash("Rated Succfully")
                return redirect(url_for('movie', movie_id=movie_id))
            return render_template('upload.html', form=form, form_name='Add Review')


@app.route('/movie/<movie_id>', methods=['GET'])
def movie(movie_id):
    movie = Movie.query.get(movie_id)
    if not movie:
        abort(400)
    else:
        return render_template('movie.html', movie=movie)

def admin_required(fun):

    def inner():
        if current_user.is_admin():
            fun()
        else:
            abort(401)
    return inner

@app.route('/actor', methods=['GET', 'POST'])
@admin_required
def add_actor():
    form = AddActor()
    if form.validate_on_submit():
        actor = Actor(name=form.name.data,
                      age= form.age.data,
                      birth_place=form.birth_place.data,
                      facebook_url=form.facebook_url.data,
                      twitter_url=form.twitter_url.data,
                      insta_url=form.insta_url.data,
                      bio=form.bio.data,
                      birthday=form.birthday.data,
                      nationality=form.nationality.data,
                      spouse_name=form.spouse_name.data,
                      father_name=form.father_name.data,
                      mother_name=form.mother_name.data,
                      children=form.children.data
                      )
        db.session.add(actor)
        db.session.commit()
        actor_id = Actor.query.filter_by(name=form.name.data).all()[-1]
        name = 'actor' + str(actor_id) + '.jpg'
        flash("Actor Added Successfully")
        return redirect(url_for('index'))
    return render_template('upload.html', form=form, form_name='Add Actor')


@app.route('/actor/<actor_id>', methods=['GET'])
def get_actor(actor_id):
    actor = Actor.query.get(actor_id)
    if actor is None:
        abort(404)
    else:
        return render_template('actor.html', actor=actor)


@app.route('/actor/<actor_id>/like', methods=['GET', 'POST'])
def like(actor_id):
    if not Actor.query.get(actor_id).is_liked(current_user.id):
        like = Likes(actor_id=actor_id, user_id=current_user.id)
        db.session.add(like)
        db.session.commit()
        flash("Liked")
    else:
        flash("Already Liked")
    return redirect(url_for('get_actor', actor_id=actor_id))


@app.route('/actor/<actor_id>/unlike', methods=['GET', 'POST'])
def unlike(actor_id):
    actor = Actor.query.get(actor_id)
    if actor.is_liked(current_user.id):
        like = actor.likes.filter_by(user_id = current_user.id).first()
        db.session.delete(like)
        db.session.commit()
        flash("Unliked")
    else:
        flash("You are not Liking")

    return redirect(url_for('get_actor', actor_id=actor_id))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


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

    return render_template('edit_movie.html', form=form, form_name="Edit Movie", movie=movie)


@app.route('/movie/<movie_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_movie(movie_id):
    if not current_user.is_admin():
        abort(401)
    movie = Movie.query.get(movie_id)
    db.session.delete(movie)
    flash("Movie Deleted")
    return redirect('index')