import jwt
from datetime import datetime, timedelta


def createToken(userObj):
  secret_key = 'SECRET'
  expiration_time = datetime.utcnow() + timedelta(days=1)
  payload = {
    'username': userObj['name'],
    'userId': userObj['id'],
    'exp': expiration_time
  }
  token = jwt.encode(payload, secret_key)
  return token


def checkToken(token):
  return jwt.decode(token, 'SECRET', algorithms=['HS256'])
