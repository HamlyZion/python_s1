from db import connect_db
from utils import generatePassword, generate_unique_login

sites = ["Paris","Nantes","Strasbourg","Bordeaux","Tours"]
roles = ["admin","user"]

def createUser(admin_site):
    conn = connect_db()
    cursor = conn.cursor()

    name = input("Nom de l'utilisateur ?\n").upper()
    surname = input("Prenom de l'utilisateur ?\n").title()
    
    if admin_site == "Paris":
        while (site := input("Où va travailler l'utilisateur ?\n Paris\n Nantes\n Strasbourg\n Bordeaux\n Tours\n").strip()) not in sites:
            print("Valeur incorrecte, veuillez réessayer")
    else:
        site = admin_site
        print(f"En tant qu'admin de {admin_site}, vous ne pouvez créer que des utilisateurs sur votre site.")

    if admin_site == "Paris":
        while (status := input("Permissions l'utilisateur ?\n admin \n user\n")) not in roles:
            print("Valeur incorrecte, veuillez réessayer")
    else:
        status = "user"
        print(f"En tant qu'admin de {admin_site}, vous ne pouvez créer que des utilisateurs sur votre site.")

    if status == "admin":
        cursor.execute("SELECT COUNT(*) FROM users WHERE site = %s AND status = 'admin'", (site,))
        count = cursor.fetchone()[0]
        if count > 0:
            print(f"Un administrateur existe déjà pour {site}. Impossible d'en créer un autre.")
            validation = input("\nCréer l'utilisateur en tant que user ? (o/n) : ").strip().lower()
            if validation == "o":
                status = "user"
            else :
                return

    login = generate_unique_login(name, surname)
    plain_password, hashed_password = generatePassword()

    sql = "INSERT INTO users (name, surname, login, password, site, status) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (name, surname, login, hashed_password, site, status)
    cursor.execute(sql, values)
    conn.commit()
    conn.close()

    print(f"Utilisateur {login} créé avec succès !")
    print(f"Mot de passe : {plain_password}")

    return login

def list_users(admin_site):
    conn = connect_db()
    cursor = conn.cursor()

    if admin_site == "Paris":
        sql = "SELECT login, name, surname, site, status FROM users"
    else:
        sql = "SELECT login, name, surname, site, status FROM users WHERE site = %s"

    cursor.execute(sql, (admin_site,) if admin_site != "Paris" else None)
    users = cursor.fetchall()
    conn.close()

    if not users:
        print("Aucun utilisateur trouvé.")
        return

    print("\n--- Liste des utilisateurs ---")
    print(f"{'Login':<15} {'Nom':<15} {'Prénom':<15} {'Site':<10} {'Rôle':<10}")
    print("=" * 65)
    for login, name, surname, site, status in users:
        print(f"{login:<15} {name:<15} {surname:<15} {site:<10} {status:<10}")

def modify_user(admin_site):
    conn = connect_db()
    cursor = conn.cursor()

    login = input("Entrez le login de l'utilisateur à modifier : ")

    sql = "SELECT site FROM users WHERE login = %s"
    cursor.execute(sql, (login,))
    user = cursor.fetchone()

    if user:
        user_site = user[0]

        if admin_site != "Paris" and user_site != admin_site:
            print("Vous ne pouvez modifier que les utilisateurs de votre site.")
        else:
            new_site = input("Nouveau site (laisser vide pour ne pas changer) : ")
            new_role = input("Nouveau rôle (admin/user, laisser vide pour ne pas changer) : ")

            if new_site:
                cursor.execute("UPDATE users SET site = %s WHERE login = %s", (new_site, login))
            if new_role in ["admin", "user"]:
                cursor.execute("UPDATE users SET status = %s WHERE login = %s", (new_role, login))

            conn.commit()
            print("Modification réussie.")
    
    else:
        print("Utilisateur non trouvé.")
    
    conn.close()

def delete_user(admin_site):
    conn = connect_db()
    cursor = conn.cursor()

    login = input("Entrez le login de l'utilisateur à supprimer : ")

    sql = "SELECT site FROM users WHERE login = %s"
    cursor.execute(sql, (login,))
    user = cursor.fetchone()

    if user:
        user_site = user[0]

        if admin_site != "Paris" and user_site != admin_site:
            print("Vous ne pouvez supprimer que les utilisateurs de votre site.")
        else:
            cursor.execute("DELETE FROM users WHERE login = %s", (login,))
            conn.commit()
            print("Utilisateur supprimé avec succès.")
    
    else:
        print("Utilisateur non trouvé.")

    conn.close()