from flask import Blueprint, redirect, render_template, request, url_for, session, flash
from .auth import getplaylist
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField


bp = Blueprint('wordcloud', __name__)


class ReusableForm(Form):
    name = TextField('Name:', validators=[validators.required()])
    email = TextField('Email:', validators=[validators.required(), validators.Length(min=6, max=35)])
    password = TextField('Password:', validators=[validators.required(), validators.Length(min=3, max=35)])
    
    @bp.route("/form", methods=['GET', 'POST'])
    def hello():
        form = ReusableForm(request.form)
        header = "SpotiCloud Form"
        print(form.errors)
        if request.method == 'POST':
            name=request.form['name']
            password=request.form['password']
            email=request.form['email']
            print(name, " ", email, " ", password)
    
        if form.validate():
        # Save the comment here.
            flash('Thanks for registration ' + name)
        else:
            flash('Error: All the form fields are required. ')
    
        return render_template('form.html', form=form, name=header)


@bp.route('/')
@bp.route('/home')
def home():
    template = "home.html"
    page_name = "Home"
    return render_template(template, name=page_name)


@bp.route('/wordCloud')
def wordCloud():
    """connection to WordCloud class is done here"""
    template = "home.html"
    page_name = "WordCloud Creation"
    if 'access_token' not in session:
        return redirect('auth.login')
    return render_template(template, name=page_name)


@bp.route('/about/')
def about():
    template = "about.html"
    page_name = "About"
    playlist = getplaylist()
    return render_template(template, name=page_name, playlist=playlist)
