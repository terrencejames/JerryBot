from random import randint
from datetime import datetime
import os




"""
check the day

if the cache file does not exist, write to it and return

if it does exist, then
  if the day matches return whatever it says

  otherwise overwrite the file and return a new result
"""
def snack(args):
    day = datetime.weekday(datetime.today())
    if day < 3 or date == 6:
        if not os.path.exists(os.path.join(os.getcwd(), "_snack.txt")):
            with open("_snack.txt", 'w+') as f:
                f.write(str(day) + "\n")
                res = randint(1,2)
                if res == 1:
                    f.write("1")
                    return "Nothing good"
                else:
                    f.write("2")
                    return "PB & J"
        else:
            with open("_snack.txt", 'r+') as f:
                lines = f.read().split("\n")
                if lines != []:
                    if str(day) == lines[0]:
                        if lines[1] == "1":
                            res = random.randint(1,2)
                            if res == 1:
                                return "nothing good"
                            else:
                                return "literally NOTHING"
                        else:
                            return "PB & J"
                    else:
                        f.seek(0)
                        f.write(str(day) + "\n")
                        res = randint(1,2)
                        if res == 1:
                            f.write("1")
                            return "Nothing good"
                        else:
                            f.write("2")
                            return "PB & J"
                else:
                        f.seek(0)
                        f.write(str(day) + "\n")
                        res = randint(1,2)
                        if res == 1:
                            f.write("1")
                            return "Nothing good"
                        else:
                            f.write("2")
                            return "PB & J"

    else:
        return "No snack today"

