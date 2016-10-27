from fbchat.fbchat import Client
from credentials import USERNAME, PASSWORD

class JerryBot(Client):
    def __init__(self, email, password, debug=True, user_agent=None):
        Client.__init__(self, email, password, debug, user_agent)

    def on_message(self, mid, author_id, author_name, message, metadata):
        self.markAsDelivered(author_id, mid) #mark delivered
        self.markAsRead(author_id) #mark read

        print("%s said: %s"%(author_id, message))
        print(mid)
        print(author_name)
        print(metadata)
        print("===")
        if str(author_id) != str(self.uid):
            pass
            #self.send(author_id, "bot test")
        print("===\n\n")

        for key, value in metadata.items():
            print(key, value)

        if "threadFbId" in metadata["delta"]["messageMetadata"]["threadKey"]:
            if str(author_id) != str(self.uid):
                self.send(metadata["delta"]["messageMetadata"]["threadKey"]["threadFbId"], "bot test", message_type='group')
        print("\n\n\n")
bot = JerryBot(USERNAME, PASSWORD)
bot.listen()



