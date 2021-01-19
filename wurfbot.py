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
        ", you sun of a beach!",
        ", you human!",
        ", [your insult HERE].",
        ".",
        ". Sorry Dave, I'm afraid I can't do that.",
        ". Do you live in a black hole?",
        ". And the earth is not flat!",
        ". And furthermore I encourage Mrs. Scheeres to resign as senator of education.",
    ]

    NONMAGIC_NUMERS = [
        "{user} rolled a `{result}`.",
        "{user} rolled a `{result}`, deal with it.",
        "{user} rolled a `{result}`, pleased to serve you.",
        "You rolled a `{result}`",
        "You rolled a `{result}`, grats.",
        "You rolled a `{result}`. Really.",
        "The dice choose `{result}` to be enough for you, {user}.",
        "It's a `{result}`.",
        "It's a `{result}`. Deal with it, {user}.",
        "A `{result}`! But the dice fell of the table.",
        "The dice atilt, but it's a `{result}`.",
        "The dice fell of the table and you cannot find it. Find a new one and roll again.",
    ]
    MAGIC_NUMBERS = {
        5: "{user} rolled a `{result}` - Heil Eris",
        23: "{user} rolled a `{result}` - Nothing is what it seems.",
        42: "{user} rolled a `{result}` - Don't Panic",
        1337: "{user} rolled a `{result}` \o/",
    }

    NONMAGIC_WORDS = "{dice} is not an integer{insult}."
    MAGIC_WORDS = {
        "rick": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "pi": "When you role pi you get a diameter of 1.",
        "cookie": "Sure, but you need to come to the dark side.",
        "cookies": "Sure, but you need to come to the dark side.",
    }

    IMPOSSIBLE_DICE = [
        "I refuse to roll a dice with {dice} sides{insult}",
        "Your impossible dice fell onto the edge.",
        "The dice fell off the table and you cannot find it anywhere. But don't worry, it was broken anyway.",
    ]

    EMPTY_DICE = [
        "\"Nothing\" is not a valid number of sides for a dice{insult}",
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "You stepped onto one of the formerly lost dices and your left foot hurts. You loose 1w3 health.",
    ]

    def setup_handler(self) -> None:
        self.dispatcher.add_handler(CommandHandler('ping', self.ping))
        self.dispatcher.add_handler(CommandHandler('roll', self.roll))
        self.dispatcher.add_handler(CommandHandler('src', self.src))
        self.dispatcher.add_handler(CommandHandler('choose', self.choose))

    @tgcmd
    def choose(self, cmd: list, update: Update, context: CallbackContext) -> str:
        try:
            return random.choice(
                update.message['text'].split(' ', 2)[1].split('|')
            )
        except Exception as e:
            return "usage: `/choose pest|cholera|covid`"

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
        base = {'0x': 16, '0o': 8, '0b': 2, '0t': 3, '0q': 4}.get(cmd[1][0:2], 10)
        _dice = cmd[1] if base == 10 else cmd[1][2:]
        try:
            dice = int(_dice, base)
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
                random.choice(self.NONMAGIC_NUMERS)
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
