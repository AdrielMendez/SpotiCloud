from flask import Blueprint, redirect, render_template, request, url_for, session
from .auth import getplaylist


bp = Blueprint('wordcloud', __name__)


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
