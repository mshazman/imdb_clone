from app.user import bp
from app.forms import *
from flask import render_template, url_for, flash, redirect, abort
from app.models import *
from app import db
from flask_login import current_user, login_user, logout_user, login_required


@bp.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('index'))
        login_user(user, remember=form.remember_me.data)
        flash("You are successfully login")
        return redirect(url_for('index'))
    return render_template("index.html", form=form)

@bp.route('/logout')
def logout():
    logout_user()
    flash("You are successfully logout")
    return redirect(url_for('index'))


@bp.route('/movie/<movie_id>/rating', methods=['POST', 'GET'])
@login_required
def rating(movie_id):
    movie = Movie.query.filter_by(id=movie_id).first()
    if not movie:
        abort(404)
    else:
        rating_form = UploadRating()
        if rating_form.validate_on_submit():
            rating = Ratings(rating=int(rating_form.rating.data),
                             movie_id=movie_id,
                             user_id=current_user.id,
                             review_text=rating_form.review.data)
            db.session.add(rating)
            db.session.commit()
            flash("Rated Succfully")
            return redirect(url_for('movie.movie', movie_id=movie_id))
        print("Hello", rating_form.errors)
        return redirect(url_for('movie.movie', movie_id=movie_id))


@bp.route('/movie/<movie_id>/rating/edit', methods=['POST', 'GET'])
def edit_rating(movie_id):
    movie = Movie.query.get(movie_id)
    current_user_rating  = movie.get_users_rating(current_user.id)
    rating_form = UploadRating()
    if rating_form.validate_on_submit():
        current_user_rating.rating = rating_form.rating.data
        current_user_rating.review_text = rating_form.review.data
        db.session.commit()
        flash("Your changes has been saved")
        return redirect(url_for('movie.movie', movie_id=movie_id))
    return redirect(url_for('movie.movie', movie_id=movie_id))


@bp.route('/movie/<movie_id>/rating/delete')
def delete_rating(movie_id):
    movie = Movie.query.get(movie_id)
    current_user_rating = movie.get_users_rating(current_user.id)
    db.session.delete(current_user_rating)
    db.session.commit()
    flash("You deleted your review")
    return redirect(url_for('movie.movie', movie_id=movie_id))


@bp.route('/actor/<actor_id>/like', methods=['GET', 'POST'])
def like(actor_id):
    if not Actor.query.get(actor_id).is_liked(current_user.id):
        like = Likes(actor_id=actor_id, user_id=current_user.id)
        db.session.add(like)
        db.session.commit()
        flash("Liked")
    else:
        flash("Already Liked")
    return redirect(url_for('actor.get_actor', actor_id=actor_id))


@bp.route('/actor/<actor_id>/unlike', methods=['GET', 'POST'])
def unlike(actor_id):
    actor = Actor.query.get(actor_id)
    if actor.is_liked(current_user.id):
        like = actor.likes.filter_by(user_id = current_user.id).first()
        db.session.delete(like)
        db.session.commit()
        flash("Unliked")
    else:
        flash("You are not Liking")

    return redirect(url_for('actor.get_actor', actor_id=actor_id))


@bp.route('/profile', methods=['GET', 'POST'])
def profile():
    actor_form = AddActor()
    movie_form = UploadMovie()
    return render_template('admin.html', actor_form=actor_form, movie_form=movie_form)


