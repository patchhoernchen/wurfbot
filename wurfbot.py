#!/usr/bin/env python
# -*- coding: utf-8 -*-


import logging
import random

from telegram import (
    Update,
)

from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackContext,
)


import config
from tgbot import (
    TgBot,
    tgcmd,
)


class Wurfbot(TgBot):

    INSULTS = [
        ", you stupid dumb fuck!",
        ", you sun of a beach!",
        ", you human!",
        ", you acid container containing lifeform!",
        ", [your insult HERE].",
        ". I'll punch you like an initiative!",
        ".",
        ". Sorry Dave, I'm afraid I can't do that.",
    ]

    NONMAGIC_NUMERS = "{user} rolled a {result}"
    MAGIC_NUMBERS = {
        5: "{user} rolled a {result} - Heil Eris",
        23: "{user} rolled a {result} - Nothing is what it seems.",
        42: "{user} rolled a {result} - Don't Panic",
        1337: "{user} rolled a {result} \o/",
    }

    NONMAGIC_WORDS = "{dice} is not an integer{insult}"
    MAGIC_WORDS = {
        "rick": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "pi": "if you role pi you get a diameter of 1.",
    }

    IMPOSSIBLE_DICE = [
        "i refuse to roll a dice with {dice} sides{insult}",
        "your impossible dice fell into the edge.",
    ]

    EMPTY_DICE = [
        "\"Nothing\" is not a valid number of sides for a dice{insult}",
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    ]

    def setup_handler(self) -> None:
        self.dispatcher.add_handler(CommandHandler('ping', self.ping))
        self.dispatcher.add_handler(CommandHandler('roll', self.roll))
        self.dispatcher.add_handler(CommandHandler('src', self.src))

    @tgcmd
    def src(self, cmd: list, update: Update, context: CallbackContext) -> str:
        return config.SRC

    @tgcmd
    def ping(self, cmd: list, update: Update, context: CallbackContext) -> str:
        return "pong"

    def insult(self) -> str:
        return random.choice(self.INSULTS)

    @tgcmd
    def roll(self, cmd: list, update: Update, context: CallbackContext) -> str:
        if not len(cmd) == 2:
            return random.choice(self.EMPTY_DICE).format(
                user=update.message.from_user.full_name,
                result=None,
                dice=None,
                insult=self.insult()
            )
        try:
            dice = int(cmd[1])
        except ValueError as e:
            return self.MAGIC_WORDS.get(
                cmd[1].lower(),
                self.NONMAGIC_WORDS
            ).format(
                user=update.message.from_user.full_name,
                result=None,
                dice=cmd[1],
                insult=self.insult()
            )
        if dice <= 1:
            return random.choice(self.IMPOSSIBLE_DICE).format(
                user=update.message.from_user.full_name,
                result=None,
                dice=cmd[1],
                insult=self.insult()
            )
        else:
            r = random.randrange(1, dice+1)
            return self.MAGIC_NUMBERS.get(
                r,
                self.NONMAGIC_NUMERS
            ).format(
                user=update.message.from_user.full_name,
                result=r,
                dice=cmd[1],
                insult=self.insult()
            )


def main() -> None:
    wb = Wurfbot(config.TOKEN)
    wb.start()


if __name__ == '__main__':
    main()
