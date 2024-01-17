import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class JoinAndLeave(WebsocketConsumer):
    def connect(self):
        print("server says connected")
        self.accept()    # new

    def receive(self, text_data=None, bytes_data=None):
        print("server says client message received: ", text_data)
        self.send("Server sends Welcome")

    def disconnect(self, code):
        print("server says disconnected")


class GroupConsumer(WebsocketConsumer):
    room_group_name = "staff_group"
    # room_name = "update_date"

    def connect(self):
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data=None, bytes_data=None):
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "staff_message", "message": 'update_data'}
        )

    # Receive message from room group
    def staff_message(self, event):
        message = event["message"]
        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message}))

