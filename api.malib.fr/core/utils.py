import random, re, datetime
from core import conf, schemas
from uuid import UUID, uuid4
from fastapi_jwt_auth import AuthJWT

def debug(msg:str):
    print(f"\033[94mDEBUG\033[00m:    {msg}")

def generate_referral_code() -> str:
    custom_base = conf.REFERRAL_CHARSET
    ref_code = ""
    for i in range(conf.REFERRAL_CODE_LENGTH):
        ref_code += custom_base[random.randint(0, len(custom_base)-1)]
    return ref_code

def camel_to_snake(string: str) -> str:
    string = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", string)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", string).lower()

def get_anon_values():
    return "deleted-account-" + str(uuid4()), "deleted-account"

def create_access_token(auth:AuthJWT, user_id:UUID) -> schemas.AccessToken:
    if user_id in conf.ADMINS:
        expiration = conf.EXPIRATION_ACCESS_TOKEN_ADMIN
    else:
        expiration = conf.EXPIRATION_ACCESS_TOKEN
    atoken = auth.create_access_token(subject=str(user_id), expires_time=datetime.timedelta(seconds=expiration))
    return schemas.AccessToken(access_token=atoken)
