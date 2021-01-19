#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

import config

from telegram import (
    Update,
)

from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackContext,
)


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=config.LOGLEVEL
)
logger = logging.getLogger(__name__)


def log_result(update: Update, result: str) -> None:
    logging.debug(str(update))
    if config.LOG_RESULT:
        logging.info(f"{update.message.from_user.name}: {update.message['text']} -> {result}")


def tgcmd(func: callable) -> callable:
    """
    decorator to wrap arround tg-commands. cares about logging and sending the
    returnd string as reply to telegram.
    """
    def wrapper(bot_instance: TgBot, update: Update, context: CallbackContext):
        cmd = update.message["text"].split(' ')
        result = func(bot_instance, cmd, update, context)
        update.message.reply_text(result)
        log_result(update, result)
    return wrapper


class TgBot:
    """
    Abstrac class for a simple telegram bot.
    @token: bot-token obtained by BotFather@telegram
    """

    def __init__(self, token: str):

        # Create the Updater and pass it your bot's token.
        # Make sure to set use_context=True to use the new context based callbacks
        # Post version 12 this will no longer be necessary
        self.updater = Updater(token, use_context=True)
        self.dispatcher = self.updater.dispatcher

        self.setup_handler()

    def start(self) -> None:
        """
        Start the Bot actually
        """
        self.updater.start_polling()

        # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
        # SIGTERM or SIGABRT
        self.updater.idle()

    def setup_handler(self) -> None:
        """
        Abstract method to setup handlers, to implemented by the inheritant.
        """
        raise NotImplemented()

