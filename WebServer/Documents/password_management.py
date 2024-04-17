import mysql.connector
import user_registration
from mysql.connector import Error
import uuid

# Function to establish a connection to the MySQL database
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

# Function to create the Passwords table
def create_passwords_table(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Passwords (
                PasswordID INT AUTO_INCREMENT PRIMARY KEY,
                UserID VARCHAR(36),
                WebsiteServiceName VARCHAR(255) NOT NULL,
                UsernameEmail VARCHAR(255),
                EncryptedPassword TEXT NOT NULL,
                URL VARCHAR(255),
                Notes TEXT,
                CONSTRAINT FK_UserPass FOREIGN KEY (UserID) REFERENCES Users(UserID)
            )
        """)
        connection.commit()
        cursor.close()
        print("Passwords table created successfully")
    except Error as e:
        print(f"Error creating Passwords table: {e}")

def update_password_table(connection, user_id, username):
    try:
        cursor = connection.cursor()
        cursor.execute("UPDATE Passwords SET UserID = %s WHERE UsernameEmail = %s AND UserID IS NULL",
                       (user_id, username))
        connection.commit()
        cursor.close()
        print("Password table updated successfully")
    except Error as e:
        print(f"Error updating password table: {e}")

# Function to store a password for a user
def store_password(connection, user_id, website_service_name, username_email, encrypted_password, url=None, notes=None):
    try:
        cursor = connection.cursor()
        # Store the password in the Passwords table using the retrieved UserID
        insert_query = """
                        INSERT INTO Passwords (UserID, WebsiteServiceName, UsernameEmail, EncryptedPassword, URL, Notes) 
                        VALUES (%s, %s, %s, %s, %s, %s)
                        """
        cursor.execute(insert_query, (user_id, website_service_name, username_email, encrypted_password, url, notes))
        connection.commit()
        print("Password stored successfully")
        cursor.close()
    except Error as e:
        print(f"Error storing password: {e}")


def store_password_menu(connection, username,):
    try:
        cursor = connection.cursor()

        # Debugging: Print the username to verify
        print("Username to search:", username)

        # Check if the username exists in the Users table
        cursor.execute("SELECT UserID FROM Users WHERE Username = %s", (username,))
        result = cursor.fetchone()
        print("Result:", result)  # Add this line for debugging

        if result:
            user_id = result[0]  # Retrieve the UserID if the Username exists
            website_service_name = input("Enter Website/Service Name: ").strip()
            username_email = input("Enter Username/Email: ").strip()
            encrypted_password = input("Enter Encrypted Password: ").strip()
            url = input("Enter URL (optional, press Enter to skip): ").strip()
            notes = input("Enter Notes (optional, press Enter to skip): ").strip()
            store_password(connection, user_id, website_service_name, username_email, encrypted_password, url, notes)

            if website_service_name and username_email and encrypted_password:
                # Store the password in the Passwords table using the retrieved UserID
                insert_query = """
                    INSERT INTO Passwords (UserID, WebsiteServiceName, UsernameEmail, EncryptedPassword, URL, Notes) 
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                cursor.execute(insert_query, (user_id, website_service_name, username_email, encrypted_password, url, notes))
                connection.commit()
                print("Password stored successfully")
            else:
                print("Error storing password: Required fields are empty")
        else:
            print("Error storing password: Username not found")

        cursor.close()
    except Error as e:
        print(f"Error storing password: {e}")


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
            print(f"\nWebsite/Service: {password[2]}")
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

def update_password_menu(connection):
    try:
        password_id = input("Enter the ID of the password you want to update: ")
        new_password = input("Enter the new password: ")
        update_password(connection, password_id, new_password)
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

def delete_password_menu(connection,):
    try:
        password_id = input("Enter the ID of the password you want to delete: ")
        delete_password(connection, password_id)
    except Error as e:
        print(f"Error deleting password: {e}")

# Entry point of the script
if __name__ == "__main__":
    # Attempt to establish a connection to the database
    connection = create_connection()
    if connection:
        # Register the first user
        user_id, username = user_registration.register_login(connection)
        print("Registered User:", user_id, username)  # Add this line for debugging
        if user_id and username:
            # If connection is successful, create the Passwords table
            create_passwords_table(connection)
            # Update the Passwords table with the UserID of the first user
            update_password_table(connection, user_id, username)
            # Call the function to store passwords
            store_password_menu(connection, username)
            # Close the database connection
            connection.close()
    else:
        # If connection fails, exit the program or take appropriate action
        print("Exiting program due to connection error")