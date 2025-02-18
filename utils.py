import random
import string
import bcrypt
from db import connect_db #Import fonction connect dans fichier db.py

def generatePassword(): # Génération mdp 
    length=int(input("Longueur du mot de passe ?\n")) # Choix de la longueur
    characters = string.ascii_uppercase.replace("O", "").replace("I", "") + \
                 string.ascii_lowercase.replace("l", "") + \
                 string.digits.replace("0", "") + \
                 string.punctuation # exclusion de O I 1 et 0 
    
    plain_password = ''.join(random.choice(characters) for _ in range(length)) # Création du mdp aléatoire en suivant la longueur saisie et les caractères exclus
    hashed_password = bcrypt.hashpw(plain_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8') # hashage du mdp
 
    return plain_password, hashed_password # Renvoie le mdp et son hash

def generate_unique_login(name, surname): # Génération login 
    conn = connect_db() # Connexion db
    cursor = conn.cursor() # placement curseur

    base_login = (surname[0] + name).lower() # Initale prénom + nom en minuscule
    login = base_login 

    cursor.execute("SELECT login FROM users WHERE login LIKE %s ORDER BY login DESC LIMIT 1", (base_login + '%',)) # On cherche un login du même nom
    last_login = cursor.fetchone() # on stocke ce login

    if last_login: # Si un login équivalent est trouvé
        last_login = last_login[0] # Premier caractère
        if last_login[len(base_login):].isdigit(): # Si le dernier caractère du login est un chiffre
            counter = int(last_login[len(base_login):]) + 1 # On prend le chiffre et ajoute 1
        else: # Sinon 
            counter = 1 # Compteur = 1
        login = f"{base_login}{counter}" # On modifie le login pour y ajouter le compteur
    
    return login # On retourne login