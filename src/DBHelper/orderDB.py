import sqlite3
from DBHelper import DATABASE_DIRECTORY, ORDER_COMMAND_TABLE, vacuum
from DBHelper.usersDB import ID

#Import attribute names
from DBHelper import USER_ID, NAME, ROLL, MODIFIER

def add_order_command(user_id: int, name: str, roll: int, modifier: int):
    conn = sqlite3.Connection(DATABASE_DIRECTORY)
    conn.execute("PRAGMA foreign_keys = ON;")
    cursor = conn.cursor()

    cursor.execute(f"INSERT INTO {ORDER_COMMAND_TABLE} VALUES (?, ?, ?, ?);", (user_id, name, roll, modifier))

    conn.commit()
    conn.close()

def get_initiative_order(user_id: int) -> list:
    conn = sqlite3.Connection(DATABASE_DIRECTORY)
    cursor = conn.cursor()

    cursor.execute(f"""
                   SELECT *
                   FROM {ORDER_COMMAND_TABLE}
                    WHERE {USER_ID} = {user_id};
                   """)
    
    order = cursor.fetchall()
    conn.close()

    order.sort(key=lambda item: item[2] + item[3], reverse=True)

    return order

def get_one_order(user_id: int, char_name: str):
    conn = sqlite3.Connection(DATABASE_DIRECTORY)
    cursor = conn.cursor()

    cursor.execute(f"""SELECT *
                        FROM {ORDER_COMMAND_TABLE}
                        WHERE {USER_ID} = {user_id} AND {NAME} = '{char_name}';
                        """)
    selection = cursor.fetchone()

    conn.close()
    return selection


def remove_one_order(user_id: int, char_name: str) -> bool:
    if get_one_order(user_id, char_name) != None:
        conn = sqlite3.Connection(DATABASE_DIRECTORY)
        cursor = conn.cursor()

        cursor.execute(f"""DELETE FROM {ORDER_COMMAND_TABLE}
                            WHERE {USER_ID} = {user_id} AND {NAME} = '{char_name}';""")

        conn.commit()
        conn.close()
        return True
    else:
        return False

def clear_user_order(user_id: int):
    conn = sqlite3.Connection(DATABASE_DIRECTORY)
    cursor = conn.cursor()

    cursor.execute(f"""
        DELETE FROM {ORDER_COMMAND_TABLE}
        WHERE {USER_ID} = {user_id};""")
    
    conn.commit()
    conn.close()