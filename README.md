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
Just replace ```<key=)>``` with your bot's key (which you get from BotFather).
```python
bot = telebot.TeleBot('key=)')
```
