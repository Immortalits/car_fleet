from werkzeug.security import safe_str_cmp
from models.user import UserModel
import hashlib

salt = "uBoRkASaLATa"


def hash_password(password):
    hashed_password = hashlib.sha512(
        password.encode('utf-8') + salt.encode('utf-8')).hexdigest()
    return hashed_password


def authenticate(username, password):
    user = UserModel.find_by_attribute(username=username)
    if user and safe_str_cmp(user.password, hash_password(password)):
        return user


def identity(payload):
    # payload info is extracted from the token...
    # print(payload)
    user_id = payload['identity']
    return UserModel.find_by_attribute(id=user_id)