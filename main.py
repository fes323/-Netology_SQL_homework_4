import psycopg2

def create_db(conn):
    try:
        with conn.cursor() as cur:
            cur.execute('''
                DROP TABLE client_phone;
                DROP TABLE phone;
                DROP TABLE client;
            ''')

            cur.execute('''
                CREATE TABLE IF NOT EXISTS client(
                id SERIAL PRIMARY KEY,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email TEXT NOT NULL
                );
            ''')

            cur.execute('''
                CREATE TABLE IF NOT EXISTS phone(
                id SERIAL PRIMARY KEY,
                phone TEXT
                );
            ''')

            cur.execute('''
                CREATE TABLE IF NOT EXISTS client_phone(
                id SERIAL PRIMARY KEY,
                client_id INTEGER NOT NULL REFERENCES client(id),
                phone_id INTEGER NOT NULL REFERENCES phone(id)
                );
            ''')
        conn.commit()
    except Exception as error:
        print(error)


def add_client(conn, first_name, last_name, email):
    with conn.cursor() as cur:
        cur.execute(f'''
            INSERT INTO client(first_name, last_name, email) VALUES
            ('{first_name}', '{last_name}', '{email}');
        ''')
    conn.commit()

# Не могу найти исправление ошибки.
# Выдает ошибку:
# Traceback (most recent call last):
#   File "G:\netology\SQL_HomeWork_4.1\main.py", line 72, in <module>
#     change_client(conn, 1, first_name='Maksim', last_name='Petrov', email='Petrov@petrov.com')
#   File "G:\netology\SQL_HomeWork_4.1\main.py", line 52, in change_client
#     cur.execute('''
# ValueError: unsupported format character '
# ' (0xa) at index 75
def change_client(conn, client_id, first_name=None, last_name=None, email=None):
    with conn.cursor() as cur:
        if first_name != None:
            cur.execute('''
                UPDATE client SET first_name=%s
                WHERE id=%
            ''', (first_name, client_id))
        if last_name != None:
            cur.execute('''
                UPDATE client SET last_name=%s
                WHERE id=%s;
            ''', (last_name, client_id))
        if email != None:
            cur.execute('''
                UPDATE client SET email=%s
                WHERE id=%s;
            ''', (email, client_id))
    conn.commit()


#Данная проблема везде *_*
def delete_client(conn, client_id):
    with conn.cursor() as cur:
        cur.execute('''
            DELETE FROM client
            WHERE client_id=%;
        ''', (client_id))
        conn.commit()

if __name__ == '__main__':
    conn = psycopg2.connect(database="netology_db", user="postgres", password="345154m9m9M")
    create_db(conn)
    add_client(conn, 'Ivan', "Ivanov", 'Test@test.ru')
    #change_client(conn, 1, first_name='Maksim', last_name='Petrov', email='Petrov@petrov.com')
    delete_client(conn, '1')
    conn.close()