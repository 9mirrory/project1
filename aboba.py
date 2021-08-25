import datetime
from time import sleep
import psycopg2
import dataclasses



time_now = datetime.datetime.now()

day = str(input())

hour = str(input())

minutes = str(input())

if len(day) == 1:
    day = '0' + day
if len(hour) == 1:
    hour = '0' + hour
if len(minutes) == 1:
    minutes = '0' + minutes
while True:
    time_now = datetime.datetime.now()
    if str(time_now.hour) == hour and str(time_now.minute) == minutes and str(time_now.day) == day:
        break
    sleep(1)

@dataclasses.dataclass
class User:
    user_id: int
    time_to_create_channel: datetime.datetime.date
    id_categories:int

def connect():
    try:
        conn = psycopg2.connect(user='postgres', dbname='postgres', password='', host='127.0.0.1', port='5432'
                                )

        with conn.cursor() as cur:
            cur.execute('select version();')

    except psycopg2.Error as e:
        raise ConnectionError(f'error with psql: {e}')

    return conn


def create_bd(conn):
    create_table_query = '''CREATE TABLE discord(
                            user_id INTEGER PRIMARY KEY NOT NULL,
                            time_to_create_channel DATE NOT NULL,
                            id_categories INTEGER PRIMARY KEY NOT NULL);'''
    try:
        conn.exucute(create_table_query)
        conn.commit()
        print('База созданна успешно')
    except Exception as e:
        print('Что-то пошло не так...')
        raise ConnectionError(f'error with psql: {e}')


def create_user(
        conn: psycopg2.connect,
        user: User) -> bool:
    query = 'INSERT INTO users (user_id, time_to_prepare) VALUES (%s, %s) RETURNING user_id;'

    with conn.cursor() as cur:
        try:
            cur.execute(query, (user.user_id, user.time_to_create_channel))
        except psycopg2.errors.UniqueViolation:
            conn.commit()
            return False
        data = cur.fetchone()
        conn.commit()

    return bool(data)


def get_user_id(
        conn: psycopg2.connect,
        user_id: int) -> User:
    query = 'SELECT * FROM users WHERE user_id=%s'

    with conn.cursor() as cur:
        cur.execute(query, (user_id,))
        data = cur.fetchone()

        if data and len(data) == 2:
            return User(data[0], data[1], data[2])

        return User(..., ..., ...)
