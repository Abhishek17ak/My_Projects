# Terrain Classification System: A Multi-Modal Approach

A robust terrain classification system that combines IMU and visual data using deep learning for accurate terrain identification.

## Features

- **Multi-Modal Classification**: Combines IMU and visual data for robust terrain identification
- **Deep Learning Models**: 
  - LSTM-based IMU classifier
  - MobileNetV2-based visual classifier
  - Ensemble approach with configurable weights
- **Supported Terrains**: Cement, Grass, Pebble, Wood Chips, Soil, Sand
- **Real-time Prediction**: Fast inference with confidence scores
- **Modular Design**: Easy to extend and modify

## Installation

```bash
# Clone the repository
git clone [repository-url]
cd terrain-classification

# Install dependencies
pip install -r requirements.txt
```

## Quick Start

```python
from ensemble_terrain_classifier import EnsembleConfig, EnsembleModel

# Initialize the model
config = EnsembleConfig()
model = EnsembleModel(config)

# Make a prediction
result = model.predict(imu_data, rgb_image, diff_image)
print(f"Terrain: {result['terrain']}")
print(f"Confidence: {result['confidence']:.2f}")
```

## System Architecture

### IMU-based Classifier
- LSTM neural network
- 6-axis IMU data processing (accelerometer and gyroscope)
- 100-sample sequence length
- Features: ax, ay, az, gx, gy, gz

### Visual-based Classifier
- Dual-stream MobileNetV2 architecture
- RGB and differential image processing
- DAIN (Dual Attention Integration Network)
- 224x224 pixel input size

### Ensemble Classifier
- Weighted combination (40% IMU, 60% visual)
- Confidence score tracking
- Real-time prediction capability

## Model Details

### IMU Model
- 2 LSTM layers (128 hidden units)
- 0.5 dropout for regularization
- Fully connected layers: 128 → 64 → 6
- Adam optimizer with weight decay

### Visual Model
- MobileNetV2 backbone
- Custom normalization for RGB and differential images
- DAIN feature fusion
- 6-class classification output

## Data Processing

### IMU Data
1. CSV file loading
2. 100-sample window segmentation
3. Standard scaling
4. Batch processing

### Visual Data
1. 256x256 resizing
2. 224x224 center cropping
3. RGB and differential normalization
4. Tensor conversion

## Training

### IMU Model
- Batch size: 32
- Learning rate: 1e-3
- 100 epochs
- LR decay every 20 epochs

### Visual Model
- Batch size: 32
- Learning rate: 1e-2
- 50 epochs
- LR decay every 40 epochs

## Requirements

### Dependencies
- PyTorch
- NumPy
- PIL (Python Imaging Library)
- torchvision
- CUDA support (optional)

### Hardware
- CPU: Multi-core processor
- RAM: 8GB minimum (16GB recommended)
- GPU: NVIDIA GPU with CUDA support (optional)
- Storage: 1GB minimum

## Future Improvements

- Dynamic weight adjustment
- Additional sensor modalities
- Real-time adaptation
- Edge case handling
- Alternative architectures
- Different ensemble methods

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[Add your license here]

## References

1. MobileNetV2: Inverted Residuals and Linear Bottlenecks
2. LSTM-based Sequence Classification
3. DAIN: Dual Attention Integration Network
4. Ensemble Methods in Machine Learning 