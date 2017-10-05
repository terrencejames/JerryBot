# -*- coding: utf8 -*-
from fbchat import log, Client
from credentials import USERNAME, PASSWORD
from modules.modules import modules
from configuration import prefixes
import sys

class LuxBot(Client):
    # test = False
    # modules = {}
    # def __init__(self, email, password, test=True, debug=True, user_agent=None):
    #     Client.__init__(self, email, password, debug, user_agent)
    #     self.self = test
    #     self.modules = modules



    def parse_message(self, message, thread_id, thread_type):
        if message[0] in prefixes:
        	args = message[1:].split(" ")
        	command = args[0]
        	arguments = args[1:]
        	if command in modules:
        		response = modules[command](arguments)
            	self.sendMessage(response, thread_id, thread_type)
        #         return (True, modules[command](arguments))
        # return (False, "")

    def onMessage(self, author_id, message, thread_id, thread_type, **kwargs):
        self.markAsDelivered(author_id, thread_id)
        self.markAsRead(author_id)

        log.info("Message from {} in {} ({}): {}".format(author_id, thread_id, thread_type.name, message))

        # If you're not the author, echo
        if author_id != self.uid:
        	self.parse_message(message, thread_id, thread_type)
            # self.sendMessage(message, thread_id=thread_id, thread_type=thread_type)

    # def on_message(self, mid, author_id, author_name, message, metadata):
    #     try:
    #         self.markAsDelivered(author_id, mid) #mark delivered
    #         self.markAsRead(author_id) #mark read

    #         log.info("Message from {} in {} ({}): {}".format(author_id, thread_id, thread_type.name, message))
    #         self.sendMessage(message, mid, thread_type=thread_type)


    #         if self.test:
    #             print("%s said: %s"%(author_id, message))
    #             print(mid)
    #             print(author_name)
    #             print(metadata)
    #             print("===")

    #         #reply to groups
    #         if "threadFbId" in metadata["delta"]["messageMetadata"]["threadKey"]:
    #             #if str(author_id) != str(self.uid):
    #             isValid, result = self.parse_message(message)
    #             if isValid:
    #                 self.send(metadata["delta"]["messageMetadata"]["threadKey"]["threadFbId"], result, message_type='group')
    #         #reply to people
    #         else:
    #             if str(author_id) != str(self.uid):
    #                 isValid, result = self.parse_message(message)

    #                 if isValid:
    #                     self.send(author_id, result)
    #     except:
    #         pass



def main():

    bot = LuxBot(USERNAME, PASSWORD)
    bot.listen()
    # while 1:
    #     try:
    #         bot.listen()
    #     except (KeyboardInterrupt, SystemExit):
    #         raise
    #     else:
    #         print(sys.exc_info()[0])
    #         print("error?")




if __name__ == "__main__":
    main()
