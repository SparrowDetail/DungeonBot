import sqlite3
from DBHelper import DATABASE_DIRECTORY, USERS_TABLE

#Import attribute names
from DBHelper import ID

def add_user(user_id: int):
    conn = sqlite3.Connection(DATABASE_DIRECTORY)
    cursor = conn.cursor()

    cursor.execute(f"INSERT INTO {USERS_TABLE} VALUES ({user_id});")

    conn.commit()
    conn.close()

def add_many_users(user_ids: list):
    conn = sqlite3.Connection(DATABASE_DIRECTORY)
    cursor = conn.cursor()

    cursor.executemany(f"INSERT INTO {USERS_TABLE} VALUES (?);", user_ids)

    conn.commit()
    conn.close()

def get_all_users() -> list:
    conn = sqlite3.Connection(DATABASE_DIRECTORY)
    cursor = conn.cursor()
    
    cursor.execute(f"SELECT {ID} FROM {USERS_TABLE};")
    data = cursor.fetchall()

    conn.close()
    return data

def get_user(user_id: int):
    conn = sqlite3.Connection(DATABASE_DIRECTORY)
    cursor = conn.cursor()

    cursor.execute(f"SELECT {ID} FROM {USERS_TABLE} WHERE {ID} = {user_id};")
    id = cursor.fetchone()
    print(type(id))

    conn.close()
    return id

def remove_user(user_id: int):
    conn = sqlite3.Connection(DATABASE_DIRECTORY)
    conn.execute("PRAGMA foreign_keys = ON;")
    cursor = conn.cursor()

    cursor.execute(f"""
        DELETE FROM {USERS_TABLE}
        WHERE {ID} = {user_id};""")
    
    conn.commit()
    conn.close()

def verify_user(user_id: int) -> bool:
    if get_user(user_id) != None:
        return True
    else:
        return False

def verify_or_add_user(user_id: int) -> bool:
    if get_user(user_id) != None:
        return True
    else:
        try:
            add_user(user_id)
            return True
        except Exception as e:
            print(e)
            return False