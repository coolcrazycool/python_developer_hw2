import logging
from contextlib import contextmanager

logger_s = logging.getLogger("covid_19_success")
logger_s.setLevel(logging.INFO)
logger_e = logging.getLogger("covid_19_errors")
logger_e.setLevel(logging.ERROR)

formatter = logging.Formatter("%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s")


@contextmanager
def logger():
    handler_success = logging.FileHandler('success.log', 'a', 'utf-8')
    handler_errors = logging.FileHandler('errors.log', 'a', 'utf-8')
    handler_success.setFormatter(formatter)
    handler_errors.setFormatter(formatter)
    logger_s.addHandler(handler_success)
    logger_e.addHandler(handler_errors)
    yield
    handler_success.close()
    logging.getLogger('covid_19_success').removeHandler(handler_success)
    handler_errors.close()
    logging.getLogger('covid_19_errors').removeHandler(handler_errors)