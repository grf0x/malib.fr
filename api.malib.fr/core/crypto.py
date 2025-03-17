import bcrypt, base64
from Crypto.Cipher import AES

def hash_password(password : str) -> str:
    return bcrypt.hashpw(password.encode("utf-8", "replace"), bcrypt.gensalt(8)).decode()

def is_valid_password(password : str, hashed_password : str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8", "replace"), hashed_password.encode())

def decode_sec(name: str) -> str:
    sec, iv = open("****REDACTED****"+name).read().split("/")
    cipher = AES.new(base64.b85decode(open("****REDACTED****").read().encode("utf-8")), AES.MODE_CFB, iv=base64.b85decode(iv.encode("utf-8")))
    return cipher.decrypt(base64.b85decode(sec.encode("utf-8"))).decode("utf-8")
