
class Channel:

    def __init__(self, name):

        self.name = name

        # Keep track of messages
        self.messages = []

    def addMessage(self, message):

        # Limit history to 100 messages
        if len(self.messages) >= 100:
            self.messages.pop[0]

        self.messages.append(message)
