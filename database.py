import logging
import sqlite3

def create_table(db_name='database.sqlite'):
    with sqlite3.connect(db_name) as con:
        cur = con.cursor()
        query = '''
            CREATE TABLE IF NOT EXISTS user_data(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                user_msg INTEGER,
                subject TEXT,
                level TEXT,
                question TEXT,
                answer TEXT
            );
        '''
        cur.execute(query)
        con.commit()
    logging.info(f'create table {db_name} done')

def get_users_data(field, db_name='database.sqlite'):
    with sqlite3.connect(db_name) as con:
        cur = con.cursor()
        query = f'''
        SELECT {field}
        FROM user_data
        '''
        data = cur.execute(query).fetchall()
    logging.info(f'get users data done')
    return data

def get_user_data(user_id, db_name='database.sqlite'):
    with sqlite3.connect(db_name) as con:
        cur = con.cursor()
        query = '''
        SELECT *
        FROM user_data
        WHERE user_id=?
        '''
        data = cur.execute(query, (user_id,))
    logging.info(f'get user data done for {user_id}')
    return data.fetchall()

def set_user_data(user_id, db_name='database.sqlite'):
    with sqlite3.connect(db_name) as con:
        cur = con.cursor()
        cur.execute(
            'INSERT INTO user_data (user_id)'
            ' VALUES(?);',
            (user_id,),
        )
        con.commit()
    logging.info(f'set user data done for {user_id}')

def update_user_data(field, value, user_id, db_name='database.sqlite'):
    with sqlite3.connect(db_name) as con:
        cur = con.cursor()
        query = f'''
        UPDATE user_data
        SET {field} = ?
        WHERE user_id = ?;
        '''
        cur.execute(query, (value, user_id))
    logging.info(f'update user data done for {user_id}')