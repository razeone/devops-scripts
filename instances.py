
import datetime

import boto3
import click

global client

client = boto3.client('ec2')


@click.command()
@click.option('--instance-state', prompt='Which instance state?',
              help='''
              The state of the instances to display:
              pending | running | shutting-down |
              terminated | stopping | stopped''')
def show_instances(instance_state):
    filters = [{
        'Name': 'instance-state-name',
        'Values': [instance_state]
    }]

    reservations = client.describe_instances(Filters=filters)
    for i in reservations['Reservations']:
        for j in i['Instances']:
            click.echo(click.style("===========================",
                                   fg='white'))
            click.echo(click.style("Tags: ", bold=True) + str(j['Tags']))
            click.echo(click.style("Instance ID: ", bold=True) +
                       j['InstanceId'])
            click.echo(click.style("Instance Type: ", bold=True) +
                       j['InstanceType'])
            click.echo(click.style("It's been running since: ", bold=True) +
                       str(j['LaunchTime']))
            now = datetime.datetime.now()
            now.replace(tzinfo=None)
            running_time = now - j['LaunchTime'].replace(tzinfo=None)
            almost_one_year = datetime.timedelta(days=360)
            more_than_2_hundred = datetime.timedelta(days=200)
            if running_time > almost_one_year:
                click.echo(click.style("Running time: ", bold=True) +
                           click.style(str(running_time), bold=True, fg='red'))
            elif running_time > more_than_2_hundred:
                click.echo(click.style("Running time: ", bold=True) +
                           click.style(str(running_time),
                                       bold=True, fg='yellow'))
            else:
                click.echo(click.style("Running time: ", bold=True) +
                           click.style(str(running_time),
                                       bold=True, fg='green'))



def get_regions():
    return client.describe_regions()


if __name__ == '__main__':
    show_instances()
