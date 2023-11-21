from functools import wraps
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden

def user_must_be_subscribed(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Assuming your user profile model has a field named 'is_subscribed'
        if request.user.is_authenticated and request.user.profile.is_premium:
            # User is subscribed, allow access to the view
            return view_func(request, *args, **kwargs)
        else:
            # User is not subscribed, deny access
            return HttpResponseForbidden("You must be subscribed to access this view.")
    return _wrapped_view