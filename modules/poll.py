# -*- coding: utf8 -*-
from fbchat.fbchat import Client
from credentials import USERNAME, PASSWORD
from configuration import prefixes
import sys
import multiprocessing

isRunning = True

def poll(args):
    pollBot = PollBot(USERNAME, PASSWORD)
    while isRunning:
        try:
            pollBot.listen()
        except:
            pass
    return None

class PollBot(Client):
    def __init__(self, email, password, test=True, debug=True, user_agent=None):
        Client.__init__(self, email, password, debug, user_agent)
        self.modules = {
            "vote": self.vote,
            "result" : self.result,
            "end": self.end
        }
        self.votes = {}

    def end(self, args):
        global isRunning
        self.listening = False
        isRunning = False
        sys.exit(0)

    def vote(self, args):
        response = " ".join(args)
        if response in self.votes:
            val = self.votes[response]
            self.votes[response] = val + 1
        else:
            self.votes[response] = 1
        print self.votes
        return None

    def result(self, args):
        print("in result!")
        print self.votes
        return ("\n".join(["%s : %i" %(k, v) for k, v in self.votes.iteritems()]))


    def parse_message(self, message):
        if message[0] in prefixes:
            args = message[1:].split(" ")
            command = args[0]
            arguments = args[1:]
            if command in self.modules:
                return (True, self.modules[command](arguments))
        return (False, "")

    def send_message(self, message,author_id, metadata):
        if "threadFbId" in metadata["delta"]["messageMetadata"]["threadKey"]:
            #if str(author_id) != str(self.uid):
            isValid, result = self.parse_message(message)
            if isValid:
                self.send(metadata["delta"]["messageMetadata"]["threadKey"]["threadFbId"], message=result, message_type='group')
        #reply to people

    def on_message(self, mid, author_id, author_name, message, metadata):
        try:
            self.markAsDelivered(author_id, mid) #mark delivered
            self.markAsRead(author_id) #mark read
            self.send_message(message, author_id, metadata)

            #reply to groups
        except Exception, e:
            print(e)


