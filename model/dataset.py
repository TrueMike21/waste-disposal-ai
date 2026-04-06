import os
from torchvision import datasets, transforms
from torch.utils.data import DataLoader, random_split

# Recommended dataset: TrashNet (https://github.com/garythung/trashnet)
# 6 classes: cardboard, glass, metal, paper, plastic, trash
# Place unzipped data in: data/dataset-resized/

CLASSES = ['cardboard', 'glass', 'metal', 'paper', 'plastic', 'trash']

def get_transforms(train=True):
    if train:
        return transforms.Compose([
            transforms.RandomResizedCrop(224),
            transforms.RandomHorizontalFlip(),
            transforms.ColorJitter(brightness=0.2, contrast=0.2),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406],
                                 [0.229, 0.224, 0.225])
        ])
    return transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406],
                             [0.229, 0.224, 0.225])
    ])

def get_dataloaders(data_dir='data/dataset-resized', batch_size=32):
    full_dataset = datasets.ImageFolder(data_dir, transform=get_transforms(train=True))
    
    train_size = int(0.8 * len(full_dataset))
    val_size = len(full_dataset) - train_size
    train_ds, val_ds = random_split(full_dataset, [train_size, val_size])
    val_ds.dataset.transform = get_transforms(train=False)

    train_loader = DataLoader(train_ds, batch_size=batch_size, shuffle=True, num_workers=2)
    val_loader   = DataLoader(val_ds,   batch_size=batch_size, shuffle=False, num_workers=2)

    return train_loader, val_loader, CLASSES