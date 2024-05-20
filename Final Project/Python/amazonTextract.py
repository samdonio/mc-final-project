import boto3

def classify(path):
    
    # Initialize Textract
    textract = boto3.client('textract')

    # Call Textract
    with open(path, 'rb') as file:
        response = textract.detect_document_text(Document={'Bytes': file.read()})

    # Print out the detected text
    for item in response['Blocks']:
        if item['BlockType'] == 'LINE':
            print(f'Detected text: {item['Text']}')
            print(f'Confidence: {item['Confidence']}')