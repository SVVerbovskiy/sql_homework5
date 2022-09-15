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
    clients_phone VARCHAR(25) UNIQUE);
    """)


def add_new_client(cur, client_name, client_surname, client_email):
    """Добавление нового клиента"""
    cur.execute("""
    INSERT INFO clients_info(client_name, client_surname, client_email) VALUES(%s, %s, %s);
    """, (client_name, client_surname, client_email))


def add_new_phone(cur, client_id, clients_phone):
    """Добавление нового телефона"""
    cur.execute("""
    INSERT INFO clients_phone(client_id, clients_phone) VALUES(%s, %s);
    """, (client_id, clients_phone))


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
            UPDATE clients_phones SET clients_phone=%s WHERE clients_phone=%s;
            ''', (new_phone, old_phone))
            break
        else:
            print('Вы ввели неверную команду повторите ввод: ')
