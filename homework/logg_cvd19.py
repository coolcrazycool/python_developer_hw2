import logging

logger_s = logging.getLogger("covid_19_success")
logger_s.setLevel(logging.INFO)
logger_e = logging.getLogger("covid_19_errors")
logger_e.setLevel(logging.ERROR)

formatter = logging.Formatter("%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s")

handler_success = logging.FileHandler('success.log', 'a', 'utf-8')
handler_errors = logging.FileHandler('errors.log', 'a', 'utf-8')
handler_success.setFormatter(formatter)
handler_errors.setFormatter(formatter)
logger_s.addHandler(handler_success)
logger_e.addHandler(handler_errors)


def decorated_log(func):
    def wrapper(*args, **kwargs):
        if func.__name__ == '__init__':
            key = 'init'
        if func.__name__ == 'save':
            key = 'save'
        try:
            result = func(*args, **kwargs)
            if result:
                return result
        except AttributeError:
            logger_e.error('F_name or L_name can not be changed')
            raise AttributeError("F_name or L_name can not be changed")
        except TypeError:
            logger_e.error('Ошибка с типом данных')
            raise TypeError("Ошибка с типом данных")
        except UnicodeError:
            logger_e.error('Something wrong with your decoder in SAVE')
            raise UnicodeError('Something wrong with your decoder in SAVE')
        except ValueError:
            logger_e.error('Ошибка с типом данных')
            raise ValueError("Ошибка с данными")
        except IsADirectoryError:
            logger_e.error('Cant write in directory. Problem in SAVE')
            raise IsADirectoryError('Cant write in directory. Problem in SAVE')
        except PermissionError:
            logger_e.error('U cant write in this file. Problem in SAVE')
            raise PermissionError('U cant write in this file. Problem in SAVE')
        except OSError:
            logger_e.error('Some System Error. Problem in SAVE')
            raise OSError('Some System Error. Problem in SAVE')
        except RuntimeError:
            logger_e.error('Something unexpected. Problem in SAVE')
            raise RuntimeError('Something unexpected. Problem in SAVE')
        else:
            if key == 'init':
                logger_s.info('Пациент создан')
            if key == 'save':
                logger_s.info('Пациент сохранен')
    return wrapper
