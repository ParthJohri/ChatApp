import textbase
from textbase.message import Message
from textbase import models
import os
from typing import List
from dotenv import load_dotenv
load_dotenv() 
import requests

# API KEYS
MY_API_KEY = os.environ['MY_API_KEY']
WEATHER_API_KEY = os.environ['WEATHER_API']
URL_SHORTENER = os.environ['URL_SHORTENER']
TRANSLATE_API_KEY = os.environ['TRANSLATE_API_KEY']
HOLIDAYS_API_KEY = os.environ['HOLIDAYS_API_KEY']
MEME_API_KEY = os.environ['MEME_API_KEY']

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
    return url+title;
    
def get_holidays(countrycode):


    url = "https://working-days.p.rapidapi.com/1.3/analyse"

    querystring = {"start_date":"2013-01-01","end_date":"2013-12-31","country_code":"IN","end_time":"18:15","start_time":"09:14"}

    headers = {
        "X-RapidAPI-Key": HOLIDAYS_API_KEY,
        "X-RapidAPI-Host": "working-days.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()

    public_holidays = data.get('public_holidays', {}).get('list', [])

    result_string = "Holiday Days:\n"

    for holiday in public_holidays:
        description = holiday.get('description', 'N/A')
        date = holiday.get('date', 'N/A')
        result_string += f"- {description}: {date}\n"

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
        bot_response = """Here are some of the commands you can use:
        - urlshorten [Link]: To get shorten link for your long url
        - translate [Text]: To translate your text from English to Hindi
        - holidays: To fetch all the public holidays of your country
        - ask: To ask any query from the internet
        - meme: To generate a meme
        """
    elif user_message.startswith("meme"):
        bot_response=get_memes();
    elif user_message.startswith("urlshorten"):
        url = user_message.replace("urlshorten", "").strip()
        print(url);
        bot_response = get_urlshorten(url)
        
    elif user_message.startswith("translate"):
        text = user_message.replace("translate", "").strip()
        bot_response = get_translate(text)
    
    elif user_message.startswith("holidays"):
        bot_response = "Please Enter Your Country Code"
        text = user_message.upper();
        bot_response = get_holidays(text)
        
    else:
        # # Generate GPT-3.5 Turbo response
        bot_response = models.OpenAI.generate(
        system_prompt=SYSTEM_PROMPT,
        message_history=message_history,
        model="gpt-3.5-turbo",
    )

    return bot_response, state
