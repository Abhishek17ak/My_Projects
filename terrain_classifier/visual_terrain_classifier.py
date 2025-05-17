import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import random
import math
from tqdm import tqdm

import torch
import torch.nn as nn
import torch.optim as optim
import torch.utils.data as data
import torchvision.transforms as transforms
import torchvision.transforms.functional as TF
from torch.autograd import Variable

SEED = 42
torch.manual_seed(SEED)
np.random.seed(SEED)
random.seed(SEED)
if torch.cuda.is_available():
    torch.cuda.manual_seed(SEED)

class VisualConfig:
    def __init__(self):
        current_dir = os.getcwd()
        possible_paths = [
            os.path.join(current_dir, "gtos", "gtos"),
            os.path.join(current_dir, "gtos"),
            os.path.join(os.path.dirname(current_dir), "gtos", "gtos"),
            os.path.join(os.path.dirname(current_dir), "gtos")
        ]
        
        self.dataset_path = None
        for path in possible_paths:
            if os.path.exists(path):
                self.dataset_path = path
                break
        
        if self.dataset_path is None:
            raise ValueError(
                "Could not find the GTOS dataset. Please ensure the dataset is in one of these locations:\n" +
                "\n".join(f"- {path}" for path in possible_paths)
            )
            
        print(f"Dataset path: {self.dataset_path}")
        
        self.batch_size = 32
        self.lr = 1e-2
        self.lr_decay = 40
        self.momentum = 0.9
        self.weight_decay = 1e-4
        self.nepochs = 50
        self.cuda = torch.cuda.is_available()
        self.gpu = '0'
        self.split = '1'
        self.seed = SEED
        self.target_terrains = [
            'cement',
            'grass',
            'pebble',
            'wood_chips',
            'soil',
            'sand'
        ]
        
        self._verify_dataset_path()
    
    def _verify_dataset_path(self):
        print("\nVerifying dataset structure...")
        
        if not os.path.exists(self.dataset_path):
            raise ValueError(f"Dataset path does not exist: {self.dataset_path}")
        print(f"✓ Dataset path exists: {self.dataset_path}")
        
        required_dirs = ['color_imgs', 'diff_imgs', 'labels']
        missing_dirs = []
        for dir_name in required_dirs:
            dir_path = os.path.join(self.dataset_path, dir_name)
            if not os.path.exists(dir_path):
                missing_dirs.append(dir_path)
            else:
                print(f"✓ Found directory: {dir_name}")
        
        if missing_dirs:
            raise ValueError(
                "Missing required directories in dataset:\n" +
                "\n".join(f"- {dir_path}" for dir_path in missing_dirs) +
                "\n\nPlease ensure the dataset is properly extracted and all required directories are present."
            )
        
        class_ind_path = os.path.join(self.dataset_path, 'labels', 'classInd.txt')
        if not os.path.exists(class_ind_path):
            raise ValueError(
                f"Class labels file not found: {class_ind_path}\n" +
                "Please ensure the dataset is properly extracted and contains the class labels file."
            )
        print(f"✓ Found class labels file: {class_ind_path}")
        
        train_file = os.path.join(self.dataset_path, 'labels', f'train{self.split}.txt')
        test_file = os.path.join(self.dataset_path, 'labels', f'test{self.split}.txt')
        missing_files = []
        if not os.path.exists(train_file):
            missing_files.append(train_file)
        if not os.path.exists(test_file):
            missing_files.append(test_file)
            
        if missing_files:
            raise ValueError(
                "Missing required split files:\n" +
                "\n".join(f"- {file_path}" for file_path in missing_files) +
                "\n\nPlease ensure the dataset is properly extracted and contains all required split files."
            )
        print(f"✓ Found train/test split files")
        
        print("\nAvailable classes in dataset:")
        try:
            with open(class_ind_path, 'r') as f:
                for line in f:
                    print(f"  {line.strip()}")
        except Exception as e:
            print(f"Warning: Could not read class labels file: {e}")
        
        print("\nDataset structure verification complete!")

def find_classes(classdir):
    classes = []
    class_to_idx = {}
    with open(classdir, 'r') as f:
        for line in f:
            label, name = line.split(' ')
            name = name.strip()
            classes.append(name)
            class_to_idx[name] = int(label) - 1
    return classes, class_to_idx

def make_dataset(txtname, datadir, target_terrains=None):
    print(f"\nLoading dataset from: {txtname}")
    rgbimages = []
    diffimages = []
    labels = []
    terrain_indices = []
    
    classes, _ = find_classes(os.path.join(datadir, 'labels/classInd.txt'))
    print(f"Found {len(classes)} total classes in dataset")
    
    if target_terrains:
        print("\nFiltering for target terrain types:")
        for terrain in target_terrains:
            if terrain in classes:
                terrain_indices.append(classes.index(terrain))
                print(f"  ✓ Found: {terrain}")
            else:
                print(f"  ✗ Not found: {terrain}")
    
    if not os.path.exists(txtname):
        raise ValueError(f"Split file not found: {txtname}")
    
    print(f"\nReading image paths from: {txtname}")
    with open(txtname, "r") as lines:
        for line in lines:
            name, label = line.split(' ')
            label = int(label) - 1
            name = name.split('/')[-1]
            
            if target_terrains and label not in terrain_indices:
                continue
                
            if target_terrains:
                new_label = terrain_indices.index(label)
            else:
                new_label = label
                
            diff_dir = os.path.join(datadir, 'diff_imgs', name)
            if os.path.exists(diff_dir):
                for filename in os.listdir(diff_dir):
                    _rgbimg = os.path.join(datadir, 'color_imgs', name, filename)
                    _diffimg = os.path.join(datadir, 'diff_imgs', name, filename)
                    if os.path.isfile(_rgbimg) and os.path.isfile(_diffimg):
                        rgbimages.append(_rgbimg)
                        diffimages.append(_diffimg)
                        labels.append(new_label)
    
    if len(rgbimages) == 0:
        raise ValueError(f"No valid images found in {txtname}. Please check the dataset structure and paths.")
    
    print(f"\nFound {len(rgbimages)} valid image pairs")
    print("Class distribution:")
    unique_labels = set(labels)
    for label in sorted(unique_labels):
        count = labels.count(label)
        class_name = classes[label] if not target_terrains else target_terrains[label]
        print(f"  {class_name}: {count} images")
    
    return rgbimages, diffimages, labels

class GTOSDataloader(data.Dataset):
    def __init__(self, config, train=True, transform=None):
        print(f"\nInitializing {'training' if train else 'testing'} dataset...")
        
        if hasattr(config, 'target_terrains') and config.target_terrains:
            self.classes = config.target_terrains
            class_to_idx = {name: i for i, name in enumerate(self.classes)}
            print(f"Using target terrain types: {self.classes}")
        else:
            self.classes, class_to_idx = find_classes(os.path.join(config.dataset_path, 'labels/classInd.txt'))
            print(f"Using all available classes: {self.classes}")
            
        self.class_to_idx = class_to_idx
        self.train = train
        self.transform = transform
        self.rgbnormalize = transforms.Normalize(mean=[0.447, 0.388, 0.340],
                                         std=[0.216, 0.204, 0.197])
        self.diffnormalize = transforms.Normalize(mean=[0.495, 0.495, 0.495],
                                         std=[0.07, 0.07, 0.07])
        
        if train:
            filename = os.path.join(config.dataset_path, 'labels/train'+ config.split +'.txt')
        else:
            filename = os.path.join(config.dataset_path, 'labels/test'+ config.split +'.txt')

        target_terrains = config.target_terrains if hasattr(config, 'target_terrains') else None
        self.rgbimages, self.diffimages, self.labels = make_dataset(filename, config.dataset_path, target_terrains)
        assert (len(self.rgbimages) == len(self.labels))
        
        print(f"\nDataset initialization complete!")
        print(f"Total images: {len(self.rgbimages)}")
        print(f"Classes: {self.classes}")

    def train_transform(self, _rgbimg, _diffimg):
        resize = transforms.Resize(size=(256, 256))
        _rgbimg, _diffimg = resize(_rgbimg), resize(_diffimg)

        i, j, h, w = transforms.RandomCrop.get_params(
            _rgbimg, output_size=(224, 224))
        _rgbimg = TF.crop(_rgbimg, i, j, h, w)
        _diffimg = TF.crop(_diffimg, i, j, h, w)

        if random.random() > 0.5:
            _rgbimg = TF.hflip(_rgbimg)
            _diffimg = TF.hflip(_diffimg)
        if random.random() > 0.5:
            _rgbimg = TF.vflip(_rgbimg)
            _diffimg = TF.vflip(_diffimg)

        _rgbimg = TF.to_tensor(_rgbimg)
        _diffimg = TF.to_tensor(_diffimg)

        _rgbimg = self.rgbnormalize(_rgbimg)
        _diffimg = self.diffnormalize(_diffimg)

        return _rgbimg, _diffimg

    def test_transform(self, _rgbimg, _diffimg):
        rgbtransform_test = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            self.rgbnormalize,
        ])

        difftransform_test = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            self.diffnormalize,
        ])

        _rgbimg = rgbtransform_test(_rgbimg)
        _diffimg = difftransform_test(_diffimg)

        return _rgbimg, _diffimg

    def __getitem__(self, index):
        _rgbimg = Image.open(self.rgbimages[index]).convert('RGB')
        _diffimg = Image.open(self.diffimages[index]).convert('RGB')
        _label = self.labels[index]
        
        if self.transform is not None:
            if self.train:
                _rgbimg, _diffimg = self.train_transform(_rgbimg, _diffimg)
            else:
                _rgbimg, _diffimg = self.test_transform(_rgbimg, _diffimg)

        return _rgbimg, _diffimg, _label

    def __len__(self):
        return len(self.rgbimages)

class Dataloader():
    def __init__(self, config):
        trainset = GTOSDataloader(config, train=True, transform=True)
        testset = GTOSDataloader(config, train=False, transform=True)
    
        kwargs = {'num_workers': 2, 'pin_memory': True} if config.cuda else {}
        self.trainloader = torch.utils.data.DataLoader(trainset, batch_size=
            config.batch_size, shuffle=True, **kwargs)
        self.testloader = torch.utils.data.DataLoader(testset, batch_size=
            config.batch_size, shuffle=False, **kwargs)
        self.classes = trainset.classes
    
    def getloader(self):
        return self.classes, self.trainloader, self.testloader

def conv_bn(inp, oup, stride):
    return nn.Sequential(
        nn.Conv2d(inp, oup, 3, stride, 1, bias=False),
        nn.BatchNorm2d(oup),
        nn.ReLU6(inplace=True)
    )

def conv_1x1_bn(inp, oup):
    return nn.Sequential(
        nn.Conv2d(inp, oup, 1, 1, 0, bias=False),
        nn.BatchNorm2d(oup),
        nn.ReLU6(inplace=True)
    )

def make_divisible(x, divisible_by=8):
    return int(np.ceil(x * 1. / divisible_by) * divisible_by)

class InvertedResidual(nn.Module):
    def __init__(self, inp, oup, stride, expand_ratio):
        super(InvertedResidual, self).__init__()
        self.stride = stride
        assert stride in [1, 2]

        hidden_dim = int(inp * expand_ratio)
        self.use_res_connect = self.stride == 1 and inp == oup

        if expand_ratio == 1:
            self.conv = nn.Sequential(
                nn.Conv2d(hidden_dim, hidden_dim, 3, stride, 1, groups=hidden_dim, bias=False),
                nn.BatchNorm2d(hidden_dim),
                nn.ReLU6(inplace=True),
                nn.Conv2d(hidden_dim, oup, 1, 1, 0, bias=False),
                nn.BatchNorm2d(oup),
            )
        else:
            self.conv = nn.Sequential(
                nn.Conv2d(inp, hidden_dim, 1, 1, 0, bias=False),
                nn.BatchNorm2d(hidden_dim),
                nn.ReLU6(inplace=True),
                nn.Conv2d(hidden_dim, hidden_dim, 3, stride, 1, groups=hidden_dim, bias=False),
                nn.BatchNorm2d(hidden_dim),
                nn.ReLU6(inplace=True),
                nn.Conv2d(hidden_dim, oup, 1, 1, 0, bias=False),
                nn.BatchNorm2d(oup),
            )

    def forward(self, x):
        if self.use_res_connect:
            return x + self.conv(x)
        else:
            return self.conv(x)

class MobileNetV2(nn.Module):
    def __init__(self, n_class=1000, input_size=224, width_mult=1.):
        super(MobileNetV2, self).__init__()
        block = InvertedResidual
        input_channel = 32
        last_channel = 1280
        interverted_residual_setting = [
            [1, 16, 1, 1],
            [6, 24, 2, 2],
            [6, 32, 3, 2],
            [6, 64, 4, 2],
            [6, 96, 3, 1],
            [6, 160, 3, 2],
            [6, 320, 1, 1],
        ]

        assert input_size % 32 == 0
        self.last_channel = make_divisible(last_channel * width_mult) if width_mult > 1.0 else last_channel
        self.features = [conv_bn(3, input_channel, 2)]
        for t, c, n, s in interverted_residual_setting:
            output_channel = make_divisible(c * width_mult) if t > 1 else c
            for i in range(n):
                if i == 0:
                    self.features.append(block(input_channel, output_channel, s, expand_ratio=t))
                else:
                    self.features.append(block(input_channel, output_channel, 1, expand_ratio=t))
                input_channel = output_channel
        self.features.append(conv_1x1_bn(input_channel, self.last_channel))
        self.features = nn.Sequential(*self.features)

        self.classifier = nn.Linear(self.last_channel, n_class)

        self._initialize_weights()

    def forward(self, x):
        x = self.features(x)
        x = x.mean(3).mean(2)
        x = self.classifier(x)
        return x

    def _initialize_weights(self):
        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                n = m.kernel_size[0] * m.kernel_size[1] * m.out_channels
                m.weight.data.normal_(0, math.sqrt(2. / n))
                if m.bias is not None:
                    m.bias.data.zero_()
            elif isinstance(m, nn.BatchNorm2d):
                m.weight.data.fill_(1)
                m.bias.data.zero_()
            elif isinstance(m, nn.Linear):
                n = m.weight.size(1)
                m.weight.data.normal_(0, 0.01)
                m.bias.data.zero_()

def mobilenet_v2(pretrained=False):
    model = MobileNetV2(width_mult=1)
    return model

class DAIN(nn.Module):
    def __init__(self, nclass, backbone1, backbone2):
        super(DAIN, self).__init__()
        self.backbone1 = backbone1
        self.backbone2 = backbone2
        self.fc = nn.Linear(1280*2, nclass)

    def forward(self, img, diff_img):
        img_f = self.backbone1.features(img)
        img_f = img_f.mean(3).mean(2)

        diff_img_f = self.backbone2.features(diff_img)
        diff_img_f = diff_img_f.mean(3).mean(2)

        img_f = torch.flatten(img_f, 1)
        diff_img_f = torch.flatten(diff_img_f, 1)
        diff_img_f = diff_img_f + img_f
        out = torch.cat((img_f, diff_img_f), dim=1)
        out = self.fc(out)

        return out

def train_model(model, train_loader, criterion, optimizer, epoch, device):
    model.train()
    train_loss, correct, total = 0, 0, 0
    progress_bar = tqdm(train_loader, desc=f'Epoch {epoch} [Train]', leave=True)
    for batch_idx, (img, diff_img, target) in enumerate(progress_bar):
        img, diff_img, target = img.to(device), diff_img.to(device), target.to(device)
        optimizer.zero_grad()
        output = model(img, diff_img)
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
        for batch_idx, (img, diff_img, target) in enumerate(progress_bar):
            img, diff_img, target = img.to(device), diff_img.to(device), target.to(device)
            output = model(img, diff_img)
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
    config = VisualConfig()
    dataloader = Dataloader(config)
    classes, train_loader, test_loader = dataloader.getloader()
    print(f"Number of classes: {len(classes)}")
    print(f"Classes: {classes}")
    print(f"Training samples: {len(train_loader.dataset)}")
    print(f"Testing samples: {len(test_loader.dataset)}")
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")
    backbone1 = mobilenet_v2(pretrained=False)
    backbone2 = mobilenet_v2(pretrained=False)
    model = DAIN(len(classes), backbone1, backbone2)
    model = model.to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(model.parameters(), lr=config.lr, momentum=config.momentum,
                          weight_decay=config.weight_decay)
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
            torch.save(model.state_dict(), 'best_visual_model.pth')
            print(f'Best accuracy: {best_acc:.2f}%')
    plt.figure(figsize=(10, 5))
    plt.plot(range(1, config.nepochs + 1), train_accs, label='Train Accuracy')
    plt.plot(range(1, config.nepochs + 1), test_accs, label='Test Accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy (%)')
    plt.title('Visual-based Terrain Classification - Training and Testing Accuracy')
    plt.legend()
    plt.grid(True)
    plt.show()
    print(f'Best accuracy: {best_acc:.2f}%')
    return model

if __name__ == "__main__":
    main() 