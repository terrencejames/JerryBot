import permissions as p
import os
import json
from json_fix import *

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
    lock = perms[p.POLL_LOCK]
    lock.acquire()

    # Get folder names for group chats that have previously polled
    polls = os.listdir('modules/poll')

    # If thread doesn't already have a poll folder, make one
    if threadID not in polls:
        os.mkdir('modules/poll/' + threadID)

    # Make temp file that indicates currently voting
    if not os.path.isfile("modules/poll/" + threadID + "/voting.txt"):
        with open("modules/poll/" + threadID + "/voting.txt", "w") as voting:
            voting.write(threadID + " started poll at " + time + ' \n')
        lock.release()
        return "Poll started!"
    else:
        lock.release()
        return "Poll currently in process!"

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
    lock = perms[p.POLL_LOCK]
    lock.acquire()
    # Store vote
    response = " ".join(args)

    polls = os.listdir('modules/poll')

    # If your group has a folder already
    if threadID in polls:
        # If previosly started poll
        if os.path.isfile('modules/poll/' + threadID + '/voting.txt'):
            # If first vote (votes file doesn't exist yet)
            if not os.path.isfile("modules/poll/" + threadID + "/votes.txt"):
                # Record vote
                with open("modules/poll/" + threadID + "/votes.txt","w") as votes:
                    json.dump({response : 1}, votes)
                with open("modules/poll/" + threadID + "/voted.txt", "w") as voted:
                    json.dump({userID : True}, voted)
                lock.release()
                return userID.split()[0] + " voted!"
            else:
                # Files already exist; read in the json
                with open("modules/poll/" + threadID + "/votes.txt", "r") as votes:
                    num_votes = json_load_byteified(votes)
                with open("modules/poll/" + threadID + "/voted.txt", "r") as voted:
                    voters = json_load_byteified(voted)

                # Update votes/voters if haven't already voted
                if userID in voters:
                    lock.release()
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
                lock.release()
                return None
        else:
            lock.release()
            return "Poll hasn't been started!"
    else:
        lock.release()
        return "Poll hasn't been started!"

def result(args, perms = {}):
    # Store permissions
    try:
        threadID = perms[p.MESSAGE_THREADID]
    except KeyError:
        # No threadID -> private message
        return "You can't vote in a chat by yourself!"
    
    lock = perms[p.POLL_LOCK]
    lock.acquire()
    polls = os.listdir('modules/poll')
    # If your group has a folder already
    if threadID in polls:
        # If previosly started poll
        if os.path.isfile('modules/poll/' + threadID + '/voting.txt'):
            # Read the votes
            with open("modules/poll/" + threadID + "/votes.txt", "r") as v:
                votes = json_load_byteified(v)
                lock.release()
                return ("\n".join(["%s : %i" %(k, v) for k, v in votes.iteritems()]))
        else:
            lock.release()
            return "Poll hasn't been started!"
    else:
        lock.release()
        return "Poll hasn't been started!"

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
    

    lock = perms[p.POLL_LOCK]
    lock.acquire()
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
                    lock.release()
                    return "Poll ended!\n" + "\n".join(["%s : %i" %(k, v) for k, v in votes.iteritems()])
            except IOError:
                # Happens when trying to end poll that has no voters
                os.remove('modules/poll/' + threadID + '/voting.txt')
                lock.release()
                return "No votes were cast :("
        else:
            lock.release()
            return "Poll hasn't been started!"
    else:
        lock.release()
        return "Poll hasn't been started!"