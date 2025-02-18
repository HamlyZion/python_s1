from db import connect_db
from utils import generatePassword
import bcrypt
import getpass

def change_password(login, admin_override=False, admin_site=None): # Changement de passwd
    conn = connect_db() # Connexion à la DB
    cursor = conn.cursor() # Curseur

    if admin_override: # Si demandeur est admin
        target_login = input("Entrez le login de l'utilisateur dont vous voulez modifier le mot de passe : ") # utilisateur cible

        sql = "SELECT login, site FROM users WHERE login = %s" # Requête cherchant le login cible
        cursor.execute(sql, (target_login,)) # Execution de la reqête
        user = cursor.fetchone()  # User = ligne de mysql correspondante à ce nom

        if not user: # Si l'utilisateur est introuvable
            print("Utilisateur non trouvé.")
            conn.close() # On ferme la db
            return
        
        user_site = user[1] # Le site de l'utilisateur

        if admin_site != "Paris" and user_site != admin_site: # Si le site de l'admin est différent de celui de l'user cible    
            print(f"Vous ne pouvez modifier que les utilisateurs du site {admin_site}.") # Affichage du message
            conn.close() # On ferme la db
            return

        plain_password, hashed_password = generatePassword()  # Génération du mdp
        cursor.execute("UPDATE users SET password = %s WHERE login = %s", (hashed_password, target_login)) # Envoie du hash dans la db
        conn.commit() 
        conn.close()
        
        print(f"Nouveau mot de passe de {target_login} : {plain_password}") # Affichage du mdp
    else: # Sinon (user)
        target_login = login
        print("Changement de votre mot de passe")
        while True: # boucle infinie
            current_password = getpass.getpass("Entrez votre mot de passe actuel : ") # Input masqué du mdp
            sql = "SELECT password FROM users WHERE login = %s" # Modèle de requête pour récupérer le mdp
            cursor.execute(sql, (target_login,)) # On exécute la requête pour récupérer le mdp dans la db
            stored_password = cursor.fetchone() # On stocke le mdp haséh dans une variable

            if bcrypt.checkpw(current_password.encode('utf-8'), stored_password[0].encode('utf-8')): # Si mdp saisi correspond au mdp de la db
                break # On casse la boucle 
            else: # Sinon
                print("Mot de passe actuel incorrect.") # Retour au début de la boucle 

        while True:
            new_password = getpass.getpass("Entrez un nouveau mot de passe : ") # On stocke dans une variable le nouveau mdp

            if len(new_password) < 12: # Si la taille de la str est inférieure à 8
                print("Mot de passe trop court. Minimum 12 caractères.") 
                continue
            if not any(char.isupper() for char in new_password): # Si le mdp n'a pas de majuscule
                print("Le mot de passe doit contenir au moins une majuscule.")
                continue
            if not any(char.isdigit() for char in new_password): # Si le mdp n'a pas de chiffre
                print("Le mot de passe doit contenir au moins un chiffre.")
                continue
            if not any(char in "!@#$%^&*()-_=+<>?/|{}[]" for char in new_password): # Si le mdp n'a pas de caractère spécial
                print("Le mot de passe doit contenir au moins un caractère spécial.")
                continue

            confirm_password = getpass.getpass("Confirmez le nouveau mot de passe : ") # confirmation du mdp

            if new_password == confirm_password: # Si les deux mdp correspondent
                hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8') # On hash le nouveau mdp
                sql = "UPDATE users SET password = %s WHERE login = %s" # modèle pour modification de la db
                cursor.execute(sql, (hashed_password, target_login)) # On envoie la requête pour modifier le mdp dans la db
                conn.commit() # On commit
                conn.close() # On ferme la db
                print(f"Mot de passe de {target_login} changé avec succès !") # On confirme l'exécution
                break # On casse la boucle
            else: # Sinon
                print("Erreur : les mots de passe ne correspondent pas.") # On recommence


def logon():
    conn = connect_db() # Connexion à la db
    cursor = conn.cursor() # Variable pour le curseur

    login = input("Entrez votre identifiant : ") # Demande du login

    sql = "SELECT id, name, surname, password, site, status, logon_count FROM users WHERE login = %s" # Modeèle de requête où l'on récupère toutes les infos d'un user
    cursor.execute(sql, (login,)) # Envoie de la requête
    user = cursor.fetchone() # On prend le premier élément répondant aux critères et on stocke la ligne dans user
    
    if user:
        user_id, name, surname, password, site, status, logon_count = user # On réassigne les valeurs aux bonnes variables

        for tentative in range(3): # Pour 4 tentatives : 
        
            entered_password = getpass.getpass("Entrez votre mot de passe : ") # On masque le mdp lorsqu'il est saisi

            if bcrypt.checkpw(entered_password.encode('utf-8'), password.encode('utf-8')): # Si le passord correspond
                print(f"Connexion réussie. Bienvenue, {surname} !") # On confirme l'accès

                if logon_count == 0: # Si le nombre de connexion est de 0
                    print("Vous devez définir un nouveau mot de passe.") 
                    change_password(login) # Changement de mdp 

                sql_update = "UPDATE users SET logon_count = logon_count + 1 WHERE id = %s" # Modèle de requête pour incrémenter le logon_count
                cursor.execute(sql_update, (user_id,)) # On envoie la requête 
                conn.commit() # On commit la modif

                conn.close() # On ferme la db
                return user_id, name, surname, login, site, status # On renvoie les valeurs à jour
            else: # Sinon 
                print("Mot de passe incorrect.")
                if tentative == 2:  # Si 3e tentative échouées
                    print("3 tentatives échouées, retour au menu") 
                    return                    
    else: # Sinon 
        print("Utilisateur non trouvé.") 
        conn.close() # On ferme la db
        return
    
    