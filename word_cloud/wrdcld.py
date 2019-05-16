from werkzeug.exceptions import abort
import spotipy.util as util
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session, current_app
)
from .auth import getplaylist




bp = Blueprint('wrdcld', __name__)


@bp.route('/')
@bp.route('/home')
def home():
    template = "wrdcld/home.html"
    page_name = "Home"
    return render_template(template, name=page_name)

@bp.route('/wordCloud')
def wordCloud():
    """connection to WordCloud class is done here"""
    template = "wrdcld/wrdcld.html"
    page_name = "WordCloud Creation"
    playlist = getplaylist()
    if 'access_token' not in session:
        return redirect('auth.login')
    return render_template(template, name=page_name, playlist=playlist)


@bp.route('/about/')
def about():
    template = "wrdcld/about.html"
    page_name = "About"
    playlist = getplaylist()
    if 'auth_header' in session:
        return render_template(template, name=page_name, playlist=playlist) # if logged in display logged in version of about.html
    else:
        inhere = "in here"
        template = "loggedoutAbout.html"
        return render_template(template, name=page_name, playlist=playlist, state=inhere) # else display logged out version
