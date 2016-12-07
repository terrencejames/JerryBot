import permissions as p
import os
import json
from json_fix import *

def end(args, perms = {}):
    """
        If a poll was previously started, ends it by deleting the 3 files
        and printing results.
        @seb
    """
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
            # Read the final votes
            try:
                with open("modules/poll/" + threadID + "/votes.txt", "r") as v:
                    # Delete the files
                    os.remove('modules/poll/' + threadID + '/votes.txt')
                    os.remove('modules/poll/' + threadID + '/voted.txt')
                    os.remove('modules/poll/' + threadID + '/voting.txt')
                    votes = json_load_byteified(v)
                    return "Poll ended!\n" + "\n".join(["%s : %i" %(k, v) for k, v in votes.iteritems()])
            except IOError:
                # Happens when trying to end poll that has no voters
                os.remove('modules/poll/' + threadID + '/voting.txt')
                return "No votes were cast :("
        else:
            return "Poll hasn't been started!"
    else:
        return "Poll hasn't been started!"

    return None