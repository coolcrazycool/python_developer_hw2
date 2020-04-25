from homework.logg_cvd19 import logger_e, logger_s, logger


# TODO Do not logg every time creation of patient
class AutoStorageDescriptor:
    def __set_name__(self, owner, name):
        self.name = name

    def __set__(self, instance, value):
        # log.logger_s.info(f"Поле {self.name} заполнено")
        instance.__dict__[self.name] = value

    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:
            return instance.__dict__[self.name]


class Validated(AutoStorageDescriptor):
    with logger():
        def __set__(self, instance, value):
            value = self.validate(instance, value)
            super(Validated, self).__set__(instance, value)

    @classmethod
    def validate(cls, instance, value):
        """return"""


class NameValidator(Validated):
    def validate(self, instance, value):
        if type(value) != str:
            with logger():
                logger_e.error("Wrong type")
            raise TypeError
        if value.isalpha():
            return value.capitalize()
        else:
            with logger():
                logger_e.error("Wrong type_name")
            raise ValueError


class NonBlank(NameValidator):
    def validate(self, instance, value):
        if self.name in instance.__dict__ and getattr(instance, self.name):
            with logger():
                logger_e.error("Переназначение ФИО не предусмотрено")
            raise AttributeError
        return NameValidator.validate(self, instance, value)


class RenameOther(Validated):
    def validate(self, instance, value):
        if self.name in instance.__dict__ and getattr(instance, self.name):
            with logger():
                logger_s.info(f"{self.name} было изменено")
            return value
        return value


class PhoneValidator(RenameOther):
    white_lst = [str(i) for i in range(0, 10)]

    def validate(self, instance, value):
        if type(value) != str:
            with logger():
                logger_e.error("Wrong type")
            raise TypeError
        for symbol in value:
            if symbol not in self.white_lst:
                value = value.replace(symbol, '')
        if value.find('8') == 0:
            value = value.replace(value[0], '7', 1)
        if len(value) != 11:
            with logger():
                logger_e.error("Wrong attribute phone")
            raise ValueError
        return RenameOther.validate(self, instance, value)


class BirthValidator(RenameOther):
    def validate(self, instance, value):
        if type(value) != str:
            with logger():
                logger_e.error("Wrong type")
            raise TypeError
        for symbol in value:
            if symbol.isalpha():
                with logger():
                    logger_e.error("Wrong value")
                raise ValueError
            if str(symbol) == ' ' or symbol == '-':
                value = value.replace(symbol, '.')
        birth_lst = value.split('.')
        value = f'{birth_lst[0].zfill(4)}-' \
                f'{birth_lst[1].zfill(2)}-' \
                f'{birth_lst[2].zfill(2)}'
        return RenameOther.validate(self, instance, value)


class DocTypeValidator(RenameOther):
    white_lst = ['Паспорт', 'Заграничный паспорт', 'Водительские права']

    def validate(self, instance, value):
        if type(value) != str:
            with logger():
                logger_e.error("Wrong type")
            raise TypeError
        else:
            if value.capitalize() in self.white_lst:
                value = value.capitalize()
                return RenameOther.validate(self, instance, value)
            else:
                with logger():
                    logger_e.error("Wrong doc_type")
                raise ValueError


class DocIDValidator(RenameOther):
    doc_dict = {'Паспорт': 10, 'Водительские права': 10, 'Заграничный паспорт': 9}
    white_lst = [str(i) for i in range(0, 10)]

    def validate(self, instance, value):
        if type(value) != str:
            with logger():
                logger_e.error("Wrong type")
            raise TypeError
        for symbol in value:
            if symbol not in self.white_lst:
                value = value.replace(symbol, '')
        if len(value) == self.doc_dict[getattr(instance, 'document_type')]:
            return RenameOther.validate(self, instance, value)
        else:
            with logger():
                logger_e.error("Wrong doc_id")
            raise ValueError

