import functools
import sys
import spotipy
import spotipy.util as util


from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash


bp = Blueprint('auth', __name__)
# , url_prefix='/auth'



@bp.route('/login')
def login():
    template = "auth.html"
    name = "spotify login"
    client_id = "53f83824eefa4ff2ab7f43f2e530ba90"
    spotify_auth_link = "https://accounts.spotify.com/authorize"
    return render_template(template, name=name, auth_link=spotify_auth_link)




def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

