import requests
import urllib
import json

from messages import hello, welcome, sorry
from startup import get_bot, get_giphy_key

def get_gif_url(text):
    GIPHY_URL = "https://api.giphy.com/v1/gifs/translate?api_key={0}&s={1}"
    url = GIPHY_URL.format(get_giphy_key(), urllib.parse.quote(text))
    print(url)
    resp = requests.get(url)
    json_resp = json.loads(resp.content)
    gif_url = json_resp['data']['images']['original']['url']
    print(gif_url)
    return gif_url

def handle_ise(chat_id, msg_id):
    BOT = get_bot()
    BOT.sendMessage(chat_id=chat_id, text=sorry, reply_to_message_id=msg_id)
    BOT.sendAnimation(chat_id=chat_id, animation=get_gif_url("sorry"))

def respond(update):
    BOT = get_bot()
    chat_id = update.message.chat.id
    msg_id = update.message.message_id
    text = update.message.text.encode('utf-8').decode()
    from_user = update.message.from_user.username
    if not from_user:
        from_user = "hooman"

    print("got text message :", text)
    print("From user: ", from_user)
    print("chat_id: ", chat_id)

    text_ = text.lower()
    if "start" in text_ or "hello" in text_ or "hai" == text_ or "hi" == text_:
        BOT.sendMessage(chat_id=chat_id,
                        text=hello.format(from_user) + welcome,
                        reply_to_message_id=msg_id)
    else:
        try:
            gif_url = get_gif_url(text)
            BOT.sendAnimation(chat_id=chat_id, animation=gif_url, reply_to_message_id=msg_id)
        except Exception as ex:
            print(ex)
            handle_ise(chat_id, msg_id)

    return 'ok'
