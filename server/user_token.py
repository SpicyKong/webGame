from cryptography.fernet import Fernet

KEY=b'[KEY]'
fernet=Fernet(KEY)

def encrypt_token(data):
    return fernet.encrypt(bytes(data, "utf-8"))

def decrypt_token(query):
    t=fernet.decrypt(bytes(query, "utf-8"))
    try:
        t=int(t)
    except: return None
    return t

def get_user(t):
    t=fernet.decrypt(bytes(t, "utf-8"))
    return int(t) 