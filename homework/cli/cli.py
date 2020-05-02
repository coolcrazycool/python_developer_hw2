from homework.patient import Patient, PatientCollection
import click


@click.group()
def cli():
    pass


@click.command()
@click.argument('f_name')
@click.argument('s_name')
@click.option('--birth-date')
@click.option('--phone')
@click.option('--document-type')
@click.option('--document-number')
def create(f_name, s_name, birth_date, phone, document_type, document_number):
    print(f_name, s_name, birth_date, phone, document_type, document_number)
    patient = Patient(f_name, s_name, birth_date, phone, document_type, document_number)
    patient.save()
    del patient


@click.command()
def show(limit=10):
    collection = PatientCollection('homework/covid_19_db.db')
    for i in collection.limit(limit):
        print(i)


@click.command()
def count():
    collection = PatientCollection('homework/covid_19_db.db')
    for i in collection.limit(None):
        print(i)


cli.add_command(create)
cli.add_command(show)
cli.add_command(count)

if __name__ == '__main__':
    cli()
