import os
import sys
import telegram
import logging

logger = logging.getLogger(__name__)

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
    """
    Args: None
    Returns: None
    Raises:
        sys.exit when mandatory arguments are not provided
        to the program
    """
    global BOT
    global TOKEN
    global WEBHOOK_URL
    global GIPHY_API_KEY
    if BOT and TOKEN and WEBHOOK_URL:
        return  # intialisation already done

    if not TOKEN:
        TOKEN = os.environ.get('TOKEN')
        if not TOKEN:
            logger.error("Bot token not provided")
            sys.exit()

    if not WEBHOOK_URL:
        WEBHOOK_URL = os.environ.get("WEBHOOK_URL")
        if not WEBHOOK_URL:
            logger.error("Webhook URL not provided")
            sys.exit()

    if not GIPHY_API_KEY:
        GIPHY_API_KEY = os.environ.get("GIPHY_API_KEY")
        if not GIPHY_API_KEY:
            logger.warning("Giphy key not configured. Silently moving on")

    if not BOT:
        BOT = telegram.Bot(token=TOKEN)

    if BOT.setWebhook(WEBHOOK_URL):
        logger.info("webhook setup ok")
    else:
        logger.error("webhook setup failed")
        sys.exit()

def get_bot():
    """
    Args: None
    Returns:
        BOT object (<telegram.Bot>)

    Raises: None
    """
    global BOT
    return BOT

def get_giphy_key():
    """
    Args:
    Returns:
        Value of API Key (str)

    Raises: None
    """
    global GIPHY_API_KEY
    return GIPHY_API_KEY
