import boto3

def lambda_handler(event, context):
    try:
        # Entrada (json)
        transaction_id = event['transaction_id']
        
        # Proceso
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('Transactions')  # Nombre de la tabla de transacciones
        
        # Eliminar la transacción de DynamoDB
        response = table.delete_item(
            Key={
                'transaction_id': str(transaction_id)
            }
        )
        
        # Salida (json)
        return {
            'statusCode': 200,
            'response': response
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'errorMessage': str(e)
        }
