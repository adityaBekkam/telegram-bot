import requests
import urllib
import json
import logging

from messages import hello, welcome, sorry
from startup import get_bot, get_giphy_key

logger = logging.getLogger(__name__)

def get_gif_url(text):
    """
    Args:
        text (str): Text message sent by the user

    Returns:
        (str) URL corresponding to the user text received

    Raises: None
    """
    GIPHY_URL = "https://api.giphy.com/v1/gifs/translate?api_key={0}&s={1}"
    url = GIPHY_URL.format(get_giphy_key(), urllib.parse.quote(text))
    logger.debug(url)
    resp = requests.get(url)
    json_resp = json.loads(resp.content)
    gif_url = json_resp['data']['images']['original']['url']
    logger.debug(gif_url)
    return gif_url

def handle_ise(chat_id, msg_id):
    """
    Args:
        chat_id (int/str): ID of chat with the current user
        msg_id (int/str): ID of the user message in current context

    Returns: None
    Raises: None
    """
    BOT = get_bot()
    BOT.sendMessage(chat_id=chat_id, text=sorry, reply_to_message_id=msg_id)
    BOT.sendAnimation(chat_id=chat_id, animation=get_gif_url("sorry"))

def respond(update):
    """
    Args:
        update (<telegram.Update>): Object containing message details

    Returns: 'ok' or None
    Raises: None
    """
    BOT = get_bot()
    chat_id = update.message.chat.id
    msg_id = update.message.message_id
    text = update.message.text.encode('utf-8').decode()
    from_user = update.message.from_user.username
    if not from_user:
        from_user = "hooman"

    logger.debug("got text message :", text)
    logger.debug("From user: ", from_user)
    logger.debug("chat_id: ", chat_id)

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
            logger.error(ex)
            handle_ise(chat_id, msg_id)

    return 'ok'
