# Horoscope newsletter bot
### 1. What is it?
The bot allows anyone to subscribe to the horoscope newsletter on Telegram. There is an admin panel where you can view all users, change the time of mailing or add a post to the message. 

~~This horoscopes are absolutely original and are not taken from mail.ru~~

### 2. What do you need it for?
- If you know how to do social media, It is quite __possible to consider earning__ from this bot.
- You have been __looking for a bot with this functionality__.
- You __want to make a bot with a similar purpose__.

### 3. What libraries have been used?
I have used the Telebot, BeautifulSoup, requests libraries as well as the "out of the box" libraries os, time, threading, datetime and csv. The choice of libraries is due to my inexperience, in particular now I would use some more interesting database rather than a csv file.

### 4. What do you need to do to use it?
First, [download it =)](https://github.com/LevRuzaev/Horoscope-newsletter-bot/releases/tag/Horobot)

And then just replace ```<key=)>``` with your bot's key (which you get from BotFather).
```python
bot = telebot.TeleBot('key=)')
```

### 5. Documentation?
For the welcome message and checking the person on the user to the mailing list is used feature:
```python
def say_hi(message):
    ***
```

A function is used for the welcome addition of a user to the mailing list:

```python
def append_user(message):
    ***
```

If it's the first time a user has walked in, they are greeted in a special way:

```python
def new_player(message):
    ***
```

Selects a zodiac sign and throws you to the first horoscope output:

```python
def main_choose(message):
    ***
```

The first output of the horoscope, take the zodiac sign in the global person_mark, then the horoscope should come automatically every day:

```python
def on_click(message):
    ***
```

Daily horoscope newsletter:

```python
def do_horo_every_day():
    ***
```

Mailing at a certain time:

```python
def do_schedule():
    ***
```

__These were the highlights of main.py__

__In stolen.py, the horoscope is parsed. I recommend changing the source!!!__
```python
from bs4 import BeautifulSoup
import requests


def horoscope(mark):
    headers = {
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 OPR/99.0.0.0 (Edition Yx GX)"
    }

    url = f'https://horo.mail.ru/prediction/{mark}/today/'
    req = requests.get(url, headers=headers)
    src = req.text
    soup = BeautifulSoup(src, "lxml")
    all_horo_text = soup.find(class_="article__item article__item_alignment_left article__item_html")
    horo = str(all_horo_text)[75:].replace('<p>', '').replace('</p>', '').replace('</div>', '')
    return horo

```
