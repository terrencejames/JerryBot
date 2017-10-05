# -*- coding: utf8 -*-
from fbchat import log, Client
from credentials import USERNAME, PASSWORD
from modules.modules import modules
from modules.tag import tag
from configuration import prefixes
import sys
import multiprocessing
import modules.permissions as p


class LuxBot(Client):
    # test = False
    # modules = {}
    # def __init__(self, email, password, test=True, debug=True, user_agent=None):
    #     Client.__init__(self, email, password, debug, user_agent)
    #     self.self = test
    #     self.modules = modules

    def isCommand(self, command):
        for key, val in modules.iteritems():
            if key == command:
                return val
        return False

    def get_permission(self, author_id, metadata, permission):
        print("in permissions")

        #build permissions
        temp = {
                p.MESSAGE_TIME : metadata["delta"]["messageMetadata"]["timestamp"],
                p.MESSAGE_AUTHOR : author_id,
                p.MESSAGE_MESSAGEID : metadata["delta"]["messageMetadata"]["messageId"],
                p.USER_NAME : self.getUserInfo(author_id)['name']
            }
        try:
            temp[p.MESSAGE_THREADID] = metadata["delta"]["messageMetadata"]["threadKey"]["threadFbId"]
        except:
            # This means it's an individual message, so no Thread ID.
            # Simply don't include it in the perms
            pass
        return temp.get(permission, None)

    def parse_message(self, message, author_id, metadata):
        # If the message starts w/ one of the specified prefixes
        try:
            if message[0] in prefixes:
                #split the message into parts
                args = message[1:].strip().lower().split(" ")
                #first part is the command
                command = args[0]
                #rest is the arguments
                arguments = args[1:]
                #if there is a command for the argument
                command_module = self.isCommand(command)
                if command_module is not False:
                    #get the function and permissions list
                    module, permissions = command_module
                    perm_dict = {}
                    print("index of perms is:",permissions)
                    #build the perms
                    for perm in permissions:
                        try:
                            perm_res = self.get_permission(author_id, metadata, perm)
                            print("perm res %s" %(perm_res))
                            perm_dict[perm]= (perm_res)
                        except Exception as e:
                            print("error %s" %(e))
                    print(perm_dict)
                    #pass the function the arguments and permissions dictionary
                    result = module(arguments, perm_dict)
                    return (True, result)
            elif message[0] == '@':
                # Tagging module
                result = tag(message[1:])
                return (True, result)
        except Exception as e:
            with open('error.log', 'w') as log:
                log.write("OOPS, THERE WAS AN ERROR:\n {}".format(str(e)))
            return (True, "Failing gracefully..")


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
