from pprint import pprint

from django.db import IntegrityError
from django.http import JsonResponse
from django.views import View
from django.forms.models import model_to_dict
from django.utils.decorators import method_decorator
from django.contrib.auth.hashers import make_password, check_password
from django.views.decorators.csrf import csrf_exempt
from .jwt_handler import createToken
import json

from api.models import Book, User
from datetime import datetime


class UserView(View):

  def get(self, request):
    users = list(User.objects.all().values())

    for user in users:
      del user['password']
      user['booksCount'] = Book.objects.filter(user_id=user['id']).count()
    response = {
      'ok': True,
      'users': users
    }

    return JsonResponse(response)


class BookView(View):

  @method_decorator(csrf_exempt)
  def dispatch(self, request, *args, **kwargs):
    return super().dispatch(request, *args, **kwargs)

  def get(self, request):
    userId = request.user['userId']
    books = list(Book.objects.filter(user_id=userId).values())
    response = {
      'ok': True,
      'books': books
    }
    return JsonResponse(response)

  def post(self, request):
    try:
      requestBody = json.loads(request.body)
      userId = request.user['userId']
      createdBook = Book.objects.create(
        author=requestBody['author'],
        isbn=requestBody['isbn'],
        release_date=datetime.fromisoformat(requestBody['release_date']),
        title=requestBody['title'],
        user_id=userId
      )
      response = {
        'ok': True,
        'createdBookId': createdBook.id
      }
      return JsonResponse(response, status=201)
    except IntegrityError as e:
      return JsonResponse({'ok': False})

  def delete(self, request, id):
    response = Book.objects.filter(id=id).delete()
    if response[0]:
      return JsonResponse({'ok': True, 'message': 'Book deleted'}, status=202)

    return JsonResponse({'ok': False, 'message': 'Book not found'}, status=404)

  def put(self, request, id):
    requestBody = json.loads(request.body)
    response = Book.objects.filter(id=id).update(**requestBody)
    if not response:
      return JsonResponse({'ok': False, 'message': 'Book not found'}, status=404)

    return JsonResponse({'ok': True, 'message': 'Book updated'}, status=201)



class AuthView(View):

  @method_decorator(csrf_exempt)
  def dispatch(self, request, *args, **kwargs):
    return super().dispatch(request, *args, **kwargs)

  def post(self, request, *args, **kwargs):
    print(request.path)
    if '/api/auth/login' == request.path:
      return self.login(request)

    if '/api/auth/register' == request.path:
      return self.register(request)

    if '/api/auth/checktoken' == request.path:
      return self.checkTokenUser(request)

    return JsonResponse({'ok': False, 'message': 'Invalid endpoint'}, status=404)

  def register(self, request):
    try:
      requestBody = json.loads(request.body)
      createdUser = User.objects.create(
        name=requestBody['name'],
        email=requestBody['email'],
        password=make_password(requestBody['password'])
      )
      response = {
        'ok': True,
      }
      return JsonResponse(response)
    except Exception as e:
      print(e)
      return JsonResponse({'ok': False, 'message': 'Algo fall'})

  def login(self, request):
    requestBody = json.loads(request.body)
    userInDB = User.objects.filter(email=requestBody['email']).values().first()
    if not userInDB:
      return JsonResponse({'ok': False, 'message': 'User not found'}, status=404)

    if not check_password(requestBody['password'], userInDB['password']):
      return JsonResponse({'ok': False, 'message': 'Incorrect credentials'}, status=403)

    userToken = createToken(userInDB)
    return JsonResponse({'ok': True, 'token': userToken, 'userName': userInDB['name']})

  def checkTokenUser(self, request):
    print(request.user)
    return JsonResponse({'ok': True, 'user': request.user})



