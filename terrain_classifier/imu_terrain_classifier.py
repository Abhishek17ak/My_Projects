import os
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from tqdm import tqdm

SEED = 42
torch.manual_seed(SEED)
np.random.seed(SEED)

class IMUConfig:
    def __init__(self):
        self.batch_size = 32
        self.lr = 1e-3
        self.lr_decay = 20
        self.momentum = 0.9
        self.weight_decay = 1e-4
        self.nepochs = 100
        self.cuda = torch.cuda.is_available()
        self.seed = SEED
        self.sequence_length = 100
        self.input_size = 6
        self.target_terrains = [
            'cement',
            'grass',
            'pebble',
            'wood_chips',
            'soil',
            'sand'
        ]

class IMUDataset(Dataset):
    def __init__(self, data_path, config, train=True):
        self.config = config
        self.train = train
        self.data, self.labels = self._load_data(data_path)
        X_train, X_test, y_train, y_test = train_test_split(
            self.data, self.labels, test_size=0.2, random_state=SEED
        )
        self.data = X_train if train else X_test
        self.labels = y_train if train else y_test
        self.scaler = StandardScaler()
        if train:
            self.data = self.scaler.fit_transform(self.data)
        else:
            self.data = self.scaler.transform(self.data)
    
    def _load_data(self, data_path):
        all_data = []
        all_labels = []
        for root, _, files in os.walk(data_path):
            for file in files:
                if file.endswith('.csv'):
                    file_path = os.path.join(root, file)
                    df = pd.read_csv(file_path)
                    imu_data = df[['ax', 'ay', 'az', 'gx', 'gy', 'gz']].values
                    terrain_type = df['terrain_type'].iloc[0]
                    if terrain_type in self.config.target_terrains:
                        for i in range(0, len(imu_data) - self.config.sequence_length, self.config.sequence_length // 2):
                            sequence = imu_data[i:i + self.config.sequence_length]
                            if len(sequence) == self.config.sequence_length:
                                all_data.append(sequence)
                                all_labels.append(self.config.target_terrains.index(terrain_type))
        return np.array(all_data), np.array(all_labels)
    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        return torch.FloatTensor(self.data[idx]), self.labels[idx]

class IMUModel(nn.Module):
    def __init__(self, config):
        super(IMUModel, self).__init__()
        self.lstm = nn.LSTM(
            input_size=config.input_size,
            hidden_size=128,
            num_layers=2,
            batch_first=True,
            dropout=0.5
        )
        self.fc = nn.Sequential(
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(64, len(config.target_terrains))
        )
    
    def forward(self, x):
        lstm_out, _ = self.lstm(x)
        last_output = lstm_out[:, -1, :]
        out = self.fc(last_output)
        return out

def train_model(model, train_loader, criterion, optimizer, epoch, device):
    model.train()
    train_loss, correct, total = 0, 0, 0
    progress_bar = tqdm(train_loader, desc=f'Epoch {epoch} [Train]', leave=True)
    for batch_idx, (data, target) in enumerate(progress_bar):
        data, target = data.to(device), target.to(device)
        optimizer.zero_grad()
        output = model(data)
        loss = criterion(output, target)
        loss.backward()
        optimizer.step()
        train_loss += loss.item()
        _, predicted = output.max(1)
        total += target.size(0)
        correct += predicted.eq(target).sum().item()
        progress_bar.set_postfix({
            'Loss': f'{train_loss/(batch_idx+1):.3f}',
            'Acc': f'{100.*correct/total:.3f}% ({correct}/{total})'
        })
    return 100. * correct / total

def test_model(model, test_loader, criterion, device):
    model.eval()
    test_loss, correct, total = 0, 0, 0
    progress_bar = tqdm(test_loader, desc='[Test]', leave=True)
    with torch.no_grad():
        for batch_idx, (data, target) in enumerate(progress_bar):
            data, target = data.to(device), target.to(device)
            output = model(data)
            loss = criterion(output, target)
            test_loss += loss.item()
            _, predicted = output.max(1)
            total += target.size(0)
            correct += predicted.eq(target).sum().item()
            progress_bar.set_postfix({
                'Loss': f'{test_loss/(batch_idx+1):.3f}',
                'Acc': f'{100.*correct/total:.3f}% ({correct}/{total})'
            })
    return 100. * correct / total

def main():
    config = IMUConfig()
    device = torch.device("cuda" if config.cuda else "cpu")
    print(f"Using device: {device}")
    data_path = "imu_data"
    train_dataset = IMUDataset(data_path, config, train=True)
    test_dataset = IMUDataset(data_path, config, train=False)
    train_loader = DataLoader(train_dataset, batch_size=config.batch_size, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=config.batch_size, shuffle=False)
    model = IMUModel(config).to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=config.lr, weight_decay=config.weight_decay)
    best_acc = 0
    train_accs = []
    test_accs = []
    for epoch in range(1, config.nepochs + 1):
        if epoch % config.lr_decay == 0:
            for param_group in optimizer.param_groups:
                param_group['lr'] *= 0.1
        train_acc = train_model(model, train_loader, criterion, optimizer, epoch, device)
        test_acc = test_model(model, test_loader, criterion, device)
        train_accs.append(train_acc)
        test_accs.append(test_acc)
        if test_acc > best_acc:
            best_acc = test_acc
            torch.save(model.state_dict(), 'best_imu_model.pth')
            print(f'Best accuracy: {best_acc:.2f}%')
    plt.figure(figsize=(10, 5))
    plt.plot(range(1, config.nepochs + 1), train_accs, label='Train Accuracy')
    plt.plot(range(1, config.nepochs + 1), test_accs, label='Test Accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy (%)')
    plt.title('IMU-based Terrain Classification - Training and Testing Accuracy')
    plt.legend()
    plt.grid(True)
    plt.show()
    print(f'Best accuracy: {best_acc:.2f}%')
    return model

if __name__ == "__main__":
    main() 