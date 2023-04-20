import jwt
from django.http import JsonResponse
from jwt import ExpiredSignatureError, InvalidSignatureError, DecodeError

from api.jwt_handler import checkToken


class JWTMiddleware:
  def __init__(self, get_response):
    self.get_response = get_response

  def __call__(self, request):

    if request.path in ['/api/auth/login', '/api/auth/register']:
      return self.get_response(request)

    # token = request.headers.get('Authorization')
    token = request.headers.get('x-token')
    if not token:
      return JsonResponse({'ok': False, 'message': 'Token not found'}, status=400)

    try:
      payload = checkToken(token)
      request.user = payload

    except ExpiredSignatureError:
      return JsonResponse({'error': 'Token has expired'}, status=401)

    except (InvalidSignatureError, IndexError, DecodeError):
      return JsonResponse({'error': 'Invalid token'}, status=400)

    response = self.get_response(request)

    return response
