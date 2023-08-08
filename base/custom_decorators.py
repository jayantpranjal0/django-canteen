from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test


def canteen_provider_required(
    function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login'
):
    actual_decorator = user_passes_test(
        lambda u: u.is_active,
        login_url='login',
        redirect_field_name=REDIRECT_FIELD_NAME
    )

    if function :
        return actual_decorator(function)
    return actual_decorator

def customer_required(
    function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login'
):
    actual_decorator = user_passes_test(
        lambda u: u.is_active,
        login_url='login',
        redirect_field_name=REDIRECT_FIELD_NAME
    )

    if function :
        return actual_decorator(function)
    return actual_decorator