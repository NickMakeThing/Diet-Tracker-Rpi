import boto3

def image_to_data(file):
    #file = 'test images\\rice.jpg'
    with open(file, 'rb') as f:
        imageBytes = bytearray(f.read())

    textract = boto3.client('textract',
        aws_access_key_id = 'AKIAXPOLFBYIEZPC3JKN',
        aws_secret_access_key = '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',
        region_name = 'ap-southeast-2'
    )

    response = textract.analyze_document(Document={'Bytes': imageBytes},FeatureTypes=['TABLES'])
    return response