# import os
from google.cloud import aiplatform

def recognize(image_path):

    # Initialize the Vertex AI client
    client = aiplatform.gapic.DatasetServiceClient()

    # Define data
    data_name = 'GCS_name'
    data_location = 'GCS_location'
    
    # data_metadata = {'input_config': {'gcs_source': {'uri': data_location}}}
    # data = {'name': data_name, 'metadata': data_metadata}

    # predictions = response.predictions

    # for prediction in predictions:
    #     label = prediction['display_name']
    #     score = prediction['classification']['score']
    #     print("Label: {label}, Score: {score}")

    return ""