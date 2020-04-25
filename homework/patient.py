import csv
import logging
import homework.model_cvd19 as model
from homework.logg_cvd19 import logger_s, logger_e

FILENAME = 'covid_19_members.csv'


class Patient(object):
    first_name = model.NonBlank()
    last_name = model.NonBlank()
    birth_date = model.BirthValidator()
    phone = model.PhoneValidator()
    document_type = model.DocTypeValidator()
    document_id = model.DocIDValidator()

    def __init__(self, *args):
        self.logger_s = logging.getLogger('covid_19_success')
        self.logger_e = logging.getLogger("covid_19_errors")

        if args:
            self.first_name = args[0]
            self.last_name = args[1]
            self.birth_date = args[2]
            self.phone = args[3]
            self.document_type = args[4]
            self.document_id = args[5]
            self.logger_s.info('Был создан новый пациент')

    def __str__(self):
        return f'{self.first_name} {self.last_name} {self.birth_date} {self.phone} {self.document_type} ' \
               f'{self.document_id}'

    @classmethod
    def create(cls, *args):
        super(Patient, cls).__init__(*args)
        cls.created = Patient(*args)
        return cls.created

    def save(self):
        data = [self.first_name, self.last_name, self.birth_date, self.phone, self.document_type, self.document_id]
        try:
            with open(FILENAME, "a", newline="", encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(data)
        except Exception:
            self.logger_e.error('Something wrong')
            raise Exception('Something wrong!')
        else:
            self.logger_s.info('Сделана новая запись о пациенте в таблице')

    def __del__(self):
        del self.logger_s
        for fh in list(logging.getLogger("covid_19_success").handlers[::-1]):
            fh.close()
        del self.logger_e
        for fh in list(logging.getLogger("covid_19_errors").handlers[::-1]):
            fh.close()


class PatientCollection(object):
    def __init__(self, path):
        self.path = path
        self.fileBytePos = 0
        self.count = -1

    def __iter__(self):
        return self

    def __next__(self):
        inFile = open(self.path, 'r', encoding='utf-8')
        inFile.seek(self.fileBytePos)
        data = inFile.readline()
        self.fileBytePos = inFile.tell()
        inFile.close()
        if not data or not self.count:
            raise StopIteration
        self.count -= 1
        return Patient(*data.split(','))

    def limit(self, count):
        self.count = count
        return self.__iter__()
