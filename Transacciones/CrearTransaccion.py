import json
import boto3

def lambda_handler(event, context):
    # Entrada (json)
    transaction_id = event['transaction_id']
    account_id = event['account_id']
    amount = event['amount']
    transaction_type = event['transaction_type']
    currency = event['currency']
    status = event['status']
    
    # Proceso
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Transactions')
    transaction = {
        'transaction_id': transaction_id,
        'account_id': account_id,
        'amount': amount,
        'transaction_type': transaction_type,
        'currency': currency,
        'status': status
    }
    response = table.put_item(Item=transaction)
    
    # Publicar en SNS
    sns_client = boto3.client('sns')
    response_sns = sns_client.publish(
        TopicArn='arn:aws:sns:us-east-1:859382257967:Banco',
        Subject='Nueva Transaccion',
        Message=json.dumps(transaction),
        MessageAttributes={
            'transaction_id': {'DataType': 'String', 'StringValue': transaction_id }
        }
    )
    print(response_sns)
    
    # Salida (json)
    return {
        'statusCode': 200,
        'response': response
    }
