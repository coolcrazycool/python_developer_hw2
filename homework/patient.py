import csv
import logging
import homework.model_cvd19 as model
from homework.logg_cvd19 import logger_s, logger_e, handler_errors, handler_success

FILENAME = 'covid_19_members.csv'


class Patient(object):
    first_name = model.NonBlank()
    last_name = model.NonBlank()
    birth_date = model.BirthValidator()
    phone = model.PhoneValidator()
    document_type = model.DocTypeValidator()
    document_id = model.DocIDValidator()

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
            self.logger_s.info('Был создан новый пациент')

    def __str__(self):
        return f'{self.first_name} {self.last_name} {self.birth_date} {self.phone} {self.document_type} ' \
               f'{self.document_id}'

    @staticmethod
    def create(first_name, last_name, birth_date, phone, document_type, document_id):
        return Patient(first_name, last_name, birth_date, phone, document_type, document_id)

    def save(self):
        data = [self.first_name, self.last_name, self.birth_date, self.phone, self.document_type, self.document_id]
        try:
            with open(FILENAME, "a", newline="", encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(data)
        except UnicodeError:
            self.logger_e.error('Something wrong with your decoder in SAVE')
            raise UnicodeError('Something wrong with your decoder in SAVE')
        except IsADirectoryError:
            self.logger_e.error('Cant write in directory. Problem in SAVE')
            raise IsADirectoryError('Cant write in directory. Problem in SAVE')
        except PermissionError:
            self.logger_e.error('U cant write in this file. Problem in SAVE')
            raise PermissionError('U cant write in this file. Problem in SAVE')
        except OSError:
            self.logger_e.error('Some System Error. Problem in SAVE')
            raise OSError('Some System Error. Problem in SAVE')
        except RuntimeError:
            self.logger_e.error('Something unexpected. Problem in SAVE')
            raise RuntimeError('Something unexpected. Problem in SAVE')
        else:
            self.logger_s.info('Сделана новая запись о пациенте в таблице')

    def __del__(self):
        handler_errors.close()
        handler_success.close()


class PatientCollection(object):
    def __init__(self, path):
        self.path = path
        self.fileBytePos = 0
        self.count = -1

    def __iter__(self):
        return self

    def __next__(self):
        with open(self.path, 'r', encoding='utf-8') as inFile:
            inFile.seek(self.fileBytePos)
            data = inFile.readline()
            self.fileBytePos = inFile.tell()
        if not data or not self.count:
            raise StopIteration
        self.count -= 1
        return Patient(*data.split(','))

    def limit(self, count):
        self.count = count
        return self.__iter__()
