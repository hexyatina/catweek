import click
from ..core.context import AppContext
from .managing_ops import db_group

@click.group()
@click.option("--verbose", is_flag=True, help="Enable detailed logging")
@click.option("--remote", is_flag=True, help="Use remote database")
@click.pass_context
def cli(ctx, verbose, remote):
    """CATWEEK CLI: Schedule Management System"""

    ctx.obj = AppContext.create(verbose=verbose, remote_database=remote)

cli.add_command(db_group)
#cli.add_command()

if __name__ == "__main__":
    cli()