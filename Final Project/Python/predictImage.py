import time
from PIL import Image
import torch
from torch.utils.data import DataLoader
from charclf.dataset import load_dataset
from charclf.models import VGGNet, AlexNet, SpinalNet, ResNet
from charclf.tools.eval import multi_evaluate, evaluate, confusion_matrix_viz
from charclf.tools.viz import predict
from charclf.tools.train import train_
# import cv2
import numpy as np
import torch
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
import torchvision.transforms as transforms
import torchvision.transforms.functional as F
from PIL import Image

class AlwaysMirrorAndRotate(object):
    def __call__(self, img):
        # Always mirror (horizontal flip)
        img = F.hflip(img)
        # Always rotate 90 degrees counter-clockwise
        img = img.rotate(90, expand=True)
        return img

def predict_character(img: Image, model) -> str:
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    class AlwaysMirrorAndRotate(object):
        def __call__(self, img):
            img = F.hflip(img)  # Always mirror (horizontal flip)
            img = img.rotate(90, expand=True)  # Always rotate 90 degrees counter-clockwise
            return img

    # Define the transformation
    mean = 0.1736
    std = 0.3248
    transform = transforms.Compose([
        AlwaysMirrorAndRotate(),
        transforms.ToTensor(),
        transforms.Normalize((mean,), (std,))
    ])

    # Assuming img is your single image, already loaded as a PIL Image
    img_transformed = transform(img)
    img_transformed = img_transformed.unsqueeze(0)  # Add batch dimension
    img_transformed = img_transformed.to(device).float()

    # Assuming label is not used in the inference step
    with torch.no_grad():
        outputs = model(img_transformed)
        _, predicted = torch.max(outputs.data, 1)
        pred_label = predicted[0].item()

    return pred_label