import csv
import logging
import model_cvd19 as model
from logg_cvd19 import logger_s, logger_e, handler_errors, handler_success, decorated_log
import sqlite3

FILENAME = 'covid_19_db.db'


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

        data = [self.first_name, self.last_name, self.birth_date, self.phone, self.document_type, self.document_id]
        cursor.execute("INSERT INTO covid_members VALUES (?, ?, ?, ?, ?, ?)", data)

        conn.commit()
        cursor.close()
        conn.close()

    def __del__(self):
        handler_errors.close()
        handler_success.close()


class PatientCollection(object):
    def __init__(self, path):
        self.path = path
        self.id = 1
        self.count = None
        self.conn = sqlite3.connect(self.path)
        self.cursor = self.conn.cursor()

    def __iter__(self):
        return self

    @decorated_log
    def __next__(self):
        if self.count:
            if self.id == self.count+1:
                self.cursor.close()
                self.conn.close()
                raise StopIteration
        read_line = self.cursor.execute(f"SELECT first_name, last_name, birth_date, phone, document_type, document_id"
                                        f" FROM covid_members WHERE ROWID = {self.id}")
        data = list(read_line)
        data = list(*data)
        if not data:
            self.cursor.close()
            self.conn.close()
            raise StopIteration
        self.id += 1
        return Patient(*data)

    def limit(self, count):
        self.count = count
        return self.__iter__()
