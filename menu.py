from user import logon, change_password # Import des fonctions de user
from admin import createUser, list_users, modify_user, delete_user # Import des fonctions de admin

def main_menu(): # Main
    while True: # Boucle infinie
        print("\n=== MENU PRINCIPAL ===")
        print("1. Se connecter")
        print("2. Quitter") 

        choice = input("Votre choix : ") # Choix utilisateur

        if choice == "1": # Choix "se connecter"
            user_data = logon() # login 

            if user_data is not None: # si logon n'est pas vice 
                user_id, name, surname, login, site, status = user_data # On mets les valeurs dans les bonnes variables 
                while True: # Boucle infinie
                    print("\n=== MENU UTILISATEUR ===") # Menu utilisateur
                    print("1. Afficher mon profil")
                    print("2. Changer mon mot de passe")
                    if status == "admin": # En cas d'utilisateur admin
                        print("3. Créer un nouvel utilisateur")
                        print("4. Lister les utilisateurs")
                        print("5. Modifier un utilisateur")
                        print("6. Supprimer un utilisateur")
                        print("7. Changer le mot de passe d'un utilisateur") 
                    print("8. Déconnexion")

                    sub_choice = input("Votre choix : ") # Sous choix

                    if sub_choice == "1": 
                        print(f"\n--- Profil ---\nNom : {name}\nPrénom : {surname}\nLogin : {login}\nSite : {site}\nRôle : {status}") # Affichage de profil

                    elif sub_choice == "2":
                        change_password(login) # Changement mdp

                    elif sub_choice == "3" and status == "admin": # Si demandeur admin
                        createUser(site) # Création utilisateur

                    elif sub_choice == "4" and status == "admin": # Si demandeur admin
                        list_users(site) # Liste des utilisateurs

                    elif sub_choice == "5" and status == "admin": # Si demandeur admin
                        modify_user(site) # Modification d'un utilisateur

                    elif sub_choice == "6" and status == "admin": # Si demandeur admin
                        delete_user(site) # Suppression d'un utilisateur

                    elif sub_choice == "7" and status == "admin": # Si demandeur admin
                        change_password(login, admin_override=True, admin_site=site) # Changement de mdp

                    elif sub_choice == "8": # Choix déconnexion
                        print("Déconnexion réussie.")
                        break # On casse la boucle

                    else:
                        print("Option invalide, veuillez réessayer.") # Si choix inccorect
            else:
                print("Connexion echouée.") # Si choix incorrect
    
        elif choice == "2":
            print("Au revoir !") # Déconnexion
            break # On casse la boucle

        else:
            print("Option invalide, veuillez réessayer.") # Si choix incorrect
