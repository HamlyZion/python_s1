from db import connect_db
from utils import generatePassword
import bcrypt
import getpass

def change_password(login, admin_override=False, admin_site=None):
    conn = connect_db()
    cursor = conn.cursor()

    if admin_override:
        target_login = input("Entrez le login de l'utilisateur dont vous voulez modifier le mot de passe : ")

        sql = "SELECT login, site FROM users WHERE login = %s"
        cursor.execute(sql, (target_login,))
        user = cursor.fetchone()

        if not user:
            print("Utilisateur non trouvé.")
            conn.close()
            return
        
        user_site = user[1]

        if admin_site != "Paris" and user_site != admin_site:
            print(f"Vous ne pouvez modifier que les utilisateurs du site {admin_site}.")
            conn.close()
            return

        plain_password, hashed_password = generatePassword()
        cursor.execute("UPDATE users SET password = %s WHERE login = %s", (hashed_password, target_login))
        conn.commit()
        conn.close()
        
        print(f"Nouveau mot de passe de {target_login} : {plain_password}")
    else:
        target_login = login
        print("Changement de votre mot de passe")
        while True:
            current_password = getpass.getpass("Entrez votre mot de passe actuel : ")
            sql = "SELECT password FROM users WHERE login = %s"
            cursor.execute(sql, (target_login,))
            stored_password = cursor.fetchone()

            if bcrypt.checkpw(current_password.encode('utf-8'), stored_password[0].encode('utf-8')):
                break
            else:
                print("Mot de passe actuel incorrect.")

        while True:
            new_password = getpass.getpass("Entrez un nouveau mot de passe : ")

            if len(new_password) < 12:
                print("Mot de passe trop court. Minimum 12 caractères.")
                continue
            if not any(char.isupper() for char in new_password):
                print("Le mot de passe doit contenir au moins une majuscule.")
                continue
            if not any(char.isdigit() for char in new_password):
                print("Le mot de passe doit contenir au moins un chiffre.")
                continue
            if not any(char in "!@#$%^&*()-_=+<>?/|{}[]" for char in new_password):
                print("Le mot de passe doit contenir au moins un caractère spécial.")
                continue

            confirm_password = getpass.getpass("Confirmez le nouveau mot de passe : ")

            if new_password == confirm_password:
                hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                sql = "UPDATE users SET password = %s WHERE login = %s"
                cursor.execute(sql, (hashed_password, target_login))
                conn.commit()
                conn.close()
                print(f"Mot de passe de {target_login} changé avec succès !")
                break
            else:
                print("Erreur : les mots de passe ne correspondent pas.")


def logon():
    conn = connect_db()
    cursor = conn.cursor()

    login = input("Entrez votre identifiant : ")

    sql = "SELECT id, name, surname, password, site, status, logon_count FROM users WHERE login = %s"
    cursor.execute(sql, (login,))
    user = cursor.fetchone()
    
    if user:
        user_id, name, surname, password, site, status, logon_count = user

        for tentative in range(3):
        
            entered_password = getpass.getpass("Entrez votre mot de passe : ")

            if bcrypt.checkpw(entered_password.encode('utf-8'), password.encode('utf-8')):
                print(f"Connexion réussie. Bienvenue, {surname} !")

                if logon_count == 0:
                    print("Vous devez définir un nouveau mot de passe.")
                    change_password(login)

                sql_update = "UPDATE users SET logon_count = logon_count + 1 WHERE id = %s"
                cursor.execute(sql_update, (user_id,))
                conn.commit()

                conn.close()
                return user_id, name, surname, login, site, status
            else:
                print("Mot de passe incorrect.")
                if tentative == 2:
                    print("3 tentatives échouées, retour au menu")
                    return                    
    else:
        print("Utilisateur non trouvé.")
        conn.close()
        return
    
    