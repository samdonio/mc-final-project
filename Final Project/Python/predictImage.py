
from charclf.models import VGGNet
import numpy as np
from PIL import Image
import time
import torch
from torchvision import transforms
import torchvision.transforms.functional as F

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