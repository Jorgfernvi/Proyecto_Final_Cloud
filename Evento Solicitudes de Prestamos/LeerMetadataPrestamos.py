import json
import boto3

def lambda_handler(event, context):
    # Entrada (json)
    archivo_id = event['Records'][0]['s3']['object']['key']
    tenant_id = archivo_id.split('/')[0] 
    moneda = archivo_id.split('/')[1] 
    #alumno_id = archivo_id.split('/')[3] 
    archivo_last_modified = event['Records'][0]['eventTime']
    archivo_size = event['Records'][0]['s3']['object']['size']
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    archivo = {
        'tenant_id': tenant_id,
        'archivo_id': archivo_id,
        'moneda': moneda,
        'archivo_datos': {
            'last_modified': archivo_last_modified,
            'size': archivo_size,
            'bucket_name': bucket_name
        }    
    }
    # Publicar en SNS
    sns_client = boto3.client('sns')
    response_sns = sns_client.publish(
        TopicArn = 'arn:aws:sns:us-east-1:859382257967:Prestamos',
        Subject = 'Nuevo Archivo',
        Message = json.dumps(archivo),
        MessageAttributes = {
            'tenant_id': {'DataType': 'String', 'StringValue': tenant_id }
        }
    )    
    # TODO implement
    return {
        'statusCode': 200,
        'body': response_sns
    }