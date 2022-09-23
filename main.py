
# Домашнее задание к лекции «Работа с PostgreSQL из Python»
# Создайте программу для управления клиентами на python.
# Требуется хранить персональную информацию о клиентах:
# имя / фамилия/ email/ телефон
# Сложность в том, что телефон у клиента может быть не один, а два, три и даже больше. А может и вообще не быть телефона
# (например, он не захотел его оставлять).
# Вам необходимо разработать структуру БД для хранения информации и несколько функций на python для управления данными:
#
# Функция, создающая структуру БД (таблицы) - DONE
# Функция, позволяющая добавить нового клиента - ERROR (WIP)
# Функция, позволяющая добавить телефон для существующего клиента
# Функция, позволяющая изменить данные о клиенте
# Функция, позволяющая удалить телефон для существующего клиента
# Функция, позволяющая удалить существующего клиента
# Функция, позволяющая найти клиента по его данным (имени, фамилии, email-у или телефону)
# Функции выше являются обязательными, но это не значит что должны быть только они. При необходимости можете создавать дополнительные функции и классы.

import psycopg2

def create_db(conn):

    with conn.cursor() as cur:

        cur.execute("""
        DROP TABLE phone;
        DROP TABLE client;
        """)

        cur.execute("""CREATE TABLE IF NOT EXISTS client (
                    client_id SERIAL PRIMARY KEY,
                    client_name VARCHAR(20) NOT NULL,
                    client_surname VARCHAR(20) NOT NULL,
                    client_email VARCHAR(20) NOT NULL UNIQUE
                     );""")
        conn.commit()

        cur.execute("""CREATE TABLE IF NOT EXISTS phone (
                    phone_id SERIAL PRIMARY KEY,
                    phone_number VARCHAR(20) UNIQUE,
                    client_id INTEGER NOT NULL REFERENCES client(client_id)
                     );""")
        conn.commit()

        cur.execute("""
                    INSERT INTO client(client_name, client_surname, client_email) VALUES
                        ('1', '11', '111'),
                        ('2', '22', '222'),
                        ('3', '33', '333'),
                        ('4', '44', '444'),
                        ('5', '55', '555')
                        RETURNING client_id, client_name, client_surname, client_email;
                    """)
        print(cur.fetchall())

        cur.execute("""
                    INSERT INTO phone(phone_number, client_id) VALUES
                        ('0000', 3),
                        ('1111', 3),
                        ('9999', 4)
                        RETURNING client_id, phone_id, phone_number;
                    """)
        print(cur.fetchall())

def add_client(conn, name, surname, email, phone=None):

    with conn.cursor() as cur:
            cur.execute("""
            INSERT INTO client(client_name, client_surname, client_email) VALUES
            (client_name=%s, client_surname=%s, client_email=%s) 
            RETURNING client_id, client_name, client_surname, client_email;
            """, (name, surname, email, ))



    return cur.fetchall()

# def add_phone(conn, client_id, phone_number):
# def change_client(conn, client_id, first_name=None, last_name=None, email=None, phones=None):
# def delete_phone(conn, client_id, phone):
# def delete_client(conn, client_id):
# def find_client(conn, first_name=None, last_name=None, email=None, phone=None):

with psycopg2.connect(database="clients_db", user="postgres", password="postgres") as conn:
    create_db(conn)
    new_client = add_client(conn, '6', '66', '666')
    print(new_client)

conn.close()