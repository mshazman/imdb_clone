from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from app.search import add_to_index, remove_from_index, query_index
from base64 import b64encode


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class SearchableMixin(object):

    @classmethod
    def search(cls, expression, page, per_page):
        ids, total = query_index(cls.__tablename__, expression, page, per_page)
        if total==0:
            return cls.query.filter_by(id=0), 0
        when = []
        for i in range(len(ids)):
            when.append((ids[i], i))
        return  cls.query.filter(cls.id.in_(ids)).order_by(
            db.case(when, value=cls.id)), total

    @classmethod
    def before_commit(cls, session):
        session._changes = {
            'add': list(session.new),
            'update': list(session.dirty),
            'delete': list(session.deleted)
        }

    @classmethod
    def after_commit(cls, session):
        for obj in session._changes['add']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['update']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['delete']:
            if isinstance(obj, SearchableMixin):
                remove_from_index(obj.__tablename__, obj)
        session._changes = None

    @classmethod
    def reindex(cls):
        for obj in cls.query:
            add_to_index(cls.__tablename__, obj)


db.event.listen(db.session, 'before_commit', SearchableMixin.before_commit)
db.event.listen(db.session, 'after_commit', SearchableMixin.after_commit)


class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    user_type = db.Column(db.String(), default='normal')
    ratings = db.relationship('Ratings', backref='user', lazy='dynamic')
    likes = db.relationship('Likes', backref= 'user')

    def __repr__(self):
        return f'username: {self.username}, email: {self.email}'

    def set_admin(self):
        self.user_type = 'admin'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reviews(self):
        return self.reviews.all()

    def get_likes(self):
        return self.likes.all()

    def is_admin(self):
        return True if self.user_type == 'admin' else False


class Movie(SearchableMixin, db.Model):

    __searchable__ = ['title']
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), unique=True, index=True)
    industry = db.Column(db.String(120), index=True)
    description = db.Column(db.String(1000), index=True)
    writer = db.Column(db.String(120), index=True)
    director = db.Column(db.String(120), index=True)
    storyline = db.Column(db.String(1000), index=True)
    country = db.Column(db.String(120), index=True)
    languages = db.Column(db.String(120), index=True)
    release_date = db.Column(db.DateTime, index=True)
    genres = db.Column(db.String(120), index=True)
    budget = db.Column(db.Integer, index=True)
    box_office_domestic = db.Column(db.Integer, index=True)
    box_office_gross = db.Column(db.Integer, index=True)
    poster = db.Column(db.LargeBinary)
    production_company = db.Column(db.String(120), index=True)
    run_time = db.Column(db.String(120), index=True)
    rating = db.relationship('Ratings', backref='movie', lazy='dynamic')
    cast = db.relationship('Cast', backref='movie', lazy='dynamic')
    youtube = db.Column(db.String(128))

    def __repr__(self):
        return f'Movie Name: {self.title}, industy: {self.industry}'

    def get_rating(self):
        ratings = self.rating.all()
        users_rated = len(ratings)
        if users_rated !=0 :
            sum_of_rating = 0
            for user_rating in ratings:
                sum_of_rating += user_rating.rating

            return (sum_of_rating/users_rated), users_rated
        return 0.0,0

    def get_users_rating(self, user_id):
        return self.rating.filter_by(user_id=user_id).first()

    def get_cast(self):
        return self.cast.all()

    def get_poster(self):
        return b64encode(self.poster).decode("utf-8") if self.poster else self.poster


class Ratings(db.Model):
    rating_id = db.Column(db.Integer, index=True, primary_key=True)
    rating = db.Column(db.Integer, index=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    review_text = db.Column(db.Text)

    def __repr__(self):
        return f' Rating id: {self.rating_id} Rating: {self.rating}'


class Cast(db.Model):

    id = db.Column(db.Integer, index=True, primary_key=True)
    role_name = db.Column(db.String(64), index=True)
    actor_name = db.Column(db.String(64))
    actor_id = db.Column(db.Integer, db.ForeignKey('actor.id'))
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))

    def __repr__(self):

        return f'Role = {self.role_name}, Movie ID: {self.movie_id}'


class Actor(db.Model):

    id = db.Column(db.Integer, index=True, primary_key=True)
    name = db.Column(db.String(64), index=True)
    age = db.Column(db.Integer, index=True)
    birth_place = db.Column(db.String(64), index=True)
    facebook_url = db.Column(db.String(200))
    twitter_url = db.Column(db.String(200))
    insta_url = db.Column(db.String(200))
    bio = db.Column(db.Text)
    birthday = db.Column(db.DateTime)
    nationality = db.Column(db.String(64))
    spouse_name = db.Column(db.String(64))
    father_name = db.Column(db.String(64))
    mother_name = db.Column(db.String(64))
    children = db.Column(db.Integer)
    profile_pic = db.Column(db.LargeBinary)
    movies = db.relationship('Cast', backref='actor', lazy='dynamic')
    likes = db.relationship('Likes', backref='actor', lazy='dynamic')
    awards = db.relationship('Awards', backref='actor', lazy='dynamic')

    def __repr__(self):
        return f'Actor Id: {self.id}, Actor Name: {self.name}'

    def get_likes(self):
        return len(self.likes.all())

    def get_awards(self):
        return self.awards.all()

    def get_movies(self):
        return self.movies.all()

    def is_liked(self, user_id):
        return not self.likes.filter_by(user_id=user_id).first() is None

    def get_profile_pic(self):
        return b64encode(self.profile_pic).decode("utf-8") if self.profile_pic else self.profile_pic


class Likes(db.Model):

    id = db.Column(db.Integer, index=True, primary_key=True)
    actor_id = db.Column(db.Integer, db.ForeignKey('actor.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):

        return f'<Like id: {self.id} Actor id: {self.actor_id} User_id: {self.user_id}>'


class Awards(db.Model):

    id = db.Column(db.Integer, index=True, primary_key=True)
    name = db.Column(db.String(64), index=True)
    year = db.Column(db.String(10), index=True)
    actor_id = db.Column(db.Integer, db.ForeignKey('actor.id'))



