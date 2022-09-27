
# Домашнее задание к лекции «Работа с PostgreSQL из Python»
# Создайте программу для управления клиентами на python.
# Требуется хранить персональную информацию о клиентах:
# имя / фамилия/ email/ телефон
# Сложность в том, что телефон у клиента может быть не один, а два, три и даже больше. А может и вообще не быть телефона
# (например, он не захотел его оставлять).
# Вам необходимо разработать структуру БД для хранения информации и несколько функций на python для управления данными:
#
# Функция, создающая структуру БД (таблицы) - DONE
# Функция, позволяющая добавить нового клиента - DONE
# Функция, позволяющая добавить телефон для существующего клиента - DONE
# Функция, позволяющая изменить данные о клиенте - DONE
# Функция, позволяющая удалить телефон для существующего клиента - DONE
# Функция, позволяющая удалить существующего клиента - DONE
# Функция, позволяющая найти клиента по его данным (имени, фамилии, email-у или телефону) - DONE

import psycopg2


def create_db(conn):

    with conn.cursor() as cur:
        # with conn.cursor() as cur:
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
                    phone_number VARCHAR(20),
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
                        RETURNING phone_id, phone_number, client_id;
                    """)
        print(cur.fetchall())

# Функция, позволяющая добавить нового клиента
def add_client(conn, name, surname, email, phone=None):

    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO client(client_name, client_surname, client_email) VALUES
            (%s, %s, %s)
            RETURNING client_id, client_name, client_surname, client_email;
            """, (name, surname, email, ))
        print(cur.fetchall())
#
# # Функция, позволяющая добавить телефон для существующего клиента
def add_phone(conn, client_id, phone_number):

    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO phone(client_id, phone_number) VALUES
            (%s, %s);
            """, (client_id, phone_number, ))
        cur.execute("""
            SELECT * FROM phone;
            """)
        print(cur.fetchall())

# Функция, позволяющая изменить данные о клиенте
def change_client(conn, client_id, name=None, surname=None, email=None, phones=None):
    with conn.cursor() as cur:
        cur.execute("""
              UPDATE client SET client_name = %s, client_surname = %s, client_email = %s  
              WHERE client_id = %s;
              """, (name, surname, email, client_id, ))
        cur.execute("""
                SELECT * FROM client;
                """)
        print(cur.fetchall())

#  Функция, позволяющая удалить телефон для существующего клиента
def delete_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        cur.execute("""
             DELETE FROM phone WHERE phone_number=%s;
             """, (phone, ))
        cur.execute("""
            DELETE FROM phone WHERE client_id=%s;
            """, (client_id,))
        cur.execute("""
            SELECT * FROM phone;
            """)
        print(cur.fetchall())

# Функция, позволяющая удалить существующего клиента
def delete_client(conn, client_id):
    with conn.cursor() as cur:
        cur.execute("""
            DELETE FROM phone WHERE client_id=%s;
            """, (client_id,))
        cur.execute("""
            DELETE FROM client WHERE client_id=%s;
            """, (client_id,))
        cur.execute("""
            SELECT * FROM client;
            """)
        print(cur.fetchall())

# Функция, позволяющая найти клиента по его данным(имени, фамилии, email или телефону)
def find_client(conn, name=None, surname=None, email=None, phone=None):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT client_name, client_surname, client_email, phone_number FROM client AS c
            JOIN phone AS p ON p.client_id = c.client_id
            WHERE client_name=%s AND client_surname=%s AND client_email=%s OR phone_number=%s;
            """, (name, surname, email, phone, ))
        print(cur.fetchall())

if __name__ == "__main__":

    with psycopg2.connect(database="clients_db", user="postgres", password="postgres") as conn:
        create_db(conn)
        add_client(conn, '6', '66', '666')
        add_phone(conn, '5', '7777')
        change_client(conn, '1', '0', '00', '000')
        delete_phone(conn, '5','7777')
        delete_client(conn, '1')
        find_client(conn, '','','','9999')
conn.close()