import json
import boto3

def lambda_handler(event, context):
    # Entrada (json)
    print(event) # Revisar en CloudWatch
    archivo_json = json.loads(event['Records'][0]['Sns']['Message'])
    # Proceso
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Prestamo_Dolares')
    archivo = {
        'tenant_id': archivo_json['tenant_id'],
        'archivo_id': archivo_json['archivo_id'],
        'archivo_datos': archivo_json['archivo_datos']
    }
    print(archivo) # Revisar en CloudWatch
    response = table.put_item(Item=archivo)
    # Salida (json)
    return {
        'statusCode': 200,
        'response': response
    }