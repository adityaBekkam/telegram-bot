import os
import sys
import telegram

BOT = None
TOKEN = None
WEBHOOK_URL = None    # Optional if registration is already done
GIPHY_API_KEY = None  # Specific to my bot

# -- Env Variables -- #
# TOKEN (Mandatory)
# WEBHOOK_URL (Optional, if registration is already done)
# GIPHY_API_KEY (Specific to my bot)
# ------------------- #

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

    if BOT.setWebhook(WEBHOOK_URL):
        print("webhook setup ok")
    else:
        print("webhook setup failed")
        sys.exit()

def get_bot():
    global BOT
    return BOT

def get_giphy_key():
    global GIPHY_API_KEY
    return GIPHY_API_KEY
