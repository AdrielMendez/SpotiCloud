from flask import Blueprint, redirect, render_template, request, url_for, session, flash, jsonify
from .auth import getplaylist
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from .src.SpotifyCloud import SpotifyCloud
import spotipy
import sys
import os

bp = Blueprint('wordcloud', __name__)



@bp.route('/')
@bp.route('/home')
def home():
    template = "home.html"
    domain = "SpotiCloud"
    page_name = "Home"
    img_paths = get_clouds()
    if len(img_paths) > 0:
        return render_template(template, name=page_name, domain=domain, image_url=img_paths[-1])
    if 'access_token' in session:
        page_name = "SpotiCloud"
        return render_template(template, name=page_name, domain=domain)

    return render_template(template, name=page_name, domain=domain)


@bp.route('/wordCloud')
def wordCloud():
    """connection to WordCloud class is done here"""
    template = "home.html"
    domain = "SpotiCloud"
    page_name = "WordCloud Creation"
    if 'access_token' not in session:
        return redirect(url_for('wordcloud.home'))
    else:
        # scheduler job followed by redirect.
        redirect(url_for('wordcloud.about'))
        createWordCloud()
    return render_template(template, name=page_name, domain=domain)


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
        return render_template(template, name=page_name, domain=domain, image_urls=img_paths)


@bp.route("/form", methods=['GET', 'POST'])
def form():
    domain = "SpotiCloud"
    page_name = "Customize your Cloud"
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
            return redirect(url_for('wordcloud.wordCloud'))

        return render_template('form.html', form=form, name=page_name, domain=domain)


def get_clouds():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    dir_path += '/static/uploads'
    imgs = []
    for filename in os.listdir(dir_path):
        imgs.append(filename)
    return imgs


def createWordCloud(data=None):
    token = ''
    sc = SpotifyCloud(number_songs=20)

    if 'form_data' in session and 'access_token' in session:
        data = session['form_data']
        print(data, file=sys.stderr)
        cloud_type = True if data['cloud_type'] == 'lyric' else False
        if data['viewport'] != 'custom':
            sc = SpotifyCloud(theme=data['theme'], viewport=data['viewport'], lyric=cloud_type, background_color=data['background'],
                time_range=data['time_range'], number_songs=data['number_songs'])
        else:
            sc = SpotifyCloud(theme=data['theme'], viewport=data['viewport'], lyric=cloud_type, background_color=data['background'],
                time_range=data['time_range'], number_songs=data['number_songs'], height=int(data['height']), width=int(data['width']))
    if 'access_token' in session:
        token = session['access_token']
    else:
        return redirect(url_for('auth.login'))
    
    if token:

        sp = spotipy.Spotify(auth=token)
    
        tracks = sp.current_user_top_tracks(limit=sc.number_songs, offset=sc.offset, time_range=sc.time_range)['items']
        
        all_lyrics = []
        all_artists = []

        for t in tracks:

            artist_name = t['album']['artists'][0]['name']
            track_name = t['name']
            
            response = sc.request_song_info(track_name, artist_name)
            json = response.json()
            remote_song_info = None

            # Check to see if Genius can find a song with matching artist name and track name.
            for hit in json['response']['hits']: 
                if artist_name.lower() in hit['result']['primary_artist']['name'].lower():
                    remote_song_info = hit
                    break
            
            if sc.lyric:
                # if song info found, collect data.
                if remote_song_info:
                        song_url = remote_song_info['result']['url']
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
    
    if 'form_data' in session:
        session.pop('form_data')

