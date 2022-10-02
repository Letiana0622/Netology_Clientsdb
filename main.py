
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

# cursor  - DONE
# в каждой функции можно не прописывать, а реализовать контекстный менеджер with conn.cursor() as ...
# именно при совершении всех действий и передавать его в качестве аргумента при вызове функций;

# CHANGE-
# функция изменения данных о клиенте реализована не совсем корректно. Если в нее не передавать необязательные аргументы,
# то просто все поля в записи изменятся на None, хотя нужно было просто поменять, например, имя, а другие поля не трогать.
# То есть нужно менять только те поля, которые переданы в функцию, а другие поля должны оставаться без изменений, а не меняться на None;

# SEARCH - аналогичная ситуация с поиском. В идеале должна быть возможность его делать хоть по одному полю
# (например, искать всех клиентов по фамилии), либо по любой их комбинации.
# У вас же поиск происходит только абсолютно по всем полям сразу.

import psycopg2
def create_db(conn):
        cur.execute("""
            DROP TABLE phone;
            DROP TABLE client;
            """)
        cur.execute("""CREATE TABLE IF NOT EXISTS client (
                    client_id SERIAL PRIMARY KEY,
                    client_name VARCHAR(20),
                    client_surname VARCHAR(20),
                    client_email VARCHAR(20) UNIQUE
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
        print(f'create client_table {cur.fetchall()}')

        cur.execute("""
                    INSERT INTO phone(phone_number, client_id) VALUES
                        ('0000', 3),
                        ('1111', 3),
                        ('9999', 4)
                        RETURNING phone_id, phone_number, client_id;
                    """)
        print(f'create phone_table {cur.fetchall()}')

# Функция, позволяющая добавить нового клиента
def add_client(conn, name, surname, email, phone=None):
        cur.execute("""
            INSERT INTO client(client_name, client_surname, client_email) VALUES
            (%s, %s, %s)
            RETURNING client_id, client_name, client_surname, client_email;
            """, (name, surname, email, ))
        print(f'add client {cur.fetchall()}')
#
# # Функция, позволяющая добавить телефон для существующего клиента
def add_phone(conn, client_id, phone_number):
        cur.execute("""
            INSERT INTO phone(client_id, phone_number) VALUES
            (%s, %s);
            """, (client_id, phone_number, ))
        cur.execute("""
            SELECT * FROM phone;
            """)
        print(f'add phone {cur.fetchall()}')

# Функция, позволяющая изменить данные о клиенте
def change_client(conn, client_id, name=None, surname=None, email=None):
        cur.execute("""
              UPDATE client SET 
                  client_name = COALESCE(NULLIF(%(client_name)s,''), client_name), 
                  client_surname = COALESCE(NULLIF(%(client_surname)s,''), client_surname), 
                  client_email = COALESCE(NULLIF(%(client_email)s,''), client_email)
              WHERE 
                  client_id = %(client_id)s
              ;
              """, {"client_name": name, "client_surname": surname, "client_email": email, "client_id": client_id})
        cur.execute("""
                SELECT * FROM client;
                """)
        print(f'change client {cur.fetchall()}')

#  Функция, позволяющая удалить телефон для существующего клиента
def delete_phone(conn, client_id, phone):
        cur.execute("""
             DELETE FROM phone WHERE phone_number=%s;
             """, (phone, ))
        cur.execute("""
            DELETE FROM phone WHERE client_id=%s;
            """, (client_id,))
        cur.execute("""
            SELECT * FROM phone;
            """)
        print(f'delete phone {cur.fetchall()}')

# Функция, позволяющая удалить существующего клиента
def delete_client(conn, client_id):
        cur.execute("""
            DELETE FROM phone WHERE client_id=%s;
            """, (client_id,))
        cur.execute("""
            DELETE FROM client WHERE client_id=%s;
            """, (client_id,))
        cur.execute("""
            SELECT * FROM client;
            """)
        print(f'delete client {cur.fetchall()}')

# Функция, позволяющая найти клиента по его данным(имени, фамилии, email или телефону)
def find_client(conn, name=None, surname=None, email=None, phone=None):
        cur.execute("""
            SELECT client_name, client_surname, client_email, phone_number FROM client AS c
            FULL JOIN phone AS p ON p.client_id = c.client_id
            WHERE
                  (client_name = %s 
                  OR 
                  client_surname = %s
                  OR
                  client_email = %s
                  OR
                  phone_number = %s);
                  """, (name, surname, email, phone))
        print(f'find client {cur.fetchall()}')
        # cur.execute("""
        #             SELECT * FROM client AS c
        #             FULL JOIN phone AS p ON p.client_id = c.client_id;
        #             """)
        # print(f'control table {cur.fetchall()}')

if __name__ == "__main__":

    with psycopg2.connect(database="clients_db", user="postgres", password="postgres") as conn:
        with conn.cursor() as cur:
            create_db(conn)
            add_client(conn, '6', '66', '666')
            add_phone(conn, '5', '7777')
            change_client(conn, 6, '1', '', '')
            delete_phone(conn, '5','7777')
            delete_client(conn, '1')
            find_client(conn, '', '22','222','')
            find_client(conn, '2', '', '', '')
            find_client(conn, '3', '33', '', '')
            find_client(conn, '3', '33', '', '9999')
            find_client(conn, '', '', '', '9999')
conn.close()