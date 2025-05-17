import os
import torch
import torch.nn as nn
import numpy as np
from PIL import Image
import torchvision.transforms as transforms
from imu_terrain_classifier import IMUModel, IMUConfig as IMUConfig
from visual_terrain_classifier import DAIN, mobilenet_v2, VisualConfig as VisualConfig

class EnsembleConfig:
    def __init__(self):
        self.imu_config = IMUConfig()
        self.visual_config = VisualConfig()
        self.ensemble_weights = {
            'imu': 0.4,
            'visual': 0.6
        }
        self.target_terrains = [
            'cement',
            'grass',
            'pebble',
            'wood_chips',
            'soil',
            'sand'
        ]

class EnsembleModel:
    def __init__(self, config):
        self.config = config
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        self.imu_model = IMUModel(config.imu_config).to(self.device)
        self.imu_model.load_state_dict(torch.load('best_imu_model.pth'))
        self.imu_model.eval()
        
        backbone1 = mobilenet_v2(pretrained=False)
        backbone2 = mobilenet_v2(pretrained=False)
        self.visual_model = DAIN(len(config.target_terrains), backbone1, backbone2).to(self.device)
        self.visual_model.load_state_dict(torch.load('best_visual_model.pth'))
        self.visual_model.eval()
        
        self.rgbnormalize = transforms.Normalize(mean=[0.447, 0.388, 0.340],
                                         std=[0.216, 0.204, 0.197])
        self.diffnormalize = transforms.Normalize(mean=[0.495, 0.495, 0.495],
                                         std=[0.07, 0.07, 0.07])
        
        self.visual_transform = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            self.rgbnormalize,
        ])
        
        self.diff_transform = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            self.diffnormalize,
        ])

    def preprocess_imu(self, imu_data):
        imu_data = torch.FloatTensor(imu_data).unsqueeze(0).to(self.device)
        return imu_data

    def preprocess_visual(self, rgb_image, diff_image):
        rgb_image = Image.fromarray(rgb_image).convert('RGB')
        diff_image = Image.fromarray(diff_image).convert('RGB')
        
        rgb_tensor = self.visual_transform(rgb_image).unsqueeze(0).to(self.device)
        diff_tensor = self.diff_transform(diff_image).unsqueeze(0).to(self.device)
        
        return rgb_tensor, diff_tensor

    def predict(self, imu_data, rgb_image, diff_image):
        with torch.no_grad():
            imu_input = self.preprocess_imu(imu_data)
            rgb_tensor, diff_tensor = self.preprocess_visual(rgb_image, diff_image)
            
            imu_output = self.imu_model(imu_input)
            visual_output = self.visual_model(rgb_tensor, diff_tensor)
            
            imu_probs = torch.softmax(imu_output, dim=1)
            visual_probs = torch.softmax(visual_output, dim=1)
            
            ensemble_probs = (
                self.config.ensemble_weights['imu'] * imu_probs +
                self.config.ensemble_weights['visual'] * visual_probs
            )
            
            prediction = torch.argmax(ensemble_probs, dim=1).item()
            confidence = ensemble_probs[0][prediction].item()
            
            return {
                'terrain': self.config.target_terrains[prediction],
                'confidence': confidence,
                'imu_confidence': imu_probs[0][prediction].item(),
                'visual_confidence': visual_probs[0][prediction].item()
            }

def main():
    config = EnsembleConfig()
    model = EnsembleModel(config)
    
    print("Ensemble Terrain Classifier")
    print("==========================")
    print("Model loaded successfully!")
    print(f"Using device: {model.device}")
    print("\nAvailable terrain types:")
    for terrain in config.target_terrains:
        print(f"- {terrain}")
    print("\nEnsemble weights:")
    print(f"IMU: {config.ensemble_weights['imu']}")
    print(f"Visual: {config.ensemble_weights['visual']}")
    
    return model

if __name__ == "__main__":
    main() 