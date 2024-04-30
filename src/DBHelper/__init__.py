"""
Initializes the database and its subsequent tables
"""
import sqlite3

DATABASE_DIRECTORY = "./Database/dungeonBot.db"
USERS_TABLE = 'users'
ORDER_COMMAND_TABLE = 'order_command_data'

#USER TABLE ATTRIBUTES
ID = "id"

#ORDER TABLE ATTRIBUTES
USER_ID = "user_id"
NAME = "order_title"
ROLL = "roll_value"
MODIFIER = "modifier"

def init_user_table():
    """Initializes the users table if one does not exist"""
    conn = sqlite3.Connection(DATABASE_DIRECTORY)
    conn.execute("PRAGMA foreign_keys = ON;")
    cursor = conn.cursor()

    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {USERS_TABLE} (
            {ID} integer NOT NULL PRIMARY KEY
        );""")
    
    conn.commit()
    conn.close()

def init_order_table():
    """
    Initializes the order command table if does not exist. Used in generating and
    maintaining initiative orders.
    """
    conn = sqlite3.Connection(DATABASE_DIRECTORY)
    conn.execute("PRAGMA foreign_keys = ON;")
    cursor = conn.cursor()

    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {ORDER_COMMAND_TABLE} (
            {USER_ID} integer NOT NULL,
            {NAME} text NOT NULL,
            {ROLL} integer NOT NULL,
            {MODIFIER} integer NOT NULL,
            FOREIGN KEY ({USER_ID}) REFERENCES {USERS_TABLE} ({ID})
                   ON UPDATE CASCADE
                   ON DELETE CASCADE
        );""")
    
    conn.commit()
    conn.close()

def vacuum():
    """Executes the SQLite 'VACUUM' command to free unused memory"""
    conn = sqlite3.Connection(DATABASE_DIRECTORY)
    conn.execute("VACUUM;")
    conn.close()

#Initialize the database
init_user_table()
init_order_table()
vacuum()