import json
import boto3
from botocore.exceptions import ClientError

# Cliente S3
s3_client = boto3.client('s3')

def lambda_handler(event, context):
    """Lambda para crear un bucket S3 con manejo correcto de región."""

    try:
        # Obtener body del evento
        body = json.loads(event.get('body', '{}'))
    except Exception as e:
        return {
            'statusCode': 400,
            'body': json.dumps(f"Error al parsear el body: {str(e)}")
        }

    # Extraer el nombre del bucket
    bucket_name = body.get('bucket_name')

    if not bucket_name:
        return {
            'statusCode': 400,
            'body': json.dumps('Error: El nombre del bucket no fue proporcionado.')
        }

    try:
        # Obtener la región actual donde corre la Lambda
        session = boto3.session.Session()
        current_region = session.region_name

        # Condición especial para us-east-1 (no requiere LocationConstraint)
        if current_region == 'us-east-1':
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={'LocationConstraint': current_region}
            )

        return {
            'statusCode': 200,
            'body': json.dumps(f"Bucket '{bucket_name}' creado exitosamente en la región '{current_region}'.")
        }

    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error al crear el bucket: {e.response['Error']['Message']}")
        }

