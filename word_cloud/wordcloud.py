from flask import (Blueprint, redirect, render_template, request, 
                    url_for, session, flash, jsonify, g, current_app,)
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from .src.SpotifyCloud import SpotifyCloud
from celery.result import AsyncResult
from word_cloud import celery_app
import requests
import spotipy
import sys
import os
from time import sleep
from pprint import pprint


bp = Blueprint('wordcloud', __name__)
task_id = 0

""" 
            ##############
            # \/routes\/ #
            ##############
"""

@bp.route('/')
@bp.route('/home')
def home():
    from word_cloud.tasks.tasks import run_createWordCloud
    template = "home.html"
    domain = "SpotiCloud"
    name = "SpotiCloud"
    img_path = get_clouds()
    gallery_imgs = get_gallery_imgs()
    if 'access_token' in session:
        if 'task_complete' in session:
            session.pop('task_complete')
            session.pop('task_id')
            return render_template(template, image_url=img_path, gallery_imgs=gallery_imgs, img_path=img_path)
        else:
            return render_template(template, gallery_imgs=gallery_imgs, img_path=img_path)
    else:
        page_name = "Home"
        return render_template(template, gallery_imgs=gallery_imgs, img_path=img_path)


@bp.route('/wordCloud', methods=['GET', 'POST'])
def wordCloud():
    from word_cloud.tasks.tasks import run_createWordCloud
    """connection to WordCloud class is done here"""
    template = "home.html"
    domain = "SpotiCloud"
    page_name = "WordCloud Creation"

    if 'access_token' not in session:
        return redirect(url_for('wordcloud.home'))
    else:
        global task_id
        task_id += 1  
        referrer = request.referrer
        info = get_form_data(referrer)
        result = run_createWordCloud.apply_async((info,), task_id='wc{}'.format(task_id))
        session['new_cloud'] = 'in session'
        session['task_id'] = result.task_id
    
        return_name = request.referrer.split('/')[-1] + '.html'
        if return_name == 'wordCloud.html':
            return_name = 'home.html'
        return render_template(return_name) 
    

@bp.route('/about/')
def about():
    template = "about.html"
    domain = "SpotiCloud"
    page_name = "About"
    return render_template(template, name=page_name, domain=domain)
    

@bp.route('/clouds/')
def clouds():
    template="clouds.html"
    domain = "SpotiCloud"
    page_name = "Generated Clouds" 

    if 'access_token' not in session:
        return redirect(url_for('auth.login'))
    else: 
        img_paths = get_clouds()
        img_paths.reverse()
        return render_template(template, name=page_name, domain=domain, image_urls=img_paths)


@bp.route("/form", methods=['GET', 'POST'])
def form():
    domain = "SpotiCloud"
    page_name = "Customize your Cloud"
    return_name = request.referrer.split('/')[-1] + '.html'

    if 'access_token' not in session:
        return redirect(url_for('auth.login'))
    else:

        if request.method == 'POST':
            data = {}
            data['theme'] = request.form.get('theme') 
            data['background'] = request.form.get('background')
            data['cloud_type'] = request.form.get('type')
            data['viewport'] = request.form.get('viewport')
            data['number_songs'] = request.form.get('number_songs')
            data['time_range'] = request.form.get('time_range')

            if data['viewport'] == 'custom':
                data['height'] = request.form.get('height')
                data['width'] = request.form.get('width')
            session['form_data'] = dict(data)
            print('inside form()******')
            return jsonify({'form_data': render_template('form.html', form=form)})
        print('+~+~+~+~++~+~ didn\'t post~+~++~+~+~+~+~+')
        return render_template('form.html', form=form, name=page_name, domain=domain)


@bp.route('/cloud_task/', methods=['GET', 'POST'])
def cloud_task():
    from word_cloud.tasks.tasks import run_createWordCloud
    global task_id
    task_id += 1  
    referrer = request.referrer
    info = get_form_data(referrer)
    print('inside cloud_task()+++++')
    result = run_createWordCloud.apply_async((info,), task_id='wc{}'.format(task_id))
    session['new_cloud'] = 'in session'
    session['task_id'] = result.task_id
    while not result.ready():
        sleep(1)
    referrer_html = result.result
    all_clouds = get_clouds()
    new_cloud = str(all_clouds[-1])
    payload = { 'data': render_template('overlay.html', new_cloud=new_cloud)}
    if 'form_data' in session:
        session.pop('form_data')
    return jsonify(payload)


""" 
            ###############
            # \/Methods\/ #
            ###############
"""  

def get_clouds():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    dir_path += '/static/uploads'
    imgs = []
    for filename in os.listdir(dir_path):
        if filename.lower().endswith('.png'):
            imgs.append(filename)
    imgs.sort()
    return imgs

def get_gallery_imgs():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    dir_path += '/static/gallery'
    imgs = []
    for filename in os.listdir(dir_path):
        if filename.lower().endswith('.png'):
            imgs.append(filename)
    return imgs


def get_form_data(referrer):
    from .auth import is_token_expired, renew_access_token
    result = {}
    return_name = referrer.split('/')[-1] + ".html"
    result['return_name'] = return_name
    if is_token_expired:
        renew_access_token()
        if 'form_data' in session:
            result['form_data'] = session['form_data']
        if 'access_token' in session:
            result['access_token'] = session['access_token']
        return result
    else:
        if 'form_data' in session:
            result['form_data'] = session['form_data']
        if 'access_token' in session:
            result['access_token'] = session['access_token']
        return result


def run_word_cloud(task_data):
    print('Fetching wordCloud')
    token = ''
    sc = SpotifyCloud(number_songs=20)

    if 'form_data' in task_data and 'access_token' in task_data:
        print("inside the custom form if-statement")
        data = task_data['form_data']
        print(data, file=sys.stderr)
        cloud_type = True if data['cloud_type'] == 'lyric' else False
        if data['viewport'] != 'custom':
            sc = SpotifyCloud(theme=data['theme'], viewport=data['viewport'], lyric=cloud_type, background_color=data['background'],
                time_range=data['time_range'], number_songs=data['number_songs'])
        else:
            sc = SpotifyCloud(theme=data['theme'], viewport=data['viewport'], lyric=cloud_type, background_color=data['background'],
                time_range=data['time_range'], number_songs=data['number_songs'], height=int(data['height']), width=int(data['width']))
        token = task_data['access_token']
    elif 'access_token' in task_data:
        print('inside the randomly generated word cloud if statement +!+!+!+!')
        data = sc.generateRandomAttributes()
        sc = SpotifyCloud(theme=data['theme'], viewport=data['viewport'], background_color=data['background'],
            time_range=data['time_range'], number_songs=data['number_songs'], lyric=data['lyric'])
        token = task_data['access_token']
    else:
        return "not working right now sorry"
        # return redirect(url_for('auth.login'))
    total = 0
    if token:

        sp = spotipy.Spotify(auth=token)
    
        tracks = sp.current_user_top_tracks(limit=sc.number_songs, offset=sc.offset, time_range=sc.time_range)['items']
        
        all_lyrics = []
        all_artists = []

        for t in tracks:

            artist_name = t['album']['artists'][0]['name']
            track_name = t['name']
            

            remote_song_info = sc.request_song_info(track_name, artist_name)

            total += 1

            if sc.lyric:
                # if song info found, collect data.
                if remote_song_info:
                        song_url = remote_song_info['url']
                        lyrics = sc.scrap_song_url(song_url)
                        all_lyrics.append(lyrics)
            else:
                all_artists.append(artist_name)
    
        temp_list = []
        if sc.lyric:
            for i in all_lyrics:
                temp_list.append(''.join(i))
            with open("Lyrics.txt", "w") as text_file:
                text_file.write(' '.join(temp_list))
            sc.createWordCloud("Lyrics.txt")
        else:
            for i in all_artists:
                temp_list.append(''.join(i))
            with open("Artists.txt", "w") as artist_file:
                artist_file.write(' '.join(temp_list))
            sc.createWordCloud("Artists.txt")
    
    print('word Cloud Function finished')
    

    # return_name =  info['return_name']
    # return return_name
