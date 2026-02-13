import click

@click.group()
def cli():
    pass

@click.command()
@click.option("--count", default=1, help="Number of dbs.")
@click.argument("database_name")
def initdb(count, database_name):
    click.echo(f"Initializing {count} Database {database_name}")

@click.command()
def dropdb():
    """Function to drop database"""
    click.echo("Dropping Database")

@click.command()
@click.option("--count", default=1, help="Number of greetings.")
@click.option("--name", prompt="Your name", help="The person to greet.")
def hello(count, name):
    """Simple program that greets NAME for a total of COUNT times."""
    for _ in range(count):
        click.echo(f"Hello, {name}!")

@click.command()
@click.option('-v', '--verbose', count=True)
def log(verbose):
    click.echo(f"Verbose {verbose}")

cli.add_command(initdb)
cli.add_command(dropdb)
cli.add_command(hello)
cli.add_command(log)

if __name__ == '__main__':
    cli()
