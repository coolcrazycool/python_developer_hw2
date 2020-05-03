from patient import Patient, PatientCollection
import click
import sqlite3


class OptionEatAll(click.Option):

    def __init__(self, *args, **kwargs):
        self.save_other_options = kwargs.pop('save_other_options', True)
        nargs = kwargs.pop('nargs', -1)
        assert nargs == -1, 'nargs, if set, must be -1 not {}'.format(nargs)
        super(OptionEatAll, self).__init__(*args, **kwargs)
        self._previous_parser_process = None
        self._eat_all_parser = None

    def add_to_parser(self, parser, ctx):

        def parser_process(value, state):
            # method to hook to the parser.process
            done = False
            value = [value]
            if self.save_other_options:
                # grab everything up to the next option
                while state.rargs and not done:
                    for prefix in self._eat_all_parser.prefixes:
                        if state.rargs[0].startswith(prefix):
                            done = True
                    if not done:
                        value.append(state.rargs.pop(0))
            else:
                # grab everything remaining
                value += state.rargs
                state.rargs[:] = []
            value = tuple(value)

            # call the actual process
            self._previous_parser_process(value, state)

        retval = super(OptionEatAll, self).add_to_parser(parser, ctx)
        for name in self.opts:
            our_parser = parser._long_opt.get(name) or parser._short_opt.get(name)
            if our_parser:
                self._eat_all_parser = our_parser
                self._previous_parser_process = our_parser.process
                our_parser.process = parser_process
                break
        return retval


@click.group()
def cli():
    pass


@click.command()
@click.argument('f_name')
@click.argument('s_name')
@click.option('--birth-date', cls=OptionEatAll, type= str)
@click.option('--phone', cls=OptionEatAll, type=str)
@click.option('--document-type', cls=OptionEatAll, type=str)
@click.option('--document-number', cls=OptionEatAll, type=str)
def create(f_name, s_name, birth_date, phone, document_type, document_number):
    print(f_name, s_name, birth_date, phone, document_type, document_number)
    birth_date = ''.join(birth_date)
    phone = ''.join(phone)
    document_type = ' '.join(document_type)
    document_number = ''.join(document_number)
    patient = Patient(f_name, s_name, birth_date, phone, document_type, document_number)
    patient.save()
    del patient


@click.command()
@click.argument('limit', default=10, type=int)
def show(limit):
    collection = PatientCollection('covid_19_db.db')
    for i in collection.limit(limit):
        print(i)


@click.command()
def count():
    collection = PatientCollection('covid_19_db.db')
    for i in collection.limit(None):
        print(i)


cli.add_command(create)
cli.add_command(show)
cli.add_command(count)

if __name__ == '__main__':
    conn = sqlite3.connect('covid_19_db.db')
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS covid_members
                              (first_name TEXT not null,
                              last_name TEXT not null,
                              birth_date TEXT not null,
                              phone TEXT not null,
                              document_type TEXT not null,
                              document_id TEXT not null UNIQUE
                              );""")

    conn.commit()
    cursor.close()
    conn.close()
    cli()
