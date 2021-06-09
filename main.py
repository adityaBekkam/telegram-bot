import os
import sys
import telegram
import requests
import urllib
import json

# -- Required Env Variables -- #
BOT = None
TOKEN = None
# ---------------------------- #

# -- Optional Env Variables -- #
WEBHOOK_URL = None    # Optional if registration is already done
GIPHY_API_KEY = None  # Specific to my bot
# ---------------------------- #

# -- Static messages -- #
hello = "Hello {0}, how you doing"
welcome = """

Welcome to Bekkam's bot. Type a word & get some nice gifs.

Oh btw, kids get kiddo gifs :p
"""
sorry = "There was a problem with this message, please send a different one or try again"
# ---------------------------- #


def initialise():
    global BOT
    global TOKEN
    global WEBHOOK_URL
    global GIPHY_API_KEY
    if BOT and TOKEN and WEBHOOK_URL:
        return  # intialisation already done

    if not TOKEN:
        TOKEN = os.environ.get('TOKEN')
        if not TOKEN:
            sys.exit()

    if not WEBHOOK_URL:
        WEBHOOK_URL = os.environ.get("WEBHOOK_URL")
        if not WEBHOOK_URL:
            sys.exit()

    if not GIPHY_API_KEY:
        GIPHY_API_KEY = os.environ.get("GIPHY_API_KEY")
        if not GIPHY_API_KEY:
            print("Silently moving on")

    if not BOT:
        BOT = telegram.Bot(token=TOKEN)

    # if BOT.setWebhook(WEBHOOK_URL):
    #     print("webhook setup ok")
    # else:
    #     print("webhook setup failed")
    #     sys.exit()

def get_gif_url(text):
    url = "https://api.giphy.com/v1/gifs/translate?api_key={0}&s={1}".format(GIPHY_API_KEY, urllib.parse.quote(text))
    print(url)
    resp = requests.get(url)
    json_resp = json.loads(resp.content)
    gif_url = json_resp['data']['images']['original']['url']
    print(gif_url)
    return gif_url

def apologize_for_ise(chat_id, msg_id):
    BOT.sendMessage(chat_id=chat_id, text=sorry, reply_to_message_id=msg_id)
    BOT.sendAnimation(chat_id=chat_id, animation=get_gif_url("sorry"))

initialise()
def handle_request(request):
    initialise()
    update = telegram.Update.de_json(request.get_json(force=True), BOT)
    if not update or not update.message or not update.message.chat:
        print("Unable to extract the chat/message details")
        print("Request body: ", request.get_json(force=True))
        return

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

        if 'bhanu' in from_user.lower():
            BOT.sendMessage(chat_id=chat_id, text="You sound like a kid, so sending you a kid gif")
            gif_url = get_gif_url("baby")
            BOT.sendAnimation(chat_id=chat_id, animation=gif_url)
    else:
        try:
            gif_url = get_gif_url(text)
            BOT.sendAnimation(chat_id=chat_id, animation=gif_url, reply_to_message_id=msg_id)
        except Exception as ex:
            print(ex)
            apologize_for_ise(chat_id, msg_id)

    return 'ok'
