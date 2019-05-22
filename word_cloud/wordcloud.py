from flask import Blueprint, redirect, render_template, request, url_for, session, flash, jsonify
from .auth import getplaylist
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField


bp = Blueprint('wordcloud', __name__)


@bp.route("/form", methods=['GET', 'POST'])
def form():
    header = "SpotiCloud Form"
    if request.method == 'POST':
        data = {}
        data['theme'] = request.form.get('theme') 
        data['background'] = request.form.get('background')
        data['cloud_type'] = request.form.get('type')
        data['viewport'] = request.form.get('viewport')
        return jsonify(data)
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
    return render_template(template, name=page_name)
