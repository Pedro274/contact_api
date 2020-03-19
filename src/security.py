from werkzeug.security import safe_str_cmp

from auth_user import User
import uuid

users = [
    User(str(uuid.uuid4), 'Pedro', 'asdf'),
    User(str(uuid.uuid4), 'Hernandez', 'asdf'),
]

username_table = {user.username: user for user in users}
userid_table = {user.id: user for user in users}


def authenticate(username, password):
    user = username_table.get(username, None)
    if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
        return user


def identity(payload):
    user_id = payload['identity']
    return userid_table.get(user_id, None)
