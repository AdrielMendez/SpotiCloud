from flask import Blueprint, redirect, render_template, request, url_for, session, flash, jsonify
from .auth import getplaylist
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from .src.SpotifyCloud import SpotifyCloud
import spotipy

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
    else:
        createWordCloud()
    return render_template(template, name=page_name)


@bp.route('/about/')
def about():
    template = "about.html"
    page_name = "About"
    return render_template(template, name=page_name)
<<<<<<< HEAD
=======

def createWordCloud():
    
    sc = SpotifyCloud(number_songs=10, time_range='long_term', offset=0,
        lyric=True, height=1792, width=828, max_words=250,
        max_font_size=350, theme='kay', viewport='custom', min_font_size=12, background_color='lightblue')
    
    token = ''

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
>>>>>>> 188d26b338d73509593bf11fd6f93ab3efc8ee51
