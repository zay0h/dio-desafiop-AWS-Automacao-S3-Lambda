import json

def lambda_handler(event, context):
    """
    Ponto de entrada da função. O objeto 'event' é o payload enviado pelo S3.
    """
    try:
        # A chave é ler a estrutura do evento S3 (que contém uma lista de Records)
        for record in event['Records']:
            bucket_name = record['s3']['bucket']['name']
            object_key = record['s3']['object']['key']

            # Insight: A função extrai o nome do arquivo para saber qual recurso processar.
            print(f"INFO: Novo objeto detectado: {object_key} no bucket {bucket_name}")

            # --- LÓGICA DE NEGÓCIO ENTRA AQUI ---
            # Ex: Chamada ao Boto3 para ler o conteúdo do objeto
            # Ex: Processamento do arquivo (redimensionar imagem, ler CSV, etc.)
            # ------------------------------------

        return {
            'statusCode': 200,
            'body': json.dumps('Evento S3 processado com sucesso pela Lambda.')
        }
    except Exception as e:
        print(f"ERRO: Falha ao processar evento S3: {e}")
        raise e
