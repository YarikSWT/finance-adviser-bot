from telegram.ext import BasePersistence
from telegram_bot.config import mongo_URI
from copy import deepcopy
from telegram.utils.helpers import decode_conversations_from_json, encode_conversations_to_json
import mongoengine
import json
from bson import json_util

class Conversations(mongoengine.Document):
    obj = mongoengine.DictField()
    meta = { 'collection': 'Conversations', 'ordering': ['-id']}

class MongoPersistence(BasePersistence):

    def __init__(self):
        super(MongoPersistence, self).__init__(store_user_data=False,
                                               store_chat_data=False,
                                               store_bot_data=False)

        dbname = "persistencedb"
        mongoengine.connect(host=mongo_URI, db=dbname)
        self.conversation_collection = "Conversations"
        self.conversations = None
        self.on_flush = False

    def get_conversations(self, name):
        if self.conversations:
            pass
        else:
            document = Conversations.objects()
            if document.first() == None:
                document = {}
            else:
                document = document.first()['obj']
            conversations_json = json_util.dumps(document)
            self.conversations = decode_conversations_from_json(conversations_json)
        return self.conversations.get(name, {}).copy()

    def update_conversation(self, name, key, new_state):
        if self.conversations.setdefault(name, {}).get(key) == new_state:
            return
        self.conversations[name][key] = new_state
        if not self.on_flush:
            conversations_dic = json_util.loads(encode_conversations_to_json(self.conversations))
            document = Conversations(obj=conversations_dic)
            document.save()

    def flush(self):
        conversations_dic = json_util.loads(encode_conversations_to_json(self.conversations))
        document = Conversations(obj=conversations_dic)
        document.save()
        mongoengine.disconnect()

    def get_bot_data(self):
        super()

    def get_chat_data(self):
        super()

    def get_user_data(self):
        super()

    def update_bot_data(self):
        super()

    def update_chat_data(self):
        super()

    def update_user_data(self):
        super()