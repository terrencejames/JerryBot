from fbchat.fbchat import Client
from credentials import USERNAME, PASSWORD
from modules.modules import modules
from configuration import prefixes

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

    def on_message(self, mid, author_id, author_name, message, metadata):
        self.markAsDelivered(author_id, mid) #mark delivered
        self.markAsRead(author_id) #mark read

        if self.test:
            print("%s said: %s"%(author_id, message))
            print(mid)
            print(author_name)
            print(metadata)
            print("===")

        if "threadFbId" in metadata["delta"]["messageMetadata"]["threadKey"]:
            #if str(author_id) != str(self.uid):
            isValid, result = self.parse_message(message)
            if isValid:
                self.send(metadata["delta"]["messageMetadata"]["threadKey"]["threadFbId"], result, message_type='group')
        print("\n\n\n")


def main():
    bot = JerryBot(USERNAME, PASSWORD)
    bot.listen()




if __name__ == "__main__":
    main()
