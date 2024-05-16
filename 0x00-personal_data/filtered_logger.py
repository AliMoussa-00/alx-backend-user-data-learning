#!/usr/bin/env python3
'''Regex-ing'''


import logging
import os
import mysql.connector
import re
from typing import List


PII_FIELDS = ('name', 'email', 'phone',
              'ssn', 'password',)


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    '''returns the log message obfuscated:'''
    for field in fields:
        message = re.sub(fr'({field})=([^{separator}]+)',
                         f'\\1={redaction}', message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        log = filter_datum(
            self.fields, self.REDACTION, record.getMessage(), self.SEPARATOR)
        record.msg = log
        return super().format(record)


def get_logger() -> logging.Logger:
    '''
    the use of this function is to create a logging object
    and add to it our custom formatter
    '''
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    stream_handler = logging.StreamHandler()
    redacting_formatter = RedactingFormatter(PII_FIELDS)
    stream_handler.setFormatter(redacting_formatter)
    logger.addHandler(stream_handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    '''
    returns a connector to the database
    '''

    connection = mysql.connector.connect(
        host=os.getenv('PERSONAL_DATA_DB_HOST', 'localhost'),
        user=os.getenv('PERSONAL_DATA_DB_USERNAME', 'root'),
        password=os.getenv('PERSONAL_DATA_DB_PASSWORD', 'root'),
        database=os.getenv('PERSONAL_DATA_DB_NAME')
    )

    return connection


def main() -> None:
    '''main function'''

    logger = get_logger()
    db = get_db()

    with db.cursor() as cursor:
        cursor.execute('SELECT * FROM users;')
        fields = [field[0] for field in cursor.description]
        rows = cursor.fetchall()
        for row in rows:
            msg = ''.join(
                f'{field}={str(value)}; '
                for field, value in zip(fields, row)
            )
            logger.info(msg.strip())

    db.close()


if __name__ == '__main__':
    main()
