import boto3
import json
import crhelper
import time
import os

# initialise logger
print('Loading function')
print('variables being passed....')

TRANSITGTW = os.environ['TRANSITGTW']
RT = os.environ['RT']
CIDR = os.environ['CIDR']

print(f'TRANSITGTW = {TRANSITGTW}')
print(f'RT = {RT}')
print(f'CIDR = {CIDR}')


logger = crhelper.log_config({"RequestId": "CONTAINER_INIT"})
logger.info('Logging configured')
# set global to track init failures
init_failed = False

try:
    # Place initialization code here
    logger.info("Container initialization completed")
except Exception as e:
    logger.error(e, exc_info=True)
    init_failed = e


def create(event, context):

    ec2 = boto3.resource('ec2')
    route_table = ec2.RouteTable(f'{RT}')
    route = route_table.create_route(DestinationCidrBlock=f'{CIDR}',TransitGatewayId=f'{TRANSITGTW}')

    response_data = {}
    physical_resource_id = 'myResourceId'
    
    return physical_resource_id, response_data


def update(event, context):


    return physical_resource_id, response_data


def delete(event, context):

    client = boto3.client('ec2')
    response = client.delete_route(DestinationCidrBlock=f'{CIDR}',RouteTableId=f'{RT}')

    return


def handler(event, context):
    """
    Main handler function, passes off it's work to crhelper's cfn_handler
    """
    print('CloudFormation event received: %s' % str(event))
    # update the logger with event info
    global logger
    logger = crhelper.log_config(event)
    return crhelper.cfn_handler(event, context, create, update, delete, logger, init_failed)