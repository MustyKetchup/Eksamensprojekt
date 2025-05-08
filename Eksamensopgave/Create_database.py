import sqlite3
import os

def create_database():
    try:
        # Connect to SQLite database (creates a new database if it doesn't exist)
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()

        # Check if Schema.sql exists
        if not os.path.exists('Schema.sql'):
            raise FileNotFoundError("Schema.sql file not found in the current directory")

        # Read the SQL file
        with open('Schema.sql', 'r') as sql_file:
            sql_script = sql_file.read()

        # Execute the SQL script
        cursor.executescript(sql_script)

        # Commit the changes
        connection.commit()
        print("Database created successfully and Schema.sql executed.")

    except sqlite3.Error as e:
        print(f"An error occurred while creating the database: {e}")
    except FileNotFoundError as e:
        print(e)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        # Close the connection
        if connection:
            connection.close()
            print("Database connection closed.")

if __name__ == "__main__":
    create_database()