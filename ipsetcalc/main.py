import click
from netaddr import IPSet


@click.command()
@click.argument("expression", nargs=-1)
def main(expression):
    operator = expression[1]
    token1= expression[0]
    token2 = expression[2]

    if operator == "-":
        result = IPSet([token1]) - IPSet([token2])
        for item in result.iter_cidrs():
            print(item)
