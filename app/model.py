import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
import io

CLASSES = ['cardboard', 'glass', 'metal', 'paper', 'plastic', 'trash']
MODEL_PATH = 'model/waste_model.pth'

_model = None

def _build_model():
    model = models.mobilenet_v3_small(weights=None)
    in_features = model.classifier[3].in_features
    model.classifier[3] = nn.Linear(in_features, len(CLASSES))
    return model

def load_model():
    global _model
    if _model is None:
        _model = _build_model()
        _model.load_state_dict(torch.load(MODEL_PATH, map_location='cpu'))
        _model.eval()
    return _model

def preprocess(image_bytes):
    transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406],
                             [0.229, 0.224, 0.225])
    ])
    image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
    return transform(image).unsqueeze(0)

def predict(image_bytes):
    model = load_model()
    tensor = preprocess(image_bytes)
    with torch.no_grad():
        outputs = model(tensor)
        probs = torch.softmax(outputs, dim=1)
        confidence, predicted_idx = probs.max(1)
    return CLASSES[predicted_idx.item()], confidence.item()