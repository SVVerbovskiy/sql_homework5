import psycopg2
from pprint import pprint


def create_tables(cur):
    """Создание таблиц данных"""

    # таблица основных данных
    cur.execute("""
    CREATE TABLE IF NOT EXISTS clients_info(
    id SERIAL PRIMARY KEY,
    client_name VARCHAR(100) NOT NULL,
    client_surname VARCHAR(100) NOT NULL,
    client_email VARCHAR(100) NOT NULL
    );  
    """)

    # таблица телефонных номеров
    cur.execute("""
    CREATE TABLE IF NOT EXISTS clients_phones(
    id_phones SERIAL PRIMARY KEY,
    client_id INTEGER NOT NULL REFERENCES clients_info(id),
    client_phone VARCHAR(25) UNIQUE);
    """)


def add_new_client(cur, client_name, client_surname, client_email):
    """Добавление нового клиента"""
    cur.execute("""
    INSERT INTO clients_info(client_name, client_surname, client_email) VALUES(%s, %s, %s);
    """, (client_name, client_surname, client_email))


def add_new_phone(cur, client_id, client_phone):
    """Добавление нового телефона"""
    cur.execute("""
    INSERT INTO clients_phones(client_id, client_phone) VALUES(%s, %s);
    """, (client_id, client_phone))


def change_client_data():
    """Изменение информации о клиенте"""
    print('Для изменения информации о клиенте введите нужную команду\n'
          '1-изменить имя; 2-изменить фамилию; 3-изменить e-mail; 4-изменить номер телефона')

    while True:
        command = int(input())
        if command == 1:
            id_changing_name = input('Введите id клиента имя которого хотите изменить: ')
            changing_name = input('Введите новое имя: ')
            cur.execute('''
            UPDATE clients_info SET client_name=%s WHERE id=%s;
            ''', (changing_name, id_changing_name))
            break
        elif command == 2:
            id_changing_surname = input('Введите id клиента фамилию которого хотите изменить: ')
            changing_surname = input('Введите новую фамилию: ')
            cur.execute('''
            UPDATE clients_info SET client_surname=%s WHERE id=%s;
            ''', (changing_surname, id_changing_surname))
            break
        elif command == 3:
            id_changing_email = input('Введите id клиента e-mail которого хотите изменить: ')
            changing_email = input('Введите новый e-mail: ')
            cur.execute('''
            UPDATE clients_info SET client_email=%s WHERE id=%s;
            ''', (changing_email, id_changing_email))
            break
        elif command == 4:
            old_phone = input('Введите номер телефона который хотите заменить: ')
            new_phone = input('Введите новый номер телефона: ')
            cur.execute('''
            UPDATE clients_phones SET client_phone=%s WHERE client_phone=%s;
            ''', (new_phone, old_phone))
            break
        else:
            print('Вы ввели неверную команду повторите ввод: ')


def delete_client_phone():
    """Удаление номера телефона клиента"""
    client_id_for_delete = input('Введите id клиента, номер телефона которого хотите удалить: ')
    phone_for_delete = input('Введите номер который хотите удалить: ')
    with conn.cursor() as cur:
        cur.execute('''
        DELETE FROM clients_phones WHERE client_id=%s AND client_phone=%s
        ''', (client_id_for_delete, phone_for_delete))


def delete_client():
    """Удаление информации о клиенте"""
    id_deleting_client = input('Введите id клиента которого хотите удалить: ')
    with conn.cursor() as cur:
        cur.execute('''
        DELETE FROM clients_phones WHERE client_id=%s
        ''', (id_deleting_client,))
        cur.execute('''
        DELETE FROM clients_info WHERE id=%s
        ''', (id_deleting_client,))


def find_client():
    """Поиск информации о клиенте"""
    print("Для поиска информации о клиенте, пожалуйста, введите команду, где:\n "
          "1 - найти по имени; 2 - найти по фамилии; 3 - найти по e-mail; 4 - найти по номеру телефона; 0 - выход;")
    while True:
        command = int(input('Введите номер команды для поиска информации о клиенте: '))
        if command == 1:
            finding_name = input('Введите имя: ')
            cur.execute('''
            SELECT id, client_name, client_surname, client_email, client_phone FROM clients_info ci
            LEFT JOIN clients_phones cp on ci.id = cp.client_id
            WHERE client_name=%s
            ''', (finding_name,))
            print(cur.fetchall())
        elif command == 2:
            finding_surname = input('Введите фамилию: ')
            cur.execute('''
            SELECT id, client_name, client_surname, client_email, client_phone FROM clients_info ci
            JOIN clients_phones cp on ci.id = cp.client_id
            WHERE client_surname=%s
            ''', (finding_surname,))
            print(cur.fetchall())
        elif command == 3:
            finding_email = input('Введите e-mail: ')
            cur.execute('''
            SELECT id, client_name, client_surname, client_email, client_phone FROM clients_info ci
            JOIN clients_phones cp on ci.id = cp.client_id
            WHERE client_email=%s
            ''', (finding_email,))
            print(cur.fetchall())
        elif command == 4:
            finding_phone = input('Введите номер телефона: ')
            cur.execute('''
            SELECT id, client_name, client_surname, client_email, client_phone FROM clients_info ci
            JOIN clients_phones cp on ci.id = cp.client_id
            WHERE client_phone=%s
            ''', (finding_phone,))
            print(cur.fetchall())
        elif command == 0:
            break
        else:
            print('Вы ввели неверную команду, попробуйте снова!')


def check_function(cur):
    """Отображение содержимого таблиц"""
    cur.execute('''
    SELECT * FROM clients_info;
    ''')
    pprint(cur.fetchall())
    cur.execute('''
    SELECT * FROM clients_phones;
    ''')
    pprint(cur.fetchall())


with psycopg2.connect(host="127.0.0.1", user="postgres", password="7753191", database="homework5", port="5432") as conn:
    with conn.cursor() as cur:
        cur.execute('''
        DROP TABLE clients_phones;
        DROP TABLE clients_info;
        ''')
        create_tables(cur)
        add_new_client(cur, "Earl", "Mendez", "eam@g.com")
        add_new_client(cur, "Steven", "Miller", "stm@g.com")
        add_new_client(cur, "John", "Gomez", "jog@g.com")
        add_new_client(cur, "Edward", "Graham", "edg@g.com")
        add_new_client(cur, "Perry", "Garcia", "peg@g.com")
        add_new_phone(cur, 1, "11111111")
        add_new_phone(cur, 1, "6666666")
        add_new_phone(cur, 2, "222222222")
        add_new_phone(cur, 3, "3333333333")
        add_new_phone(cur, 4, "44444444444")
        add_new_phone(cur, 5, "555555555555")
        add_new_phone(cur, 5, "77777880")
        check_function(cur)
        change_client_data()
        check_function(cur)
        delete_client_phone()
        check_function(cur)
        delete_client()
        check_function(cur)
        find_client()
conn.close()



