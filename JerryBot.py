# -*- coding: utf8 -*-
from fbchat.fbchat import Client
from credentials import USERNAME, PASSWORD
from modules.modules import modules
from configuration import prefixes
import sys
import multiprocessing


class JerryBot(Client):
    test = False
    modules = {}
    def __init__(self, email, password, test=True, debug=True, user_agent=None):
        Client.__init__(self, email, password, debug, user_agent)
        self.self = test
        self.modules = modules



    def parse_message(self, message):
        if message[0] in prefixes:
            args = message[1:].split(" ")
            command = args[0]
            arguments = args[1:]
            if command in modules:
                return (True, modules[command](arguments))
        return (False, "")

    def send_message(self, message,author_id, metadata):
        if "threadFbId" in metadata["delta"]["messageMetadata"]["threadKey"]:
            #if str(author_id) != str(self.uid):
            isValid, result = self.parse_message(message)
            if isValid:
                self.send(metadata["delta"]["messageMetadata"]["threadKey"]["threadFbId"], result, message_type='group')
        #reply to people
        else:
            if str(author_id) != str(self.uid):
                isValid, result = self.parse_message(message)

                if isValid:
                    self.send(author_id, result)


    def on_message(self, mid, author_id, author_name, message, metadata):
        try:
            self.markAsDelivered(author_id, mid) #mark delivered
            self.markAsRead(author_id) #mark read

            if self.test:
                print("%s said: %s"%(author_id, message))
                print(mid)
                print(author_name)
                print(metadata)
                print("===")

            p = multiprocessing.Process(target=self.send_message, args=(message, author_id, metadata))
            p.start()

            #reply to groups
        except Exception, e:
            print(e)



def main():

    bot = JerryBot(USERNAME, PASSWORD)
    while 1:
        try:
            bot.listen()
        except (KeyboardInterrupt, SystemExit):
            sys.exit(0)
        else:
            print(sys.exc_info()[0])


if __name__ == "__main__":
    main()
