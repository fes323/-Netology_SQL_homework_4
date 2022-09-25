import psycopg2


def delete_db(conn):
    try:
        cur.execute('''
            DROP TABLE client_phone;
            DROP TABLE phone;
            DROP TABLE client;
        ''')
    except Exception as error:
        print(error)
    pass


def create_db(conn):
    try:
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
    except Exception as error:
        print(error)
    pass


def add_client(conn, first_name, last_name, email, phone=None):
    cur.execute(f'''
        INSERT INTO client(first_name, last_name, email) VALUES
        ('{first_name}', '{last_name}', '{email}') RETURNING id;
    ''')
    client_id = cur.fetchone()[0]
    if phone is not True:
        cur.execute(f'''
            INSERT INTO phone(phone) VALUES
            ('{phone}') RETURNING id;
        ''')
        phone_id = cur.fetchone()[0]
        cur.execute(f'''
            INSERT INTO client_phone(client_id, phone_id) VALUES
            ('{client_id}', '{phone_id}');
        ''')
    pass


def add_phone(conn, client_id, phone):
    cur.execute(f'''
        INSERT INTO phone(phone) VALUES
        ('{phone}') RETURNING id;
    ''')
    cur.execute(f'''
        INSERT INTO client_phone(client_id, phone_id) VALUES
        ('{client_id}', '{cur.fetchone()[0]}');
    ''')
    pass


def change_client(conn, client_id, first_name=None, last_name=None, email=None):
    if first_name is not True:
        cur.execute('''
            UPDATE client SET first_name=%s
            WHERE id=%s;
        ''', (first_name, client_id))
    if last_name is not True:
        cur.execute('''
            UPDATE client SET last_name=%s
            WHERE id=%s;
        ''', (last_name, client_id))
    if email is not True:
        cur.execute('''
            UPDATE client SET email=%s
            WHERE id=%s;
        ''', (email, client_id))
    pass


def delete_client(conn, client_id):
    try:
        cur.execute('''
            DELETE FROM client_phone
            WHERE client_id=%s;
        ''', (client_id))
    except Exception as error:
        print(f'Не удалось удалить клиента[0]:\n{error}')
    finally:
        try:
            cur.execute('''
                DELETE FROM phone
                WHERE id=%s;
            ''', client_id)
        except Exception as error:
            print(f'Не удалось удалить клиента[1]:\n{error}')
        finally:
            try:
                cur.execute('''
                        DELETE FROM client
                        WHERE id=%s;
                    ''', (client_id))
            except Exception as error:
                print(f'Не удалось удалить клиента[2]:\n{error}')
    pass


def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
    try:
        if first_name is not None:
            cur.execute('''
                SELECT * FROM client
                WHERE first_name=%s;
            ''', (first_name))
        if last_name is not None:
            cur.execute('''
                SELECT * FROM client
                where last_name=%s;
            ''', (last_name))
        if email is not None:
            cur.execute('''
                SELECT * FROM client
                where email=%s;
            ''', (email))
        if phone is not None:
            cur.execute('''
                SELECT * FROM phone
                where phone=%s;
            ''', (phone))
    finally:
        print(cur.fetchall())
        pass


with psycopg2.connect(database="netology_db", user="postgres", password="345154m9m9M") as conn:
    with conn.cursor() as cur:
        delete_db(conn)
        create_db(conn)
        add_client(conn, "Ivan", "Ivanov", "Test@test.ru", "323232")
        add_phone(conn, '1', '121212')
        change_client(conn, 1, first_name='Maksim', last_name='Petrov', email='Petrov@petrov.com')
        #delete_client(conn, '1')
        find_client(conn, first_name='Maksim')
        pass
    pass
