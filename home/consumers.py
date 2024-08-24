from channels.generic.websocket import AsyncWebsocketConsumer
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync,sync_to_async
import json
from .models import *


class OrderConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.group_name='order_data'
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self,close_code):
        pass

    async def receive(self,text_data):
        # print (text_data)
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type':'send_order',
                'value':text_data,
            }
        )

    async def send_order(self,event):
        print (event['value'])
        await self.send(event['value'])
        
        

class OrderProgress(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['order_id']
        self.room_group_name = f'order_{self.room_name}'

        await self.accept()

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # Fetch the order details
        order = await sync_to_async(Order.give_order_details)(self.room_name)
        
        # Ensure the payload is correctly structured
        await self.send(text_data=json.dumps({
            'order_id': order.get('order_id', 'N/A'),
            'amount': order.get('amount', 'N/A'),
            'status': order.get('status', 'Pending')
        }))

async def order_status(self, event):
    data = json.loads(event['value'])
    await self.send(text_data=json.dumps({
        'order_id': data.get('order_id', 'N/A'),
        'amount': data.get('amount', 'N/A'),
        'status': data.get('status', 'Pending')
    }))
