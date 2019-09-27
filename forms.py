from flask_wtf import FlaskForm
from wtforms import FileField, TextAreaField, DateField, TextField, StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Email, ValidationError
from flask_wtf.file import FileField, FileAllowed
from app.models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):

    username = StringField('Username: ', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    # password2 = PasswordField(
    #     'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class UploadMovie(FlaskForm):

    title = StringField('Title')
    industry = StringField('Industry')
    description = TextField('Bio')
    writer = StringField('Writers')
    director = StringField('Director')
    storyline = TextField('Storyline')
    country = StringField('Origin Country')
    languages = StringField('Languages')
    release_date = DateField('Release Date',format='%d/%m/%Y')
    genres = StringField('Genres')
    budget = StringField('Budget')
    box_office_domestic = StringField('Box Office Domestic')
    box_office_gross = StringField('Box Office Gross')
    production_company = StringField('Production Company')
    run_time = StringField('Run Time')
    youtube_trailer = StringField('Youtube Trailer')
    submit = SubmitField('Add Movie')


class UploadCast(FlaskForm):
    role = StringField('Role')
    actor_name = StringField('Actor Name')
    submit = SubmitField('Add Cast')


class UploadReview(FlaskForm):
    review = TextAreaField('Review')
    submit = SubmitField('Post Review')


class UploadRating(FlaskForm):
    rating = StringField('Rating')
    submit = SubmitField('Rate')


class AddActor(FlaskForm):
    name = StringField('Name')
    age = StringField('Age: ')
    birth_place = StringField('Birth Place')
    facebook_url = StringField('Facebook Profile')
    twitter_url = StringField('Twitter Profile')
    insta_url = StringField('Instagram Profile')
    bio = StringField('Bio')
    birthday = DateField('Birthday', format = '%d/%m/%Y' )
    nationality = StringField('Nationality')
    spouse_name = StringField('Spouse Name')
    father_name = StringField('Father Name')
    mother_name = StringField('Mother Name')
    children = StringField('Children')
    profile_img = FileField(label="Profile Image", validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Image Only!')])
    submit = SubmitField()


class EditMovie(FlaskForm):

    title = StringField('Title')
    industry = StringField('Industry')
    description = TextField('Bio')
    writer = StringField('Writers')
    director = StringField('Director')
    storyline = TextField('Storyline')
    country = StringField('Origin Country')
    languages = StringField('Languages')
    genres = StringField('Genres')
    budget = StringField('Budget')
    box_office_domestic = StringField('Box Office Domestic')
    box_office_gross = StringField('Box Office Gross')
    production_company = StringField('Production Company')
    run_time = StringField('Run Time')
    youtube_trailer = StringField('Youtube Trailer')
    submit = SubmitField('Edit')

