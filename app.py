import json
import boto3
from decimal import Decimal
import logging


def default_serializer(obj):
    if isinstance(obj, Decimal):
        return int(obj) if obj % 1 == 0 else float(obj)
    raise TypeError

def lambda_handler(event, context):

    logging.getLogger().setLevel(logging.INFO)
    logging.info('starting lambda')
    try:
        dynamodb = boto3.resource('dynamodb')
        usuarios = dynamodb.Table('Usuarios')

        logging.info(f"Evento recibido: {event}")

        # body = event['body'] if 'body' in event else None
        params = event.get('queryStringParameters')
        logging.info(f"params: {params}")  
        if isinstance(params, str):
            data = json.loads(params) if params else {}
        else:
            data = params or {}  
        usuario = usuarios.get_item(Key={'id': data['id']})
        if usuario.get('Item') is None:
            logging.error(f"Usuario no encontrado: {data['id']}")
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'Usuario no encontrado en la tabla usuarios'})
            }
        logging.info(f"usuario: {usuario}")  
        return {
            'statusCode': 200,
            'body': json.dumps(usuario.get('Item') , default=default_serializer)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
