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

def get_character_id(user_id: int, char_name: str) -> int:
    """
    Queries for the characters rowid within the SQLite database and returns the id or None if the character could
    not be found.

    :param user_id: FOREIGN KEY user_id, must exist within the users table
    :param char_name: Character being verified
    :return: Unique integer id for queried character or None if the character does not exist
    """
    conn = sqlite3.Connection(DATABASE_DIRECTORY)
    conn.execute("PRAGMA foreign_keys = ON;")
    cursor = conn.cursor()

    cursor.execute(f"""
        SELECT rowid
        FROM {ORDER_COMMAND_TABLE}
        WHERE {USER_ID} = {user_id} AND {NAME} = '{char_name}';""")
    
    result: int = cursor.fetchone()

    conn.commit()
    conn.close()

    return result[0] if (not result == None) else result

def update_character_by_id(char_id: int, char_name:str = None, roll_value: int = None, modifier: int = None) -> bool:
    """
    Updates the character data of a particular row within the order table using a unique row ID.

    :param char_id: SQLite generated row id for the character being updated
    :param char_name: Optional str value used to update the character's name
    :param roll_value: Optional int value used to update the character's roll value
    :param modifier: Optional integer value used to update a character's roll modifier
    :return: True if the data was updated and False if no change was made
    """
    #Formats the modified data for the SQLite update query
    updated_data: str = ""
    if not (char_name == None):
        updated_data = updated_data + f"{NAME} = '{char_name}'"
    if not (roll_value == None):
        if not (updated_data == ""):
            updated_data = updated_data + ", "
        updated_data = updated_data + f"{ROLL} = {roll_value}"
    if not (modifier == None):
        if not (updated_data == ""):
            updated_data = updated_data + ", "
        updated_data = updated_data + f"{MODIFIER} = {modifier}"

    #Executes SQLite UPDATE only if data was changed
    if not (updated_data == ""):
        conn = sqlite3.Connection(DATABASE_DIRECTORY)
        conn.execute("PRAGMA foreign_keys = ON;")
        cursor = conn.cursor()

        cursor.execute(f"""
            UPDATE {ORDER_COMMAND_TABLE}
            SET {updated_data}
            WHERE rowid = {char_id};""")
        
        conn.commit()
        conn.close()

        return True
    else:
        return False

def get_character_by_id(char_id: int):
    """
    Returns the data for a particular character corresponding to a specified rowid within the order command table.

    :param char_id: rowid corresponding to a target character
    :return: None if the row does not exist or a tuple if the row does exist. Tuple indices: [0]: character name, [1]: roll value, [2]: modifier
    """
    conn = sqlite3.Connection(DATABASE_DIRECTORY)
    conn.execute("PRAGMA foreign_keys = ON;")
    cursor = conn.cursor()

    cursor.execute(f"""
        SELECT {NAME}, {ROLL}, {MODIFIER}
        FROM {ORDER_COMMAND_TABLE}
        WHERE rowid = {char_id};""")
    
    selection = cursor.fetchone()

    conn.close()

    print(type(selection))
    return selection