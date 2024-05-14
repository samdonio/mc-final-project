import os
from google.cloud import vision

def classify_image(image_path):
    # Set the environment variable for authentication
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '../api-keys/mobile-computing-423003-db46a0535e44.json'

    # Initialize the Google Vision API client
    client = vision.ImageAnnotatorClient()

    # Load the image
    with open(image_path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    # Perform text detection on the image
    
    response = client.text_detection(image=image)
    texts = response.text_annotations

    if response.error.message:
        raise Exception(f'{response.error.message}')

    print(texts)

    # Extract the detected text
    detected_text = texts[0].description if texts else ''
    detected_text = detected_text.strip()

    return detected_text

# if __name__ == "__main__":
#     image_path = '../path_to_your_image.jpg'  # Replace with the path to your image
#     result = classify_image(image_path)
#     if result:
#         print(f'The image contains: {result}')
#     else:
#         print('The image does not contain a single letter or digit.')
