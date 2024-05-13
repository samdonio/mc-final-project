from google.cloud import vision
# from google.oauth2 import service_account

file = '../Python/mobile-computing-423003-a238b69640f2.json'
client = vision.Client.from_service_account_json(file)

png = '../Data/AImage.png'

with open(png, 'rb') as f:
    content = f.read()

image = vision.Image(content=content)
response = client.document_text_detection(image=image)