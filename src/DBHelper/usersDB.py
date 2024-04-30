"""Helper module used to maintain the database users table"""
import sqlite3
from DBHelper import DATABASE_DIRECTORY, USERS_TABLE, vacuum

#Import attribute names
from DBHelper import ID

def add_user(user_id: int):
    """
    Add a passed user id into the database

    :param user_id: integer value representing the target user
    :raise sqlite3.IntegrityError: Raised when the target user id already exists within the table
    """
    conn = sqlite3.Connection(DATABASE_DIRECTORY)
    cursor = conn.cursor()

    cursor.execute(f"INSERT INTO {USERS_TABLE} VALUES ({user_id});")

    conn.commit()
    conn.close()

def add_many_users(user_ids: list):
    """
    Add a list of user ids into the database

    :param user_ids: a list of tuples containing the target user ids to be added, i.e.
        DATA = [(123,), (124,), (125,),]
    :raise ValueError: Raised when data is formatted incorrectly, must be a list of tuples (123,)
    :raise sqlite3.IntegrityError: Raised when a target user id already exists within the table
    """
    conn = sqlite3.Connection(DATABASE_DIRECTORY)
    cursor = conn.cursor()

    cursor.executemany(f"INSERT INTO {USERS_TABLE} VALUES (?);", user_ids)

    conn.commit()
    conn.close()

def get_all_users() -> list:
    """
    Returns all users within the database as a list of tuples[size 1]

    :return: list of tuple[size 1] or None if no ids exist. Tuple indices: [0]: user_id
    """
    conn = sqlite3.Connection(DATABASE_DIRECTORY)
    cursor = conn.cursor()
    
    cursor.execute(f"SELECT {ID} FROM {USERS_TABLE};")
    data = cursor.fetchall()

    conn.close()
    return data

def get_user(user_id: int):
    """
    Returns users table row where the id matches the passed user od or None if
    the id does not exist

    :param user_id: integer value representing the target user
    :return: tuple or None if id does not exist. Tuple indices: [0]: user_id
    """
    conn = sqlite3.Connection(DATABASE_DIRECTORY)
    cursor = conn.cursor()

    cursor.execute(f"SELECT {ID} FROM {USERS_TABLE} WHERE {ID} = {user_id};")
    id = cursor.fetchone()

    conn.close()
    return id

def remove_user(user_id: int):
    """
    Remove a user with the passed user id if it exists

    :param user_id: integer value representing the target user
    """
    conn = sqlite3.Connection(DATABASE_DIRECTORY)
    conn.execute("PRAGMA foreign_keys = ON;")
    cursor = conn.cursor()

    cursor.execute(f"""
        DELETE FROM {USERS_TABLE}
        WHERE {ID} = {user_id};""")
    
    conn.commit()
    conn.close()

def verify_user(user_id: int) -> bool:
    """
    Verify the passed user id exists within the database

    :return: True if the id exists, False if the id does not exist
    """
    return get_user(user_id) != None

def verify_or_add_user(user_id: int) -> bool:
    """
    Verify the passed user id exists within the database or add the user id to the database
    if it does not exist

    :return: True if the id exists or was added, False if the id could not be verified or added
    """
    if get_user(user_id) != None:
        return True
    else:
        try:
            add_user(user_id)
            return True
        except sqlite3.IntegrityError as e:
            print(e)
            return False
        except Exception as e:
            print(e)
            return False