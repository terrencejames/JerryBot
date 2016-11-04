# -*- coding: utf8 -*-
from roll import roll
from flip import flip
from menu import menu
from choose import choose
from weather import weather, jacket
from random import randint
from tip import tip
from translate.py import translate_text
import mini_modules

help_string = ""

def help_message(args=[]):
    global help_string
    if help_string is "":
        result = "Commands:\n"
        for key in sorted(modules):
            result += "  !%s\n" %(key)
        help_string = result
    return help_string


"""command : function"""
modules = {
    "roll": roll,
    "flip": flip,
    "help": help_message,
    "menu": menu,
    "fud": menu,
    "food": menu,
    "sustenance":menu,
    "thanks": mini_modules.thanks,
    "eatadick": mini_modules.eatadick,
    "weather": weather,
    "jacket": jacket,
    "barrelroll" : mini_modules.doabarrelroll,
    "doabarrelroll": mini_modules.doabarrelroll,
    "shrug": mini_modules.shrug,
    "birb": mini_modules.bird,
    "choose": choose,
    "tip": tip,
    "translate" : translate_text
    }

