"""Helper module used to maintain the database initiative order table"""
import sqlite3
from DBHelper import DATABASE_DIRECTORY, ORDER_COMMAND_TABLE, vacuum
from DBHelper.usersDB import ID

#Import attribute names
from DBHelper import USER_ID, NAME, ROLL, MODIFIER

def add_order_command(user_id: int, name: str, roll: int, modifier: int):
    """
    Add a row to the order table

    :param user_id: FOREIGN KEY user_id, must exist within the users table
    :param name: Character name being added to the initiative order
    :param roll: initiative roll, typically from a D20 (1-20)
    :param modifier: roll modifier (i.e. -1, 0, or 1)
    """
    conn = sqlite3.Connection(DATABASE_DIRECTORY)
    conn.execute("PRAGMA foreign_keys = ON;")
    cursor = conn.cursor()

    cursor.execute(f"INSERT INTO {ORDER_COMMAND_TABLE} VALUES (?, ?, ?, ?);", (user_id, name, roll, modifier))

    conn.commit()
    conn.close()

def get_initiative_order(user_id: int) -> list:
    """
    Returns a list of tuples representing the passed user id's initiative roll data. Data is sorted in order
    from highest to lowest based on the sum of their roll value and their modifier (initiative order)

    :param user_id: FOREIGN KEY user_id, must exist within the users table
    :return: list of tuple[size 3] or None if no ids exist. Tuple indices: [0]: character name, [1]: roll value, [2]: modifier
    """
    conn = sqlite3.Connection(DATABASE_DIRECTORY)
    conn.execute("PRAGMA foreign_keys = ON;")
    cursor = conn.cursor()

    cursor.execute(f"""
        SELECT {NAME}, {ROLL}, {MODIFIER}
        FROM {ORDER_COMMAND_TABLE}
        WHERE {USER_ID} = {user_id};""")
    
    order = cursor.fetchall()
    conn.close()

    order.sort(key=lambda item: item[1] + item[2], reverse=True)

    return order

def get_one_order(user_id: int, char_name: str):
    """
    Returns a row as a tuple where the passed user id and character name are stored within the database or None if the
    row does not exist

    :param user_id: FOREIGN KEY user_id, must exist within the users table
    :param char_name: Character name being searched for
    :return: None if the row does not exist or a tuple if the row does exist. Tuple indices: [0]: character name, [1]: roll value, [2]: modifier
    """
    conn = sqlite3.Connection(DATABASE_DIRECTORY)
    conn.execute("PRAGMA foreign_keys = ON;")
    cursor = conn.cursor()

    cursor.execute(f"""
        SELECT {NAME}, {ROLL}, {MODIFIER}
        FROM {ORDER_COMMAND_TABLE}
        WHERE {USER_ID} = {user_id} AND {NAME} = '{char_name}';""")
    selection = cursor.fetchone()

    conn.close()
    return selection


def remove_one_order(user_id: int, char_name: str) -> bool:
    """
    Removes all rows from the database where the passed user id and character name match. Returns True if the rows
    were removed and False if the rows did not exist

    :param user_id: FOREIGN KEY user_id, must exist within the users table
    :param char_name: Character name being removed from the order
    :return: True if the rows were removed and False if the rows did not exist
    """
    if get_one_order(user_id, char_name) != None:
        conn = sqlite3.Connection(DATABASE_DIRECTORY)
        conn.execute("PRAGMA foreign_keys = ON;")
        cursor = conn.cursor()

        cursor.execute(f"""
            DELETE FROM {ORDER_COMMAND_TABLE}
            WHERE {USER_ID} = {user_id} AND {NAME} = '{char_name}';""")

        conn.commit()
        conn.close()
        vacuum()
        return True
    else:
        return False

def clear_user_order(user_id: int):
    """
    Removes all rows where the passed user id matches

    :param user_id: FOREIGN KEY user_id, must exist within the users table
    """
    conn = sqlite3.Connection(DATABASE_DIRECTORY)
    conn.execute("PRAGMA foreign_keys = ON;")
    cursor = conn.cursor()

    cursor.execute(f"""
        DELETE FROM {ORDER_COMMAND_TABLE}
        WHERE {USER_ID} = {user_id};""")
    
    conn.commit()
    conn.close()
    vacuum()