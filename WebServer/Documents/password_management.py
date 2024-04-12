import mysql.connector
from mysql.connector import Error
import uuid

# Function to create the Passwords table
def create_passwords_table(connection):
    try:
        cursor = connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS Passwords (
            PasswordID INT AUTO_INCREMENT PRIMARY KEY,
            UserID VARCHAR(36),
            WebsiteServiceName VARCHAR(255) NOT NULL,
            UsernameEmail VARCHAR(255),
            EncryptedPassword TEXT NOT NULL,
            URL VARCHAR(255),
            Notes TEXT,
            FOREIGN KEY (UserID) REFERENCES Users(UserID)
        )
        """
        cursor.execute(create_table_query)
        connection.commit()
        cursor.close()
        print("Passwords table created successfully")
    except Error as e:
        print(f"Error creating Passwords table: {e}")


# Function to establish a connection to the MySQL database
def create_connection():
    try:
        connection = mysql.connector.connect(
            host='B-MacBook-Pro.local',
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


# Function to create the Users table
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
def store_login(connection, username, hashed_password, bcrypt_hash=None):
    try:
        cursor = connection.cursor()
        user_id = generate_unique_user_id()
        insert_query = "INSERT INTO Users (UserID, Username, Password, BcryptHash) VALUES (%s, %s, %s, %s)"

        # Ensure bcrypt_hash is not None
        if bcrypt_hash is None:
            bcrypt_hash = ''
        cursor.execute(insert_query, (user_id, username, hashed_password, bcrypt_hash))
        connection.commit()
        cursor.close()
        print("Username, password, and bcrypt hash stored successfully in the database")
        return user_id
    except Error as e:
        print(f"Error storing username, password, and bcrypt hash: {e}")


# Function to store a password for a user
def store_password(connection, user_id, website_service_name, username_email, encrypted_password, url=None, notes=None):
    try:
        cursor = connection.cursor()
        insert_query = "INSERT INTO Passwords (UserID, WebsiteServiceName, UsernameEmail, EncryptedPassword, URL, Notes) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(insert_query, (user_id, website_service_name, username_email, encrypted_password, url, notes))
        connection.commit()
        cursor.close()
        print("Password stored successfully")
    except Error as e:
        print(f"Error storing password: {e}")


# Function to generate a unique user ID
def generate_unique_user_id():
    return str(uuid.uuid4())


# Function to register a new user (modified to store passwords)
def register_login(connection):
    # Prompt the user for a username and password
    ...

    # Store the username, hashed password, and hashing method in the Users table
    user_id = store_login(connection, username, hashed_password, choice)

    print(f"Registration successful! Your UserID is: {user_id}")

    # Prompt the user to store passwords
    while True:
        website_service_name = input("Enter Website/Service Name: ")
        username_email = input("Enter Username/Email: ")
        encrypted_password = input("Enter Encrypted Password: ")
        url = input("Enter URL (optional): ")
        notes = input("Enter Notes (optional): ")

        # Store the password in the Passwords table
        store_password(connection, user_id, website_service_name, username_email, encrypted_password, url, notes)

        add_another = input("Do you want to add another password? (yes/no): ")
        if add_another.lower() != 'yes':
            break


# Function to interactively store a new password
def store_password_menu(connection, user_id):
    website_service_name = input("Enter Website/Service Name: ")
    username_email = input("Enter Username/Email: ")
    encrypted_password = input("Enter Encrypted Password: ")
    url = input("Enter URL (optional): ")
    notes = input("Enter Notes (optional): ")
    store_password(connection, user_id, website_service_name, username_email, encrypted_password, url, notes)
    print("Password stored successfully")


# Function to retrieve passwords for a user
def retrieve_passwords(connection, user_id):
    try:
        cursor = connection.cursor()
        select_query = "SELECT * FROM Passwords WHERE UserID = %s"
        cursor.execute(select_query, (user_id,))
        passwords = cursor.fetchall()
        cursor.close()
        return passwords
    except Error as e:
        print(f"Error fetching passwords: {e}")
        return []


# Function to display saved passwords for a user
def display_saved_passwords(connection, user_id):
    passwords = retrieve_passwords(connection, user_id)
    if passwords:
        print("Saved Passwords:")
        for password in passwords:
            print(f"Website/Service: {password[2]}")
            print(f"Username/Email: {password[3]}")
            print(f"Encrypted Password: {password[4]}")
            print(f"URL: {password[5]}")
            print(f"Notes: {password[6]}")
            print()
    else:
        print("No passwords saved for this user")


# Function to update a password for a given ID
def update_password(connection, password_id, new_password):
    try:
        cursor = connection.cursor()
        update_query = "UPDATE Passwords SET EncryptedPassword = %s WHERE PasswordID = %s"
        cursor.execute(update_query, (new_password, password_id))
        connection.commit()
        cursor.close()
        print("Password updated successfully")
    except Error as e:
        print(f"Error updating password: {e}")


# Function to delete a password for a given ID
def delete_password(connection, password_id):
    try:
        cursor = connection.cursor()
        delete_query = "DELETE FROM Passwords WHERE PasswordID = %s"
        cursor.execute(delete_query, (password_id,))
        connection.commit()
        cursor.close()
        print("Password deleted successfully")
    except Error as e:
        print(f"Error deleting password: {e}")

# Entry point of the script
if __name__ == "__main__":
    # Attempt to establish a connection to the database
    connection = create_connection()
    if connection:
        # If connection is successful, create the Passwords table
        create_passwords_table(connection)
        # Close the database connection
        connection.close()
    else:
        # If connection fails, exit the program or take appropriate action
        print("Exiting program due to connection error")