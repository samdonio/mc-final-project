from flask import Flask, request
import pandas as pd
import torch
from dataToPredict import csv_to_image
from charclf.models import VGGNet, AlexNet, SpinalNet, ResNet
import time

app = Flask(__name__)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
vggnet = VGGNet()
vggnet.to(device).load_state_dict(torch.load("model_hub/fine_tuned/vggnet_tuned.pth", map_location=device))
model = vggnet
model.eval()

@app.route('/')
def hello_world():
    return 'Hello, World!'

def rename_keys(dict):
    return {'x_pos': dict['x'],
            'y_pos': dict['y'],
            'z_pos': dict['z']}

@app.route('/character', methods=['POST'])
def character_classifier():
    start_time = time.time()

    # Access JSON data (application/json)
    json_data = map(rename_keys, (request.json)['data'])
    if not json_data:
        return "No Data in Request", 400


    # for key in json_data:
    #     print(key)
    # print(json_data)

    
    df = pd.DataFrame(json_data)
    result = df[['x_pos', 'z_pos']]
    end_time = time.time()
    result = csv_to_image(result, model)
    end2_time = time.time()
    print(end_time - start_time)
    print(end2_time - end_time)

    print(f'The expected character is: {result}')
    return result, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

    