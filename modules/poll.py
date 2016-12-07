import permissions as p
import os

def poll(args, perms = {}):
    """
        Starts a poll by creating the "voted.txt" file in a directory named
        after the threadID of the chat it was called in.
        @seb
    """
    # Careful w/ threadID (None if in a pm)
    try:
        threadID = perms[p.MESSAGE_THREADID]
        if threadID is None:
            raise KeyError
    except KeyError:
        # No threadID -> private message
        return "You can't poll in a chat by yourself!"
    time = perms[p.MESSAGE_TIME]

    # Get folder names for group chats that have previously polled
    polls = os.listdir('modules/poll')

    # If thread doesn't already have a poll folder, make one
    if threadID not in polls:
        os.mkdir('modules/poll/' + threadID)

    # Make temp file that indicates currently voting
    if not os.path.isfile("modules/poll/" + threadID + "/voting.txt"):
        with open("modules/poll/" + threadID + "/voting.txt", "w") as voting:
            voting.write(threadID + " started poll at " + time + ' \n')
    else:
        return "Poll currently in process!"

    return "Poll started!"