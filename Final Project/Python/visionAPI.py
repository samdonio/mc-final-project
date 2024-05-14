import os
from google.cloud import vision

def classify_image(image_path):

    # Set the environment variable for authentication
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '../api-keys/mobile-computing-423003-db46a0535e44.json'

    # Initialize the Google Vision API
    client = vision.ImageAnnotatorClient()

    # An image is read
    with open(image_path, 'rb') as image_file:
        content = image_file.read()

    # OCR
    image = vision.Image(content=content)
    response = client.document_text_detection(image=image)

    texts = response.text_annotations

    if response.error.message:
        raise Exception(f'{response.error.message}')

    print(texts)

    detected_text = texts[0].description if texts else ''
    detected_text = detected_text.strip()

    return detected_text