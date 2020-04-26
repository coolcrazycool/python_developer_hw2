from abc import ABCMeta


# TODO Do not logg every time creation of patient
class AutoStorageDescriptor:
    def __set_name__(self, owner, name):
        self.name = name

    def __set__(self, instance, value):
        instance.__dict__[self.name] = value

    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:
            return instance.__dict__[self.name]


class Validated(AutoStorageDescriptor):
    def __set__(self, instance, value):
        value = self.validate(instance, value)
        super(Validated, self).__set__(instance, value)

    @classmethod
    def validate(cls, instance, value):
        raise NotImplementedError("Validate method is not implemented")


class NameValidator(Validated):
    def validate(self, instance, value):
        if not isinstance(value, str):
            instance.logger_e.error("Wrong type for f_name or l_name")
            raise TypeError("Wrong type for f_name or l_name")
        if value.isalpha():
            return value.capitalize()
        else:
            instance.logger_e.error("Wrong value for f_name or s_name")
            raise ValueError("Wrong value for f_name or s_name")


class NonBlank(NameValidator):
    def validate(self, instance, value):
        if self.name in instance.__dict__ and getattr(instance, self.name):
            instance.logger_e.error("Переназначение ФИО не предусмотрено")
            raise AttributeError("F_name or L_name can not be changed")
        return super(NonBlank, self).validate(instance, value)


class RenameOther(Validated):
    def validate(self, instance, value):
        if self.name in instance.__dict__ and getattr(instance, self.name):
            instance.logger_s.info(f"{self.name} было изменено")
            return value
        return value


class PhoneValidator(RenameOther):
    white_lst = [str(i) for i in range(0, 10)]

    def validate(self, instance, value):
        if not isinstance(value, str):
            instance.logger_e.error("Wrong type for Phone")
            raise TypeError("Wrong type for Phone")
        for symbol in value:
            if symbol not in self.white_lst:
                value = value.replace(symbol, '')
        if value.find('8') == 0:
            value = value.replace(value[0], '7', 1)
        if len(value) != 11:
            instance.logger_e.error("Wrong attribute phone")
            raise ValueError("Wrong attribute phone")
        return RenameOther.validate(self, instance, value)


class BirthValidator(RenameOther):
    def validate(self, instance, value):
        if not isinstance(value, str):
            instance.logger_e.error("Wrong type for birthday")
            raise TypeError("Wrong type for birthday")
        for symbol in value:
            if symbol.isalpha():
                instance.logger_e.error("Wrong value for birthday")
                raise ValueError("Wrong value for birthday")
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
        if not isinstance(value, str):
            instance.logger_e.error("Wrong type for doc_type")
            raise TypeError("Wrong type for doc_type")
        else:
            if value.capitalize() in self.white_lst:
                value = value.capitalize()
                return RenameOther.validate(self, instance, value)
            else:
                instance.logger_e.error("Wrong doc_type value")
                raise ValueError("Wrong doc_type value")


class DocIDValidator(RenameOther):
    doc_dict = {'Паспорт': 10, 'Водительские права': 10, 'Заграничный паспорт': 9}
    white_lst = [str(i) for i in range(0, 10)]

    def validate(self, instance, value):
        if not isinstance(value, str):
            instance.logger_e.error("Wrong type for doc_id")
            raise TypeError("Wrong type for doc_id")
        for symbol in value:
            if symbol not in self.white_lst:
                value = value.replace(symbol, '')
        if len(value) == self.doc_dict[getattr(instance, 'document_type')]:
            return RenameOther.validate(self, instance, value)
        else:
            instance.logger_e.error("Wrong doc_id value")
            raise ValueError("Wrong doc_id value")

