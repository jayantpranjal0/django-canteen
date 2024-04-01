from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from base.models import *
import json
import json
from django.core.serializers import serialize


def sendOrder(order):
    channel_layer = get_channel_layer()
    order_items = OrderItem.objects.filter(order=order)
    order_items_json = serialize('json', order_items)
    order_items_data = json.loads(order_items_json)
    order_items_list = []
    for order_item in order_items:
        order_items_list.append({
            'item_id': order_item.meal.id,
            'quantity': order_item.quantity_ordered,
            'item_name': order_item.meal.name
        })

    order_items_json = json.dumps(order_items_list)
    canteen_owner=order_items[0].meal.canteen.canteen_owner
    # print(order_items[0].meal.canteen.canteen_owner)
    # print(order_items_json)
    canteen_owner_username = canteen_owner.username
    async_to_sync(channel_layer.group_send)(
        canteen_owner_username,
        {
            "type": "custom_message_handler",
            "event": "New Order",
            "order": order_items_json,
        },
    )




def sendOrderRequirements(canteen):
    channel_layer = get_channel_layer()
    order_items = Order.get_items_to_be_delivered(canteen)
    items = {}
    for i, j in order_items.items():
        items[str(i)] = j
    print(items)
    context = {'order_items': items}
    canteen_owner_username = canteen.canteen_owner.username
    async_to_sync(channel_layer.group_send)(
        canteen_owner_username,
        {
            "type": "custom_message_handler",
            "event": "New Order",
            "order": items,
        },
    )
