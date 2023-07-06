import json
from channels.generic.websocket import AsyncWebsocketConsumer
from base.models import *

class CanteenProvider(AsyncWebsocketConsumer):
	async def connect(self):
		self.room_name = self.scope['url_route']['kwargs']['room_name']
		self.room_group_name = 'canteen_%s' % self.room_name
		# Join room group
		await self.channel_layer.group_add(
			self.room_group_name,
			self.channel_name
		)

		await self.accept()
	
	async def disconnect(self, close_code):
		# Leave room group
		await self.channel_layer.group_discard(
			self.room_group_name,
			self.channel_name
		)

	# Receive message from WebSocket
	# async def receive(self, text_data):
	# 	text_data_json = json.loads(text_data)
	# 	message = text_data_json['message']

	# 	# Send message to room group
	# 	await self.channel_layer.group_send(
	# 		self.room_group_name,
	# 		{
	# 			'type': 'chat_message',
	# 			'message': message
	# 		}
	# 	)

	async def receive(self, text_data):
		text_data_json = json.loads(text_data)
		message = text_data_json["message"]
		username = text_data_json["username"]
		await self.channel_layer.group_send(
			self.roomGroupName,{
				"type" : "sendMessage" ,
				"message" : message ,
				"username" : username ,
			})
	async def sendMessage(self , event) :
		message = event["message"]
		username = event["username"]
		await self.send(text_data = json.dumps({"message":message ,"username":username}))


	# Functions to perform:
		# 1. Create Orders
		# 2. Deliver OTP
		# 3. Provide information on availability of orders
		# 4. 