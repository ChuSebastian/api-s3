import json
import boto3
import base64
from botocore.exceptions import ClientError

s3_client = boto3.client('s3')

def lambda_handler(event, context):
    """Lambda para subir una imagen a un bucket S3 en un directorio específico."""

    try:
        if 'body' in event:
            body = event['body']
            if isinstance(body, str):
                body = json.loads(body)
        else:
            body = event
    except Exception as e:
        return {
            'statusCode': 400,
            'body': json.dumps(f"Error al parsear el body: {str(e)}")
        }

    bucket_name = body.get('bucket_name')
    folder_name = body.get('folder_name')
    file_name = body.get('file_name')
    file_content = body.get('file_content')  # Este debe venir en base64

    if not bucket_name or not folder_name or not file_name or not file_content:
        return {
            'statusCode': 400,
            'body': json.dumps('Error: Se requiere "bucket_name", "folder_name", "file_name" y "file_content".')
        }

    # Asegurar que el folder_name termina con '/'
    if not folder_name.endswith('/'):
        folder_name += '/'

    try:
        # Decodificar contenido base64
        decoded_file = base64.b64decode(file_content)

        # Construir la key (ruta final en S3)
        key = folder_name + file_name

        # Subir el archivo
        s3_client.put_object(Bucket=bucket_name, Key=key, Body=decoded_file, ContentType='image/jpeg')

        return {
            'statusCode': 200,
            'body': json.dumps(f"Archivo '{file_name}' subido exitosamente en '{bucket_name}/{folder_name}'.")
        }

    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error al subir el archivo: {e.response['Error']['Message']}")
        }

