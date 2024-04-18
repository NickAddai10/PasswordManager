import mysql.connector
import username
from mysql.connector import Error
import user_registration
import password_management

def main_menu():
    connection = user_registration.create_connection()
    if connection:
        user_registration.create_users_table(connection)
        while True:
            print("\nMenu:")
            print("1. Register")
            print("2. Login")
            print("3. Exit")
            choice = input("Enter your choice: ")
            if choice == "1":
                user_registration.register_login(connection)
                password_management.create_passwords_table(connection)
            elif choice == "2":
                user_id = user_registration.login(connection)  # Obtain the user_id from login
                password_management.update_password_table(connection, user_id)
                if user_id:
                    password_management_menu(connection, user_id)  # Pass the user_id to password management menu
                    break
                else:
                    print("Login failed.")
            elif choice == "3":
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please try again.")


# Password management menu function
def password_management_menu(connection, user_id):
    while True:
        print("\nPassword Management Menu:")
        print("1. View Saved Passwords")
        print("2. Add New Password")
        print("3. Update Password")
        print("4. Delete Password")
        print("5. Logout")
        choice = input("Enter your choice: ")
        if choice == "1":
            password_management.display_saved_passwords(connection, user_id)
        elif choice == "2":
            password_management.store_password_menu(connection, user_id)
        elif choice == "3":
            password_management.update_password_menu(connection,)
        elif choice == "4":
            password_management.delete_password_menu(connection,)
        elif choice == "5":
            print("Logging out...")
            return True  # Return True to indicate logout
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    while True:
        main_menu()
        # If main_menu() returns, the user has logged out
        print("Returning to main menu...")
