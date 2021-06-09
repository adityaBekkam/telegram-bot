import telegram

from startup import initialise, get_bot
from bot import respond

initialise()
def handle_request(request):
    initialise()
    BOT = get_bot()
    update = telegram.Update.de_json(request.get_json(force=True), BOT)
    if not update or not update.message or not update.message.chat:
        print("Unable to extract the chat/message details")
        print("Request body: ", request.get_json(force=True))
        return

    return respond(update)

# if __name__ == "__main__":
#     from bot import get_gif_url
#     BOT = get_bot()
#     BOT.sendAnimation(chat_id=1055163296, animation=get_gif_url("sorry"))
