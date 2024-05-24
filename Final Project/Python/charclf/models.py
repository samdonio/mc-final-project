import torch
import torch.nn.functional as F
from torch import nn
from torch.nn import init
import warnings
warnings.filterwarnings('ignore') # Avoid warnings caused by libraries' version conflicts

# A variant of VGGNet
class VGGNet(nn.Module):
  def __init__(self, num_classes=62):
    super(VGGNet, self).__init__()
    self.features = nn.Sequential(
      # Block 1
      nn.Conv2d(1, 16, kernel_size=3, padding=1),
      nn.ReLU(inplace=True),

      # Block 2
      nn.Conv2d(16, 32, kernel_size=3, padding=1),
      nn.ReLU(inplace=True),
      nn.MaxPool2d(kernel_size=2, stride=2),

      # Block 3
      nn.Conv2d(32, 64, kernel_size=3, padding=1),
      nn.ReLU(inplace=True),
      nn.Conv2d(64, 64, kernel_size=3, padding=1),
      nn.ReLU(inplace=True),

      # Block 4
      nn.Conv2d(64, 128, kernel_size=3, stride=1, padding=1),
      nn.ReLU(inplace=True),
      nn.Conv2d(128, 128, kernel_size=3, stride=1, padding=1),
      nn.ReLU(inplace=True),
      nn.MaxPool2d(kernel_size=2, stride=2),
      
      # Block 5
      nn.Conv2d(128, 128, kernel_size=3, stride=1, padding=1),
      nn.ReLU(inplace=True),
      nn.Conv2d(128, 128, kernel_size=3, stride=1, padding=1),
      nn.ReLU(inplace=True),
    )
    self.avgpool = nn.AdaptiveAvgPool2d((3, 3))
    self.classifier = nn.Sequential(
      nn.Linear(128 * 3 * 3, 512),
      nn.BatchNorm1d(512),
      nn.ReLU(inplace=True),
      nn.Dropout(),
      nn.Linear(512, 512),
      nn.BatchNorm1d(512),
      nn.ReLU(inplace=True),
      nn.Dropout(),
      nn.Linear(512, num_classes),
    )
    self._initialize_weights()

  def forward(self, x):
    x = self.features(x)
    x = self.avgpool(x)
    x = torch.flatten(x, 1)
    x = self.classifier(x)
    return x

  def _initialize_weights(self):
    for m in self.modules():
      if isinstance(m, nn.Conv2d):
        init.kaiming_normal_(m.weight, mode='fan_out', nonlinearity='relu')
        if m.bias is not None:
          init.constant_(m.bias, 0)
      elif isinstance(m, nn.BatchNorm2d):
        init.constant_(m.weight, 1)
        init.constant_(m.bias, 0)
      elif isinstance(m, nn.Linear):
        init.normal_(m.weight, 0, 0.01)
        init.constant_(m.bias, 0)
