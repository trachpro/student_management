import datetime
import jwt

JWT_SECRET = 'YOUR_SECRET_STRING'


def encode(account):
    iat = datetime.datetime.utcnow()
    return jwt.encode({
        'id': account['id'],
        'role': account['role'],
        'iat': iat,
        'exp': iat + datetime.timedelta(days=365)
    }, JWT_SECRET).decode('utf-8')


def decode(access_token):
    try:
        token = jwt.decode(access_token, JWT_SECRET, leeway=10)
    except jwt.InvalidTokenError:
        return None
    return token