import textbase
from textbase.message import Message
from textbase import models
import os
from typing import List
from dotenv import load_dotenv
load_dotenv() 
import openai
import requests

# API KEYS
MY_API_KEY = os.environ['MY_API_KEY']
WEATHER_API_KEY = os.environ['WEATHER_API']
URL_SHORTENER = os.environ['URL_SHORTENER']
TRANSLATE_API_KEY = os.environ['TRANSLATE_API_KEY']
HOLIDAYS_API_KEY = os.environ['HOLIDAYS_API_KEY']
MEME_API_KEY = os.environ['MEME_API_KEY']
JOKES_API_KEY = os.environ['JOKES_API_KEY']
SONGS_API_KEY = os.environ['SONGS_API_KEY']

# Load your OpenAI API key
models.OpenAI.api_key =MY_API_KEY
# or from environment variable:
# models.OpenAI.api_key = os.getenv("OPENAI_API_KEY")

# Prompt for GPT-3.5 Turbo
SYSTEM_PROMPT = """You are chatting with an AI. There are no specific prefixes for responses, so you can ask or talk about anything you like. The AI will respond in a natural, conversational manner. Feel free to start the conversation with any question or topic, and let's have a pleasant chat!
"""

MY_USERNAME = os.environ['MY_USERNAME']
CONTESTS_API_KEY = os.environ['CONTESTS_API_KEY']


def get_contest():
    response = requests.get(f"https://clist.by/api/v1/contest/?username={MY_USERNAME}&api_key={CONTESTS_API_KEY}")
    print(response);
    return response;

def get_translate(text):
    url = "https://google-translate1.p.rapidapi.com/language/translate/v2"

    payload = {
        "q": text,
        "target": "hi",
        "source": "en"
    }
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "Accept-Encoding": "application/gzip",
        "X-RapidAPI-Key": TRANSLATE_API_KEY,
        "X-RapidAPI-Host": "google-translate1.p.rapidapi.com"
    }

    response = requests.post(url, data=payload, headers=headers)
    data = response.json();
    translated_text = data['data']['translations'][0]['translatedText']
    return translated_text


def get_urlshorten(long_url):
    try:
        url = "https://url-shortener-service.p.rapidapi.com/shorten"

        payload = { "url":long_url }
        headers = {
            "content-type": "application/x-www-form-urlencoded",
            "X-RapidAPI-Key": URL_SHORTENER,
            "X-RapidAPI-Host": "url-shortener-service.p.rapidapi.com"
        }

        response = requests.post(url, data=payload, headers=headers)
        res = response.json();
        return "Here is your shorten URL: " + res["result_url"];
    except :
        return "Please re-enter your URL with along with http"


def get_memes():
    
    url = "https://reddit-meme.p.rapidapi.com/memes/top"

    headers = {
        "X-RapidAPI-Key": MEME_API_KEY,
        "X-RapidAPI-Host": "reddit-meme.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    title = data[0]['title']
    url = data[0]['url']
    return "<img src="+url+"/>\n"+title;

def get_joke():
    
    url = "https://jokes-by-api-ninjas.p.rapidapi.com/v1/jokes"

    headers = {
        "X-RapidAPI-Key": JOKES_API_KEY,
        "X-RapidAPI-Host": "jokes-by-api-ninjas.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers).json()
    data = response[0]['joke']
    print(response)
    return data
    
def download_song():
    
    url = "https://spotify-downloader1.p.rapidapi.com/download/22LAwLoDA5b4AaGSkg6bKW"

    headers = {
        "X-RapidAPI-Key": SONGS_API_KEY,
        "X-RapidAPI-Host": "spotify-downloader1.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)
    data = response.json()
    song_link = data['link']
    image_url = data['metadata']['cover']
    artists = data['metadata']['artists']
    song_title = data['metadata']['title']
    return f"""<strong>{song_title}</strong><br>
    <strong>Artist: {artists}</strong>
    <img src="{image_url}" alt="{song_title} cover" width="200">
    <audio controls>
        <source src="{song_link}" type="audio/mpeg">
        Your browser does not support the audio element.
    </audio>""";

def song_playlist():
    url = "https://spotify-downloader1.p.rapidapi.com/trackList/playlist/37i9dQZF1DX0XUsuxWHRQd"

    headers = {
        "X-RapidAPI-Key": SONGS_API_KEY,
        "X-RapidAPI-Host": "spotify-downloader1.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)
    data = response.json()
    print(data)
    result = "<ul>"
    for track in data['trackList']:
        title = track['title']
        artists = track['artists']
        cover_url = track['cover']
        album = track['album']
        release_date = track['releaseDate']

        result += f"""
            <li>
                <strong>Title:</strong> {title}<br>
                <strong>Artists:</strong> {artists}<br>
                <strong>Album:</strong> {album}<br>
                <strong>Release Date:</strong> {release_date}<br>
                <img src="{cover_url}" alt="{title} - {artists}" height="100" width="100">
            </li>
        """

    result += "</ul>"
    return result
    
def get_holidays():


    url = "https://working-days.p.rapidapi.com/1.3/analyse"

    querystring = {"start_date":"2013-01-01","end_date":"2013-12-31","country_code":"IN","end_time":"18:15","start_time":"09:14"}

    headers = {
        "X-RapidAPI-Key": HOLIDAYS_API_KEY,
        "X-RapidAPI-Host": "working-days.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()

    public_holidays = data.get('public_holidays', {}).get('list', [])

    result_string = "<strong>Indian Public Holiday Days📍</strong>\n"
    result_string += "<ul>\n---------------\n"
    for holiday in public_holidays:
        description = holiday.get('description', 'N/A')
        date = holiday.get('date', 'N/A');
        date_parts = date.split('-')
        reversed_date_parts = date_parts[::-1]
        reversed_date = '-'.join(reversed_date_parts)
        result_string += f"<li><strong>{description}:</strong> <em>{reversed_date}</em></li>\n"
    result_string += "</ul>"


    return result_string
    
@textbase.chatbot("talking-bot")
def on_message(message_history: List[Message], state: dict = None):
    """Your chatbot logic here
    message_history: List of user messages
    state: A dictionary to store any stateful information

    Return a string with the bot_response or a tuple of (bot_response: str, new_state: dict)
    """
    if state is None or "counter" not in state:
        state = {"counter": 0}
    else:
        state["counter"] += 1

    # Get the latest user message
    user_message = message_history[-1].content.lower()

    if user_message.startswith("hi"):
        bot_response = "Hello 😁! How can I assist you? Type start to look for all the commands"
        
    elif user_message.startswith("start"):
        bot_response = """
        <p><strong>Here are some of the commands you can use:</strong></p>
        <ul>
        <li><strong>urlshorten [Link]:</strong> To get a shortened link for your long URL 😁</li>
        <li><strong>translate [Text]:</strong> To translate your text from English to Hindi 💬</li>
        <li><strong>holidays:</strong> To fetch all the public holidays of India 🎃</li>
        <li><strong>ask:</strong> To ask any query from the internet 🧐</li>
        <li><strong>meme:</strong> To generate a meme 😄</li>
        <li><strong>joke:</strong> To generate a joke 😵‍💫</li>
        <li><strong>playsong:</strong> To play a Spotify song 🎵</li>
        <li><strong>spotifyplaylist:</strong> To get a Spotify playlist 📽️</li>
        </ul>
        """
    elif user_message.startswith("meme"):
        bot_response=get_memes();
    elif user_message.startswith("urlshorten"):
        url = user_message.replace("urlshorten", "").strip()
        print(url);
        bot_response = get_urlshorten(url)
        
    elif user_message.startswith("translate"):
        text = user_message.replace("translate", "").strip().lower()
        bot_response = get_translate(text)
    
    elif user_message.startswith("holidays"):
        bot_response = get_holidays()
        
    elif user_message.startswith("generate"):
        url = user_message.replace("generate", "").strip()
        bot_response = generate_image(url)
        
    elif user_message.startswith("joke"):
        bot_response = get_joke()
    
    elif user_message.startswith("playsong"):
        bot_response = download_song()
        
    elif user_message.startswith("spotifyplaylist"):
        bot_response = song_playlist()
        
    else:
        # # Generate GPT-3.5 Turbo response
        bot_response = models.OpenAI.generate(
        system_prompt=SYSTEM_PROMPT,
        message_history=user_message,
        model="gpt-3.5-turbo",
        
    )

    return bot_response, state
