from urllib.parse import parse_qs

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.db import close_old_connections

from channels.auth import AuthMiddleware
from channels.db import database_sync_to_async
from channels.sessions import CookieMiddleware, SessionMiddleware
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_api_key.models import APIKey
from trips.models import UserAPIKey

User = get_user_model()

@database_sync_to_async
def get_user(scope):
    close_old_connections()

    if b'authorization' in dict(scope['headers']):
        print("authorization")
        try:
            apikey_name, apikey = dict(scope['headers'])[b'authorization'].decode().split()
            if apikey_name == 'Api-Key':
                user_apikey = UserAPIKey.objects.get_from_key(apikey)
                user = User.objects.get(api_keys=user_apikey)
                return user
        except Exception as exception:
            print(exception)
            return AnonymousUser()

    if scope['query_string']:
        try:
            token_name, token_key = scope['query_string'].decode().split("=")
            if not token_key:
                return AnonymousUser()
            try:
                access_token = AccessToken(token_key)
                user = User.objects.get(id=access_token['id'])
            except Exception as exception:
                return AnonymousUser()
            if not user.is_active:
                return AnonymousUser()
            return user
        except Exception as exception:
            print(exception)
            return AnonymousUser()

class TokenAuthMiddleware(AuthMiddleware):
    async def resolve_scope(self, scope):
        scope['user']._wrapped = await get_user(scope)

def TokenAuthMiddlewareStack(inner):
    return CookieMiddleware(SessionMiddleware(TokenAuthMiddleware(inner)))
