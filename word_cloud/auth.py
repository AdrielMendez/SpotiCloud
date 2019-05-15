import functools
import sys
import spotipy
import spotipy.util as util
from urllib.parse import quote

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash


bp = Blueprint('auth', __name__)
# , url_prefix='/auth'


auth_query_parameters = {
    "response_type": "code",
    "redirect_uri": 'http://localhost/',
    "scope": 'user-top-read',
    # "state": STATE,
    # "show_dialog": SHOW_DIALOG_str,
    "client_id": ''
}


@bp.route("/login")
def login():
    # Auth Step 1: Authorization
    name = "buttcheeks"
    url_args = "&".join(["{}={}".format(key, quote(val)) for key, val in auth_query_parameters.items()])
    auth_url = "{}/?{}".format("https://accounts.spotify.com/authorize", url_args)
    return render_template('auth.html', spot_link=auth_url, name=name)



# @bp.route('/login')
# def login():
#     template = "auth.html"
#     name = "spotify login"
#     client_id = "53f83824eefa4ff2ab7f43f2e530ba90"
#     spotify_auth_link = "https://accounts.spotify.com/authorize"
#     return render_template(template, name=name, auth_link=spotify_auth_link)




def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

