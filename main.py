import sys
from time import sleep

import psycopg2
import schedule
import logging

from psycopg2.sql import SQL

from datetime import datetime, timedelta

row_number = 0
row_true_number = 0


def gen_data(number):
    return f"test_gen_data {number}"


def connect_to_db():
    logger.info("Старт подключения к базе данных")
    print_message("Старт подключения к базе данных")
    try:
        conn = psycopg2.connect(
            dbname="megafon",
            user="postgres",
            password="12345",
            host="megafon_postgres",
            port="5432"
        )
        logger.info("Скрипт успешно подключился к базе данных")
        print_message("Скрипт успешно подключился к базе данных")
        return conn
    except Exception as e:
        logger.info("Не удалось подключиться к базе данных. Ошибка:", e)
        print_message("Не удалось подключиться к базе данных. Ошибка:", e)
        sys.exit(1)


def insert_data_db(curr_list):

    global row_number

    logger.info(f"Вставка строки с номером {row_number}")
    print_message(f"Вставка строки с номером {row_number} и данными {curr_list[1]}")
    cursor.execute(SQL("INSERT INTO gen_data(record_id, data, record_date) values (%s, %s, now() at time zone 'Europe/Moscow')"), curr_list)
    connection.commit()


def insert_data():

    global row_number, row_true_number

    if row_number != 30:
        row_number += 1
        row_true_number += 1
        curr_data = gen_data(row_true_number)
        curr_list = [row_number, curr_data]
        insert_data_db(curr_list)
    else:
        row_number = 1
        row_true_number += 1
        cursor.execute(SQL("DELETE FROM gen_data"))
        logger.info("В таблице 30 строк. Произошла очистка таблицы")
        print_message("В таблице 30 строк. Произошла очистка таблицы")
        curr_data = gen_data(row_true_number)
        curr_list = [row_number, curr_data]
        insert_data_db(curr_list)


def main(conn, cur):

    try:
        logger.info("Старт выполнения задания по расписанию (вставка сгенерированных данных в БД каждую минуту)")
        print_message("Старт выполнения задания по расписанию (вставка сгенерированных данных в БД каждую минуту)")
        schedule.every(1).minutes.do(insert_data)

        while True:
            schedule.run_pending()

    finally:
        cur.close()
        conn.close()
        logger.info("Завершение работы скрипта")
        print_message("Завершение работы скрипта")


def print_message(message):
    print(datetime.now() + timedelta(hours=3), message)


logger = logging.getLogger()
if __name__ == '__main__':

    sleep(5)
    logging.basicConfig(filename="megafon.log", level=logging.INFO,
                        format="%(asctime)s %(levelname)s %(message)s")
    logger.info("Старт работы скрипта")
    print_message("Старт работы скрипта")
    connection = connect_to_db()
    cursor = connection.cursor()

    main(connection, cursor)
