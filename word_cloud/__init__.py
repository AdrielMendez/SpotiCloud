import os
import spotipy
from flask import Flask, g
from flask_bootstrap import Bootstrap
from celery import Celery
from .tasks.celery_config import celery_app

# celery = Celery(__name__)
# celery.config_from_object('tasks.celery_config')

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    Bootstrap(app)
    app.config.from_mapping(SECRET_KEY='dev',)
    app.config['CELERY_BROKER_URL'] = 'amqp://localhost/'
    app.config['CELERY_BACKEND'] = 'rpc://'

    ctx = app.app_context()
    ctx.push()

    from . import auth
    app.register_blueprint(auth.bp)

    from . import wordcloud
    app.register_blueprint(wordcloud.bp)
    

    app.app_context().push()
    
    return app