import permissions as p
import os
import json
from json_fix import *

def result(args, perms = {}):
    # Store permissions
    try:
        threadID = perms[p.MESSAGE_THREADID]
    except KeyError:
        # No threadID -> private message
        return "You can't vote in a chat by yourself!"
    
    # Get folder names for group chats that have previously polled
    polls = os.listdir('modules/poll')

    # If your group has a folder already
    if threadID in polls:
        # If previosly started poll
        if os.path.isfile('modules/poll/' + threadID + '/voting.txt'):
            # Read the votes
            with open("modules/poll/" + threadID + "/votes.txt", "r") as v:
                votes = json_load_byteified(v)
                return ("\n".join(["%s : %i" %(k, v) for k, v in votes.iteritems()]))
        else:
            return "Poll hasn't been started!"
    else:
        return "Poll hasn't been started!"

    return None