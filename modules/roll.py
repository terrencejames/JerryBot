from random import randint

def roll(args, permisions = {}):
    if len(args) > 0:
        try:
            num = int(args[0])
            return ("Rolled a %s sided die: %s" %(args[0], str(randint(1,num))))
        except e:
            return (str(args[0]) + " isn't an int!")
    else:
        return ("Rolled a die: %s") %(str(randint(1,6)))

