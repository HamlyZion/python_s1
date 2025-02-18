from user import logon, change_password
from admin import createUser, list_users, modify_user, delete_user

def main_menu():
    while True:
        print("\n=== MENU PRINCIPAL ===")
        print("1. Se connecter")
        print("2. Quitter")

        choice = input("Votre choix : ")

        if choice == "1":
            user_data = logon()

            if user_data is not None:
                user_id, name, surname, login, site, status = user_data
                while True:
                    print("\n=== MENU UTILISATEUR ===")
                    print("1. Afficher mon profil")
                    print("2. Changer mon mot de passe")
                    if status == "admin":
                        print("3. Créer un nouvel utilisateur")
                        print("4. Lister les utilisateurs")
                        print("5. Modifier un utilisateur")
                        print("6. Supprimer un utilisateur")
                        print("7. Changer le mot de passe d'un utilisateur") 
                    print("8. Déconnexion")

                    sub_choice = input("Votre choix : ")

                    if sub_choice == "1":
                        print(f"\n--- Profil ---\nNom : {name}\nPrénom : {surname}\nLogin : {login}\nSite : {site}\nRôle : {status}")

                    elif sub_choice == "2":
                        change_password(login)

                    elif sub_choice == "3" and status == "admin":
                        createUser(site)

                    elif sub_choice == "4" and status == "admin":
                        list_users(site)

                    elif sub_choice == "5" and status == "admin":
                        modify_user(site)

                    elif sub_choice == "6" and status == "admin":
                        delete_user(site)

                    elif sub_choice == "7" and status == "admin":
                        change_password(login, admin_override=True, admin_site=site)

                    elif sub_choice == "8":
                        print("Déconnexion réussie.")
                        break

                    else:
                        print("Option invalide, veuillez réessayer.")
            else:
                print("Connexion echouée.")
    
        elif choice == "2":
            print("Au revoir !")
            break

        else:
            print("Option invalide, veuillez réessayer.")
