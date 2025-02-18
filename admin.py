from db import connect_db
from utils import generatePassword, generate_unique_login

sites = ["Paris","Nantes","Strasbourg","Bordeaux","Tours"] # Définition des sites
roles = ["admin","user"] # Définition des rôles 

def createUser(admin_site): # Création user
    conn = connect_db() # Connexion à la db
    cursor = conn.cursor() # Curseur

    while True: # Boucle infinie
        name = str(input("Nom de l'utilisateur ?\n").upper()) # Nom d'utilisateur en majuscule
        surname = str(input("Prenom de l'utilisateur ?\n").title()) # Pseudo avec la prmeière lettre en majuscule
        if surname != "" and name != "": # Si nom ou pseudo non vice
            break # On casse la boucle
        else: # Sinon (nom vide)
            print("Le nom et le prénom ne peuvent pas être vides") 
    
    if admin_site == "Paris": # Si admin sur Paris
        while (site := input("Où va travailler l'utilisateur ?\n Paris\n Nantes\n Strasbourg\n Bordeaux\n Tours\n").strip()) not in sites: # Si le site saisi n'est pas présent dans sites
            print("Valeur incorrecte, veuillez réessayer") # Erreur : recommencer
    else: # Sinon 
        site = admin_site 
        print(f"En tant qu'admin de {admin_site}, vous ne pouvez créer que des utilisateurs sur votre site.") # Affichage du site d'admin

    if admin_site == "Paris": # Si admin sur paris
        while (status := input("Permissions l'utilisateur ?\n admin \n user\n")) not in roles: # Si le role n'existe pas 
            print("Valeur incorrecte, veuillez réessayer") # Erreur : recommencer
    else:
        status = "user" # Status user 
        print(f"En tant qu'admin de {admin_site}, vous ne pouvez créer que des utilisateurs sur votre site.") 

    if status == "admin":
        cursor.execute("SELECT COUNT(*) FROM users WHERE site = %s AND status = 'admin'", (site,)) # Requete comptant le nombre d'admin pour le site 
        count = cursor.fetchone()[0] # Mise dans une variable
        if count > 0: # Si supérieur à 0
            print(f"Un administrateur existe déjà pour {site}. Impossible d'en créer un autre.")  
            validation = input("\nCréer l'utilisateur en tant que user ? (o/n) : ").strip().lower() # Demande de validation
            if validation == "o": # Vérification de la validation
                status = "user" # Définition du status en user
            else : # Sinon
                return # Return

    login = generate_unique_login(name, surname) # Génération login
    plain_password, hashed_password = generatePassword() # Génération mdp

    sql = "INSERT INTO users (name, surname, login, password, site, status) VALUES (%s, %s, %s, %s, %s, %s)" # Modèle requête pour insérer les infos dans la db  
    values = (name, surname, login, hashed_password, site, status) # On attribue les valeurs dans values
    cursor.execute(sql, values) # Exécution de la requête
    conn.commit() # Commit
    conn.close() # Fermeture de la db

    print(f"Utilisateur {login} créé avec succès !") # Confirmation de création
    print(f"Mot de passe : {plain_password}") # Affichage mdp

    return login # Return login

def list_users(admin_site): # Fonction affichage users
    conn = connect_db() # Connexion db
    cursor = conn.cursor() # Curseur

    if admin_site == "Paris": # Si admin sur paris
        sql = "SELECT login, name, surname, site, status FROM users" # Modèle requête cherchant toutes les données car admin paris
    else:
        sql = "SELECT login, name, surname, site, status FROM users WHERE site = %s" # Sinon modèle requête cherchant seulement sur le site dont est admin le demandeur

    cursor.execute(sql, (admin_site,) if admin_site != "Paris" else None) # Execution de la requête suivant le résultat du if précédent
    users = cursor.fetchall() # Attribution du résultat à la variable users 
    conn.close() # Fermeture db

    if not users: # Si user vide
        print("Aucun utilisateur trouvé.") 
        return

    print("\n--- Liste des utilisateurs ---")
    print(f"{'Login':<15} {'Nom':<15} {'Prénom':<15} {'Site':<10} {'Rôle':<10}") # Affichage des en tête du tableau
    print("=" * 65) # Mise en page
    for login, name, surname, site, status in users: # Boucle pour afficher toutes les lignes 
        print(f"{login:<15} {name:<15} {surname:<15} {site:<10} {status:<10}") # Affichage infos

def modify_user(admin_site): # Fonction modification user
    conn = connect_db() # Connexion db
    cursor = conn.cursor() # Curseur

    login = input("Entrez le login de l'utilisateur à modifier : ")

    sql = "SELECT site FROM users WHERE login = %s" # Modèle requête recherchant le login a modifier
    cursor.execute(sql, (login,)) # Execution requête
    user = cursor.fetchone() # Attribution des infos

    if user: # Si user non vide 
        user_site = user[0] # 

        if admin_site != "Paris" and user_site != admin_site: # Si non admin paris et utilisateur pas sur le site du demandeur
            print("Vous ne pouvez modifier que les utilisateurs de votre site.") # Erreur
        else: # Sinon
            new_name = input("Nouveau nom (laisser vide pour ne pas changer) : ") # Nouveau nom

            new_surname = input("Nouveau prénom (laisser vide pour ne pas changer) : ") # Nouveau pseudo

            new_site = input("Nouveau site (laisser vide pour ne pas changer) : ") # Nouveau site

            if admin_site == "Paris": # Si admin paris
                new_role = input("Nouveau rôle (admin/user, laisser vide pour ne pas changer) : ") # Nouveau rôle

            if new_site != "": # Si nouveau site non vide
                cursor.execute("UPDATE users SET site = %s WHERE login = %s", (new_site, login)) # Modification de la db
            if new_role in ["admin", "user"]: # Si nouveau rôle
                cursor.execute("UPDATE users SET status = %s WHERE login = %s", (new_role, login)) # Modification de la db
            if new_name != "": # Si nouveau nom
                cursor.execute("UPDATE users SET name = %s WHERE login = %s", (new_name, login)) # Modification de la db
            if new_surname != "": # Si nouveau pseudo
                cursor.execute("UPDATE users SET surname = %s WHERE login = %s", (new_surname, login)) # Modification de la db

            conn.commit() # commit
            print("Modification réussie.")
    
    else: # Sinon
        print("Utilisateur non trouvé.") # Erreur
    
    conn.close() # Fermeture db

def delete_user(admin_site): # Suppression user
    conn = connect_db() # Connexion db
    cursor = conn.cursor() # Curseur

    login = input("Entrez le login de l'utilisateur à supprimer : ") # Demande utilisateur

    sql = "SELECT site FROM users WHERE login = %s" # Modèle de requête cherchant le site de l'user
    cursor.execute(sql, (login,)) # Exécution de la requête 
    user = cursor.fetchone() # Attribution du résultat

    if user: # Si user non vice
        user_site = user[0] # Attribution du site à la variable

        if admin_site != "Paris" and user_site != admin_site: # Si demandeur n'est pas admin Paris et n'est pas admin sur le site de l'user
            print("Vous ne pouvez supprimer que les utilisateurs de votre site.") # Action impossible
        else: # Sinon
            cursor.execute("DELETE FROM users WHERE login = %s", (login,)) # Requête supprimant l'utilisateur dans la db
            conn.commit() # commit
            print("Utilisateur supprimé avec succès.") # Confirmation
     
    else: # Sinon
        print("Utilisateur non trouvé.") # Erreur

    conn.close() # Fermeture db