import csv
import logging
import homework.model_cvd19 as model
from homework.logg_cvd19 import logger_s, logger_e, handler_errors, handler_success, decorated_log
import sqlite3

FILENAME = 'covid_19_members.csv'


class Patient(object):
    first_name = model.NonBlank()
    last_name = model.NonBlank()
    birth_date = model.BirthValidator()
    phone = model.PhoneValidator()
    document_type = model.DocTypeValidator()
    document_id = model.DocIDValidator()

    @decorated_log
    def __init__(self, first_name, last_name, birth_date, phone, document_type, document_id):
        self.logger_s = logging.getLogger('covid_19_success')
        self.logger_e = logging.getLogger("covid_19_errors")

        if first_name and last_name and birth_date and phone and document_type and document_id:
            self.first_name = first_name
            self.last_name = last_name
            self.birth_date = birth_date
            self.phone = phone
            self.document_type = document_type
            self.document_id = document_id

    def __str__(self):
        return f'{self.first_name} {self.last_name} {self.birth_date} {self.phone} {self.document_type} ' \
               f'{self.document_id}'

    @staticmethod
    def create(first_name, last_name, birth_date, phone, document_type, document_id):
        return Patient(first_name, last_name, birth_date, phone, document_type, document_id)

    @decorated_log
    def save(self):
        conn = sqlite3.connect('covid_19_db.db')
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS covid_members
                (first_name char(30) not null, last_name char(30) not null, birth_date char(10) not null,
                phone char(11) not null , document_type char(20) not null , document_id char(10) not null UNIQUE);""")

        data = [self.first_name, self.last_name, self.birth_date, self.phone, self.document_type, self.document_id]
        cursor.execute('INSERT INTO covid_members VALUES(?, ?, ?, ?, ?, ?)', data)
        conn.commit()
        cursor.close()
        conn.close()

    def __del__(self):
        handler_errors.close()
        handler_success.close()


class PatientCollection(object):
    def __init__(self, path):
        self.path = path
        self.fileBytePos = 0
        self.id = 1
        self.count = None
        self.conn = sqlite3.connect(self.path)
        self.cursor = self.conn.cursor()

    def __iter__(self):
        return self

    @decorated_log
    def __next__(self):
        data = self.cursor.execute(f"SELECT * FROM covid_members WHERE id = {self.id}")
        self.id += 1
        if not data or (self.count and self.id == self.count):
            self.conn.close()
            self.cursor.close()
            raise StopIteration
        return Patient(*data)

    def limit(self, count):
        self.count = count
        return self.__iter__()
