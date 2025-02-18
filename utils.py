import random
import string
import bcrypt
from db import connect_db

def generatePassword():
    length=int(input("Longueur du mot de passe ?\n"))
    characters = string.ascii_uppercase.replace("O", "").replace("I", "") + \
                 string.ascii_lowercase.replace("l", "") + \
                 string.digits.replace("0", "") + \
                 string.punctuation
    
    plain_password = ''.join(random.choice(characters) for _ in range(length))
    hashed_password = bcrypt.hashpw(plain_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
 
    return plain_password, hashed_password

def generate_unique_login(name, surname):
    conn = connect_db()
    cursor = conn.cursor()

    base_login = (surname[0] + name).lower()
    login = base_login

    cursor.execute("SELECT login FROM users WHERE login LIKE %s ORDER BY login DESC LIMIT 1", (base_login + '%',))
    last_login = cursor.fetchone()

    if last_login:
        last_login = last_login[0]
        if last_login[len(base_login):].isdigit():
            counter = int(last_login[len(base_login):]) + 1
        else:
            counter = 1
        login = f"{base_login}{counter}"
    
    return login