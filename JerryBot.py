# -*- coding: utf8 -*-
from fbchat.fbchat import Client
from credentials import USERNAME, PASSWORD
from modules.modules import modules
from modules.tag import tag
from configuration import prefixes
import sys
import multiprocessing
import modules.permissions as p

class JerryBot(Client):
    test = True
    modules = {}
    def __init__(self, email, password, test=True, debug=True, user_agent=None):
        Client.__init__(self, email, password, debug, user_agent)
        self.self = test
        self.modules = modules

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

        return (False, "")

    def send_message(self, message,author_id, metadata):
        if "threadFbId" in metadata["delta"]["messageMetadata"]["threadKey"]:
            #if str(author_id) != str(self.uid):
            isValid, result = self.parse_message(message, author_id, metadata)
            if isValid:
                self.send(metadata["delta"]["messageMetadata"]["threadKey"]["threadFbId"], result, message_type='group')
        #reply to people
        else:
            if str(author_id) != str(self.uid):
                isValid, result = self.parse_message(message, author_id, metadata)

                if isValid:
                    self.send(author_id, result)


    def on_message(self, mid, author_id, author_name, message, metadata):
        try:
            self.markAsDelivered(author_id, mid) #mark delivered
            self.markAsRead(author_id) #mark read

            if self.test:
                print("==METADATA==")
                print("%s said: %s"%(self.getUserInfo(author_id)['name'], message))
                # print(mid)
                # print(author_name)
                # print(metadata)
                print("====")

            p = multiprocessing.Process(target=self.send_message, args=(message, author_id, metadata))
            p.start()

            #reply to groups
        except Exception, e:
            print(e)



def main():

    #create bot
    bot = JerryBot(USERNAME, PASSWORD)

    #kep going
    while 1:
        try:
            bot.listen()
        #quit
        except (KeyboardInterrupt, SystemExit):
            sys.exit(0)
        else:
            #print diagnostic info
            print(sys.exc_info()[0])


if __name__ == "__main__":
    main()
