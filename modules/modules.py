from roll import roll
from flip import flip

def help_message(args=[]):
    result = "Commands:\n"
    for key,value in modules.items():
        result += "  !%s\n" %(key)
    return result

modules = {
    "roll": roll,
    "flip": flip,
    "help": help_message
    }


