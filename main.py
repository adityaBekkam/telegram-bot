import logging
import telegram

from startup import initialise, get_bot
from bot import respond

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG
)
logger = logging.getLogger(__name__)

initialise()
def handle_request(request):
    """
    Args:
        request (Flask.request): Flask request object

    Returns: 'ok' or None
    Raises: None
    """
    initialise()
    BOT = get_bot()
    update = telegram.Update.de_json(request.get_json(force=True), BOT)
    if not update or not update.message or not update.message.chat:
        logger.error("Unable to extract the chat/message details")
        logger.error("Request body: ", request.get_json(force=True))
        return

    return respond(update)

# if __name__ == "__main__":
#     from bot import get_gif_url
#     BOT = get_bot()
#     msg = "sleeping baby"
#     BOT.sendAnimation(chat_id=chat_id, animation=get_gif_url(msg))
#     BOT.sendMessage(chat_id=chat_id, text="Good night kiddoo")
