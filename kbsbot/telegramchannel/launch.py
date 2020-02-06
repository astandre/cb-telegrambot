from kbsbot.telegramchannel.services import *
from kbsbot.telegramchannel.utils import *
from telegram import (ChatAction)
from telegram import (InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler,
                          ConversationHandler)
from telegram import ParseMode
import logging
from functools import wraps
import os

API_KEY = "616944972:AAFUU_Od5-fiEg_Oe7pV0g-aWgXuAVM0ctk"
# API_KEY = os.environ.get("API_KEY")

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

CHAT, HELP = range(2)


def send_typing_action(func):
    """Sends typing action while processing func command."""

    @wraps(func)
    def command_func(update, context, *args, **kwargs):
        context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=ChatAction.TYPING)
        return func(update, context, *args, **kwargs)

    return command_func


def start(update, context):
    user = update.message.from_user.username
    greetings = get_greetings()
    full_response = f"Hola {user} soy {greetings['name']}, {greetings['about']}. En que te puedo ayudar?"
    update.message.reply_text(full_response)


@send_typing_action
def chat(update, context):
    # update.send_chat_action(update.message.chat_id, action=ChatAction.TYPING)
    # logger.info("Raw-Message: %s", update.message)
    # Creating user
    user_name = update.message.from_user.username
    content = update.message.text
    name = update.message.from_user.first_name
    last_name = update.message.from_user.last_name
    id_account = update.message.chat_id

    data_user = {"user_name": user_name,
                 "name": name, "last_name": last_name,
                 "social_network_id": id_account}

    context.user_data["user"] = data_user
    # Creating context
    local_context = {
        "intent": None,
        "entities": []
    }
    if "entities" in context.chat_data and len(context.chat_data["entities"]) > 0:
        local_context["entities"] = context.chat_data["entities"]
    if "intent" in context.chat_data and context.chat_data["intent"] is not None:
        local_context["intent"] = context.chat_data["intent"]
    # Preparing data
    data = {
        "user": data_user,
        "input": {
            "user_input": content,
            "context": local_context
        }
    }
    logger.info("[CHAT] >>>>> SentData  %s", data)
    resp = chat_with_system(data)
    logger.info("[CHAT] <<<<< ReceivedData %s", data)
    if resp is not None:
        if len(resp["context"]["entities"]) > 0:
            context.chat_data["entities"] = resp["context"]["entities"]
        if resp["answer"]["answer_type"] == "text":
            update.message.reply_text(resp["answer"]["text"])
            context.chat_data["intent"] = None
        elif resp["answer"]["answer_type"] == "options":
            # print("Carrying context ", resp["context"]["intent"])
            context.chat_data["intent"] = resp["context"]["intent"]
            context.chat_data["entity_type"] = resp["answer"]["options"]["entity"]
            reply_keyboard = InlineKeyboardMarkup(
                prepare_keyboard(resp["answer"]["options"]["options"]))
            # reply_keyboard = ReplyKeyboardMarkup(prepare_keyboard2(resp["answer"]["options"]))
            update.message.reply_text(resp["answer"]["text"],
                                      reply_markup=reply_keyboard, one_time_keyboard=True)
        else:
            # update.message.reply_text(resp["output"])
            logger.error("Method not supported yet")
            update.message.reply_text("Method not supported yet")
    else:
        update.message.reply_text("Ha ocurrido un error al obtener su respuesta")


def button(update, context):
    query = update.callback_query
    entity = query.data
    entity_type = context.chat_data["entity_type"]
    local_context = {
        "intent": context.chat_data["intent"],
        "entities": [{"value": entity, "type": entity_type}]
    }
    data = {
        "user": context.user_data["user"],
        "input": {
            "user_input": None,
            "context": local_context
        }
    }
    logger.info("[BUTTON] >>>>> SentData  %s", data)
    resp = chat_with_system(data)
    logger.info("[BUTTON] <<<<< ReceivedData %s", data)
    if resp["answer"]["answer_type"] == "text":
        context.chat_data["intent"] = None
        context.chat_data["entities"] = resp["context"]["entities"]
        query.edit_message_text(text=resp["answer"]["text"])


def cancel(bot, update):
    return ConversationHandler.END


@send_typing_action
def ayuda(update, context):
    user_name = update.message.from_user.username
    content = update.message.text
    name = update.message.from_user.first_name
    last_name = update.message.from_user.last_name
    id_account = update.message.chat_id

    data_user = {"user_name": user_name,
                 "name": name, "last_name": last_name,
                 "social_network_id": id_account}

    local_context = {
        "intent": None,
        "entities": []
    }
    data = {
        "user": data_user,
        "input": {
            "help": True,
            "user_input": content,
            "context": local_context
        }
    }
    logger.info("[HELP] >>>>> SentData  %s", data)
    resp = chat_with_system(data)
    logger.info("[HELP] <<<<< ReceivedData %s", data)
    if resp["answer"]["answer_type"] == "help":
        full_response = prepare_chatbot_cap(resp["answer"]["help"])
        update.message.reply_text(full_response, parse_mode=ParseMode.MARKDOWN)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(token=API_KEY, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher
    updater.dispatcher.add_handler(CallbackQueryHandler(button))

    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler('start', start),
            CommandHandler('help', ayuda),
            MessageHandler(Filters.regex('.'), chat),
            # RegexHandler('\w', chat),
            # CommandHandler('cursos', chat),
        ],

        states={
            CHAT: [
                MessageHandler(Filters.text, chat),
                # CommandHandler('cursos', chat)
            ],
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    # Launching App
    logger.info("Starting bot")
    main()
