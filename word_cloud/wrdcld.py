from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort


bp = Blueprint('wrdcld', __name__)


@bp.route('/')
def home(page_name=None):
    template = "wrdcld.html"
    page_name = "Home"
    return render_template(template, name=page_name)

@bp.route('/wordCloud')
def wordCloud():
    template = "wrdcld.html"
    page_name = "WordCloud Creation"
    return render_template(template, name=page_name)


@bp.route('/about/')
def about(page_name=None):
    template = "about.html"
    page_name = "About"
    return render_template(template, name=page_name)
