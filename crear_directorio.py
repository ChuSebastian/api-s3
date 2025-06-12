import json
import boto3
from botocore.exceptions import ClientError

s3_client = boto3.client('s3')

def lambda_handler(event, context):
    """Lambda para crear un 'directorio' (objeto con sufijo '/') en un bucket S3."""
    try:
        body = json.loads(event.get('body', '{}'))
    except Exception as e:
        return {
            'statusCode': 400,
            'body': json.dumps(f"Error al parsear el body: {str(e)}")
        }

    bucket_name = body.get('bucket_name')
    folder_name = body.get('folder_name')

    if not bucket_name or not folder_name:
        return {
            'statusCode': 400,
            'body': json.dumps('Error: Se requiere "bucket_name" y "folder_name".')
        }

    # Asegurar que el "folder_name" termina con "/"
    if not folder_name.endswith('/'):
        folder_name += '/'

    try:
        # Crear objeto vacío para simular la carpeta
        s3_client.put_object(Bucket=bucket_name, Key=folder_name)
        return {
            'statusCode': 200,
            'body': json.dumps(f"Directorio '{folder_name}' creado en el bucket '{bucket_name}'.")
        }
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error al crear el directorio: {e.response['Error']['Message']}")
        }

