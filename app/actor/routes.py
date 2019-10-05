from app.actor import bp
from app.forms import LoginForm, RegistrationForm, AddAward, EditActor,AddActor, UploadMovie
from flask import render_template, url_for, flash, redirect, abort
from app.models import *
from app import db
from flask_login import current_user, login_required
from base64 import b64encode


@bp.route('/actors', methods=['GET'])
def actors():
    actors = Actor.query.all()
    login_form = LoginForm()
    signup_form = RegistrationForm()
    return render_template('actors.html', title='Actors', actors=actors, login_form=login_form, signup_form=signup_form)


@bp.route('/actor/<actor_id>', methods=['GET'])
def get_actor(actor_id):
    login_form =LoginForm()
    signup_form = RegistrationForm()
    add_award = AddAward()
    edit_actor_form = EditActor()
    actor = Actor.query.get(actor_id)
    if not actor.profile_pic is None:
        profile_pic = b64encode(actor.profile_pic).decode("utf-8")
    else:
        profile_pic = actor.profile_pic
    if actor is None:
        abort(404)
    else:
        return render_template('actor.html', edit_actor_form=edit_actor_form, add_award=add_award, actor=actor, login_form=login_form, signup_form=signup_form, profile_pic=profile_pic)


@bp.route('/actor', methods=['GET', 'POST'])
@login_required
def add_actor():
    if not current_user.is_admin():
        abort(401)
    actor_form = AddActor()
    movie_form = UploadMovie()

    if actor_form.validate_on_submit():
        if actor_form.profile_img is None:
            profile_pic = actor_form.profile_img.data.read()
        else:
            profile_pic = actor_form.profile_img.data
        actor = Actor(name=actor_form.name.data,
                      age= actor_form.age.data,
                      birth_place=actor_form.birth_place.data,
                      facebook_url=actor_form.facebook_url.data,
                      twitter_url=actor_form.twitter_url.data,
                      insta_url=actor_form.insta_url.data,
                      bio=actor_form.bio.data,
                      birthday=actor_form.birthday.data,
                      nationality=actor_form.nationality.data,
                      spouse_name=actor_form.spouse_name.data,
                      father_name=actor_form.father_name.data,
                      mother_name=actor_form.mother_name.data,
                      children=actor_form.children.data,
                      profile_pic=profile_pic
                      )
        db.session.add(actor)
        db.session.commit()
        flash("Actor Added Successfully")
        return redirect(url_for('admin'))
    print(actor_form.errors)
    return render_template('admin.html', actor_form=actor_form, movie_form=movie_form)


@bp.route('/actor/<actor_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_actor(actor_id):
    if not current_user.is_admin():
        abort(401)
    actor = Actor.query.get(actor_id)
    db.session.delete(actor)
    db.session.commit()
    flash("Actor Deleted")
    return redirect(url_for('admin'))

@bp.route('/actor/<actor_id>/award', methods=['GET', 'POST'])
def add_award(actor_id):
    actor = Actor.query.filter_by(id=actor_id).first()
    if not actor:
        return render_template('404.html')
    add_award = AddAward()
    if add_award.validate_on_submit():
        award = Awards(name=add_award.name.data,
                       year=add_award.year.data,
                        actor_id=actor_id)
        db.session.add(award)
        db.session.commit()
        flash("Award Added Successfully")
        return redirect(url_for('get_actor', actor_id=actor_id))
    return redirect(url_for('get_actor', actor_id=actor_id))


@bp.route('/actor/<actor_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_actor(actor_id):
    if not current_user.is_admin():
        abort(401)
    actor = Movie.query.get(actor_id)
    edit_actor_form = EditActor()
    if edit_actor_form.validate_on_submit():
        actor.name = edit_actor_form.name.data
        actor.age = edit_actor_form.age.data
        actor.bio = edit_actor_form.bio.data
        actor.birth_place = edit_actor_form.birth_place.data
        actor.facebook_url = edit_actor_form.facebook_url.data
        actor.twitter_url = edit_actor_form.twitter_url.data
        actor.insta_url = edit_actor_form.insta_url.data
        actor.nationality = edit_actor_form.nationality.data
        actor.spouse_name = edit_actor_form.spouse_name.data
        actor.father_name = edit_actor_form.father_name.data
        actor.mother_name =edit_actor_form.mother_name.data
        actor.children = edit_actor_form.children.data

        db.session.commit()
        flash("Your Changes have been Saved")

        return redirect(url_for('get_actor', actor_id=actor_id))
        return redirect(url_for('get_actor', actor_id=actor_id))

    return redirect(url_for('get_actor', actor_id=actor_id))