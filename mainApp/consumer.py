import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.core import serializers
class ChatConsumer(WebsocketConsumer):

    def connect(self):
        self.user = self.scope['user']
        self.room_name = 'chatroom'
        self.room_group_name = 'chatgroup'

            # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name)

        self.accept()
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, 
            {
               'type' : 'chat_bot',
               'alert' : str(self.scope['user']) + ' joined the chat' 
            }
        )

    def disconnect(self):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user = str(self.user)
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'author' : user,
            }
        )

    def chat_message(self, event):
        message = event['message']
        author = event['author']
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'author' : author,
        }))

    def chat_bot(self, event):
        alert = event['alert']
        self.send(text_data = json.dumps({
            'alert' : alert,
            'type' : 'alert_message'
        }))