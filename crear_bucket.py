import json
import boto3
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    """Lambda para crear un bucket S3. El nombre del bucket se recibe vía evento JSON."""
    s3_client = boto3.client('s3')

    # Obtener el nombre del bucket desde el evento
    bucket_name = event.get('bucket_name')
    
    if not bucket_name:
        return {
            'statusCode': 400,
            'body': json.dumps('Error: El nombre del bucket no fue proporcionado.')
        }

    try:
        s3_client.create_bucket(Bucket=bucket_name)
        return {
            'statusCode': 200,
            'body': json.dumps(f"Bucket '{bucket_name}' creado exitosamente.")
        }
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error al crear el bucket: {e.response['Error']['Message']}")
        }

