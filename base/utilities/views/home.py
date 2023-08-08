from .imports import *


@login_required()
@customer_required()
def home(request):
    context = {"canteens": Canteen.all()}
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'jayant_pranjal',
        {
            'type': 'custom_message_handler',
            'text': json.dumps({
                "message": "Test Message",
            })
        }
    )
    return render(request, 'base/home_page.html', context)