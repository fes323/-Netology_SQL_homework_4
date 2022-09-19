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


def add_client(conn, first_name, last_name, email, phone=None):
    with conn.cursor() as cur:
        cur.execute(f'''
            INSERT INTO client(first_name, last_name, email) VALUES
            ('{first_name}', '{last_name}', '{email}') RETURNING id;
        ''')
        client_id = cur.fetchone()[0]
        if phone != None:
            cur.execute(f'''
                INSERT INTO phone(phone) VALUES
                ('{phone}') RETURNING id;
            ''')
            phone_id = cur.fetchone()[0]
            cur.execute(f'''
                INSERT INTO client_phone(client_id, phone_id) VALUES
                ('{client_id}', '{phone_id}');
            ''')
    conn.commit()

def add_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        cur.execute(f'''
            INSERT INTO phone(phone) VALUES
            ('{phone}') RETURNING id;
        ''')
        cur.execute(f'''
            INSERT INTO client_phone(client_id, phone_id) VALUES
            ('{client_id}', '{cur.fetchone()[0]}');
        ''')
    conn.commit()

def change_client(conn, client_id, first_name=None, last_name=None, email=None):
    with conn.cursor() as cur:
        if first_name != None:
            cur.execute('''
                UPDATE client SET first_name=%s
                WHERE id=%s;
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

def delete_client(conn, client_id):
    with conn.cursor() as cur:
        try:
            cur.execute('''
                DELETE FROM client_phone
                WHERE id=%s;
            ''', (client_id))
        finally:
            try:
                cur.execute('''
                    DELETE FROM phone
                    WHERE id=%s;
                ''', (client_id))
            finally:
                try:
                    cur.execute('''
                        DELETE FROM client
                        WHERE id=%s;
                    ''', (client_id))
                except Exception as error:
                    print(f'Не удалось удалить клиента:\n{error}')

    conn.commit()

def find_client(conn, first_name=None, last_name=None, email=None):
    with conn.cursor() as cur:
        if first_name != None:
            cur.execute('''
                SELECT * FROM client
                WHERE first_name=%s;
            ''', (first_name))
            print(cur.fetchall())


if __name__ == '__main__':
    conn = psycopg2.connect(database="netology_db", user="postgres", password="345154m9m9M")
    create_db(conn)
    add_client(conn, "Ivan", "Ivanov", "Test@test.ru", "323232")
    add_phone(conn, '1', '121212')
    change_client(conn, 1, first_name='Maksim', last_name='Petrov', email='Petrov@petrov.com')
    delete_client(conn, '1')
    #find_client(conn, first_name="Maksim")
    conn.close()