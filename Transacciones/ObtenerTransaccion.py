import json
import boto3

def lambda_handler(event, context):
    try:
        # Entrada (json)
        transaction_id = event['transaction_id']
        
        # Proceso
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('Transactions')
        
        # Obtener la transacción desde DynamoDB
        response = table.get_item(
            Key={'transaction_id': transaction_id}
        )
        
        # Verificar si se encontró la transacción
        if 'Item' in response:
            transaction = response['Item']
            
            # Publicar en SNS
            sns_client = boto3.client('sns')
            response_sns = sns_client.publish(
                TopicArn='arn:aws:sns:us-east-1:859382257967:Banco',
                Subject='Consulta de Transaccion',
                Message=json.dumps(transaction),
                MessageAttributes={
                    'transaction_id': {'DataType': 'String', 'StringValue': transaction_id }
                }
            )
            print(response_sns)
            
            # Retornar la transacción encontrada
            return {
                'statusCode': 200,
                'transaction': transaction
            }
        else:
            # Si no se encuentra la transacción, retornar un error
            return {
                'statusCode': 404,
                'errorMessage': 'Transaction not found'
            }

    except Exception as e:
        # Capturar cualquier excepción y retornar un error 500
        return {
            'statusCode': 500,
            'errorMessage': str(e)
        }
