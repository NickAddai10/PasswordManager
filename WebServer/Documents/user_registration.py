import mysql.connector
from mysql.connector import Error
import hashlib
import bcrypt
import argon2
import uuid

# Establish a connection to the MySQL database
def create_connection():
    try:
        connection = mysql.connector.connect(
            host='127.0.0.1',
            database='password_manager',
            user='Nick',
            password='Season8TBD!',
            auth_plugin='mysql_native_password'
        )
        print("Connected to MySQL database")
        return connection
    except Error as e:
        print(f"Error connecting to MySQL database: {e}")
        return None

# Create a table to store user credentials
def create_users_table(connection):
    try:
        cursor = connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS Users (
            UserID VARCHAR(36) PRIMARY KEY,
            Username VARCHAR(50) UNIQUE NOT NULL,
            Password VARCHAR(255) NOT NULL,
            BcryptHash VARCHAR(255) NOT NULL DEFAULT ''
        )
        """
        cursor.execute(create_table_query)
        connection.commit()
        cursor.close()
        print("Users table created successfully")
    except Error as e:
        print(f"Error creating Users table: {e}")

# Function to store username, password, and bcrypt hash in the database
def store_login(connection, user_id, username, hashed_password, bcrypt_hash=None):
    try:
        cursor = connection.cursor()
        insert_query = "INSERT INTO Users (UserID, Username, Password, BcryptHash) VALUES (%s, %s, %s, %s)"

        # Ensure bcrypt_hash is not None
        if bcrypt_hash is None:
            bcrypt_hash = ''

        cursor.execute(insert_query, (user_id, username, hashed_password, bcrypt_hash))
        connection.commit()
        cursor.close()
        print("Username, password, and bcrypt hash stored successfully in the database")
    except Error as e:
        print(f"Error storing username, password, and bcrypt hash: {e}")

# Function to prompt user for choice of password hashing method
def prompt_hashing_method(previous_choice=None):
    print("Choose Your Hashing Methods:")
    print("1. SHA-256")
    print("2. Bcrypt")
    print("3. Argon2")
    while True:
        try:
            choice = int(input("Enter your choice (1/2/3): "))
            if choice in [1, 2, 3] and choice != previous_choice:
                return choice
            elif choice == previous_choice:
                print("Error: Please choose a different hashing method.")
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

# Function to generate a unique user ID
def generate_unique_user_id():
    return str(uuid.uuid4())

# Function to hash password using SHA-256
def hash_password_sha256(password):
    hashed = hashlib.sha256(password.encode()).hexdigest()
    return hashed[:16]

# Function to hash password using bcrypt
def hash_password_bcrypt(password):
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return hashed.decode('utf-8')

# Function to hash password using Argon2
def hash_password_argon2(password):
    hasher = argon2.PasswordHasher()
    hashed = hasher.hash(password.encode())
    # Extract only the hash value without the algorithm identifier and parameters
    return hashed.split('$')[-1][:16]

# Function to register a new user
def register_login(connection):
    # Prompt the user for a username
    while True:
        username = input("Enter a username: ")
        if ' ' in username:
            print("Error: Username cannot contain spaces. Please try again.")
        else:
            break

    # Prompt the user to input a password
    password = input("Enter A Password: ")

    # Prompt the user to choose the first hashing method
    choice1 = prompt_hashing_method()

    # Perform hashing based on the first choice
    if choice1 == 1:
        hashed_password1 = hash_password_sha256(password)
    elif choice1 == 2:
        hashed_password1 = hash_password_bcrypt(password)
    elif choice1 == 3:
        hashed_password1 = hash_password_argon2(password)

    # Print the first hashed password
    print("First Hashed Password:", hashed_password1)

    # Prompt the user to choose the second hashing method
    choice2 = prompt_hashing_method(choice1)

    # Perform hashing based on the second choice
    if choice2 == 1:
        hashed_password2 = hash_password_sha256(hashed_password1)
    elif choice2 == 2:
        # If bcrypt is chosen as the second hashing method, generate a new Bcrypt hash
        hashed_password2 = hash_password_bcrypt(password)
    elif choice2 == 3:
        hashed_password2 = hash_password_argon2(hashed_password1)

    # Generate a unique UserID for the new user
    user_id = generate_unique_user_id()

    # Store the username, hashed password, and bcrypt hash in the database
    if choice2 == 2:
        bcrypt_hash = None  # No bcrypt hash is stored when bcrypt is the second choice
        store_login(connection, user_id, username, hashed_password2, bcrypt_hash)
    else:
        store_login(connection, user_id, username, hashed_password2)

    # Print the final hashed password
    print("Final Hashed Password:", hashed_password2)
    print("UserID:", user_id)

    # Return the username along with the user_id1
    return user_id, username

# Function to authenticate a user
def login(connection):
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    try:
        cursor = connection.cursor()
        select_query = "SELECT Password, BcryptHash FROM Users WHERE Username = %s"
        cursor.execute(select_query, (username,))
        result = cursor.fetchone()
        cursor.close()

        if result:
            stored_password = result[0]
            bcrypt_hash = result[1]
            # Check if bcrypt is the chosen hashing method
            if bcrypt_hash:
                # If bcrypt is the chosen hashing method, authenticate using bcrypt
                if bcrypt.checkpw(password.encode(), stored_password.encode()):
                    print("\nLogin successful!")
                    return True
            else:
                # For other hashing methods, simply compare the stored hashed password
                if password == stored_password:
                    print("\nLogin successful!")
                    return True
                return user_id  # Return user_id after successful login
        print("Incorrect username or password.")
        return False

    except Error as e:
        print(f"Error authenticating user: {e}")
        return False


def main_menu():
    connection = create_connection()
    if connection:
        create_users_table(connection)
        while True:
            print("\nMenu:")
            print("1. Register")
            print("2. Login")
            print("3. Exit")
            choice = input("Enter your choice: ")
            if choice == "1":
                user_id, username = register_login(connection)
                print("Registered User:", user_id, username)  # Add this line for debugging
            elif choice == "2":
                if login(connection):
                    print("Exiting...")
                    break
            elif choice == "3":
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    connection = create_connection()
    if connection:
        create_users_table(connection)
        user_id = login(connection)
        if user_id:
            print("Login successful!")
        else:
            print("Login failed.")
