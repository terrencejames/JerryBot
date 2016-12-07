import permissions as p
import os
import json
from json_fix import *

def vote(args, perms = {}):
    """
        If a poll has been started records who voted and what the vote was.
        This is done by reading/writing to 2 json files.
        @seb
    """
    # Store permissions
    try:
        threadID = perms[p.MESSAGE_THREADID]
    except KeyError:
        # No threadID -> private message
        return "You can't vote in a chat by yourself!"

    userID = perms[p.USER_NAME]
    
    # Get folder names for group chats that have previously polled
    polls = os.listdir('modules/poll')

    # If your group has a folder already
    if threadID in polls:
        # If previosly started poll
        if os.path.isfile('modules/poll/' + threadID + '/voting.txt'):
            # If first vote (votes file doesn't exist yet)
            if not os.path.isfile("modules/poll/" + threadID + "/votes.txt"):
                response = " ".join(args)
                # Record vote
                with open("modules/poll/" + threadID + "/votes.txt","w") as votes:
                    json.dump({response : 1}, votes)
                with open("modules/poll/" + threadID + "/voted.txt", "w") as voted:
                    json.dump({userID : True}, voted)
                return userID.split()[0] + " voted!"
            else:
                # Files already exist; read in the json
                with open("modules/poll/" + threadID + "/votes.txt", "r") as votes:
                    num_votes = json_load_byteified(votes)
                with open("modules/poll/" + threadID + "/voted.txt", "r") as voted:
                    voters = json_load_byteified(voted)

                # Update votes/voters if haven't already voted
                if userID in voters:
                    return userID.split()[0] + " already voted!"
                else:
                    if response in num_votes:
                        num_votes[response] = num_votes[response] + 1
                    else:
                        num_votes[response] = 1
                    voters[userID] = True

                # Write to out file; update votes/voted
                with open("modules/poll/" + threadID + "/votes.txt", "w") as votes:
                    json.dump(num_votes, votes)
                with open("modules/poll/" + threadID + "/voted.txt", "w") as voted:
                    json.dump(voters, voted)
                return None
        else:
            return "Poll hasn't been started!"
    else:
        return "Poll hasn't been started!"

    return None