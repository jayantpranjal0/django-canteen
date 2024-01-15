import json
from channels.generic.websocket import AsyncWebsocketConsumer
from base.models import *
from base.custom_decorators import *
from django.contrib.auth.decorators import login_required
from asgiref.sync import sync_to_async
import math, random
 
# function to generate OTP
def generateOTP() :

    digits = "0123456789"
    OTP = ""
    for i in range(4) :
        OTP += digits[math.floor(random.random() * 10)]
 
    return OTP


class CanteenProvider(AsyncWebsocketConsumer):
	async def connect(self):
		print("Connected as Canteen Provider")
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
		text_data_json = json.loads(text_data)
		print(text_data_json)

		if(text_data_json.get("type")=="order"):
			order = text_data_json["order"]
			await self.channel_layer.group_send(
				'all',{
					"type" : "custom_message_handler" ,
					"order" : order ,
				})
		elif(text_data_json.get("type")=="deliver"):
			order = text_data_json["order"]
			await self.channel_layer.group_send(
				order.customer.username,{
					"type" : "deliverOrder" ,
					"order" : order ,
				})
			
		elif (text_data_json.get("type")=="get_new_otp"):
			otp = generateOTP()
			await self.send(text_data=json.dumps({
				"type":"new_otp",
				"otp":otp,
			}))
		elif (text_data_json.get("type")=="avail_item"):
			# await sync_to_async(print)(text_data_json.get("item_name"))
			meal_object = await sync_to_async(Meal.objects.get)(name=text_data_json.get("item_name"))
			meal_object.qunatity_prepared = meal_object.qunatity_prepared + 1
			print(meal_object.qunatity_prepared)
			await sync_to_async(meal_object.save)()

			
		# await self.send(text_data=json.dumps({
		# 	'message': message,
		# 	'username': username,
		# }))
		


	async def sendOrder(self,order) :
		await self.send(json.dumps({"message":order}))
	async def custom_message_handler(self, event):
		await self.sendOrder(event["order"])
		print("Ordered")

	async def deliverOrder(self , order) :
		pass


class CustomerConsumer(AsyncWebsocketConsumer):
	async def connect(self):
		user=self.scope['user']
		user_obj = await sync_to_async(User.objects.get)(username=user.username)
		if(not user.is_authenticated):
			print("Error")
		await self.channel_layer.group_add(
			user_obj.username,
			self.channel_name
        )
		await self.accept()
	
	async def disconnect(self, close_code):
		print("Disconnected ",close_code)
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