import json
from channels.generic.websocket import AsyncWebsocketConsumer
from base.models import *
from base.custom_decorators import *
from django.contrib.auth.decorators import login_required
from asgiref.sync import sync_to_async


class CanteenProvider(AsyncWebsocketConsumer):
	async def connect(self):
		user=self.scope['user']
		user_obj = await sync_to_async(User.objects.get)(username=user.username)
		if(not user.is_authenticated):
			print("Error")
		temp = await sync_to_async(Canteen.objects.get)(canteen_owner=user_obj)
		print(temp)
		try:
			canteen = await sync_to_async(Canteen.objects.get)(canteen_owner=user_obj)
		except Canteen.DoesNotExist:
			print("Error: Canteen not found for the user")
			return
		await self.channel_layer.group_add(
			user_obj.username,
			self.channel_name
        )
		await self.accept()
	
	async def disconnect(self, close_code):
		await self.channel_layer.group_discard(
			'all',
			self.channel_name
		)

	async def receive(self, text_data):
		pass
	async def sendOrder(self,order) :
		await self.send(json.dumps({"message":order}))
	async def custom_message_handler(self, event):
		await self.sendOrder(event["order"])
		print("Ordered")

	async def deliverOrder(self , order) :
		pass


class CustomerConsumer(AsyncWebsocketConsumer):
	async def connect(self):
		await self.accept()
	
	async def disconnect(self, close_code):
		pass

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