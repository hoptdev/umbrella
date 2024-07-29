import json

class User:
    def __init__(self, id, is_bot, first_name, last_name=None, username=None, language_code=None):
        self.id = id
        self.is_bot = is_bot
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.language_code = language_code
    
    def __init__(self, j):
        self.__dict__ = json.loads(j)

class Chat:
    def __init__(self, id, type, title=None, username=None, first_name=None, last_name=None):
        self.id = id
        self.type = type
        self.title = title
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
    
    def __init__(self, j):
        self.__dict__ = json.loads(j)

class Location:
    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude
    
    def __init__(self, j):
        data = json.loads(j)
        self.__dict__ = data


class Message:
    def __init__(self, message_id, from_user, chat, date, text, entities=None):
        self.message_id = message_id
        self.from_user = from_user
        self.chat = chat
        self.date = date
        self.text = text
        self.entities = entities
    
    def __init__(self, j):
        data = json.loads(j)
        self.__dict__ = data
        self.from_user = User(json.dumps(data["from"]))
        self.chat = Chat(json.dumps(self.chat))
        self.location = Location(json.dumps(data["location"])) if data.get("location") else None

    def __setstate__(self, state):
        self.from_user = state['from']

class Entity:
    def __init__(self, type, offset, length, url=None, user=None):
        self.type = type
        self.offset = offset
        self.length = length
        self.url = url
        self.user = user
    
    def __init__(self, j):
        self.__dict__ = json.loads(j)

class CallbackQuery:
    def __init__(self, id: str, from_user: User, inline_message_id: str = None, chat_instance: str = None, data: str = None, 
                 game_short_name: str = None, message: Message = None):
        self.id = id
        self.message = message
        self.from_user = from_user
        self.inline_message_id = inline_message_id
        self.chat = message.chat
        self.data = data
        self.game_short_name = game_short_name
    
    def __init__(self, j):
        data = json.loads(j)
        self.__dict__ = data
        self.from_user = User(json.dumps(data["from"]))
        self.message = Message(json.dumps(data['message'])) if data.get('message') else None
        self.chat = self.message.chat if self.message.chat else None

    def __setstate__(self, state):
        self.from_user = state['from']

class Update:
    def __init__(self, update_id, message=None, edited_message=None, channel_post=None, edited_channel_post=None, inline_query=None, chosen_inline_result=None, callback_query=None, shipping_query=None, pre_checkout_query=None, poll=None, poll_answer=None, my_chat_member=None, chat_member=None):
        self.update_id = update_id
        self.message = message
        self.edited_message = edited_message
        self.channel_post = channel_post
        self.edited_channel_post = edited_channel_post
        self.inline_query = inline_query
        self.chosen_inline_result = chosen_inline_result
        self.callback_query = callback_query
        self.shipping_query = shipping_query
        self.pre_checkout_query = pre_checkout_query
        self.poll = poll
        self.poll_answer = poll_answer
        self.my_chat_member = my_chat_member
        self.chat_member = chat_member

    def __init__(self, j):
        data = json.loads(j)
        self.__dict__ = data
        self.message = Message(json.dumps(data['message'])) if data.get('message') else None
        self.callback_query = CallbackQuery(json.dumps(data['callback_query'])) if data.get('callback_query') else None