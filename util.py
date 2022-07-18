import bcrypt


def hash_password(plain_text_password):
    hashed_password = bcrypt.hashpw(plain_text_password.encode('utf_8'), bcrypt.gensalt())
    return hashed_password.decode('utf-8')


def verify_password(user_input_password, hashed_password):
    hashed_bytes_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(user_input_password.encode('utf-8'), hashed_bytes_password)

