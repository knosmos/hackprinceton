import cv2
import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image

# Set up device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Reconstruct the ResNet-50 model architecture.
model = models.resnet50(pretrained=False)
num_features = model.fc.in_features
model.fc = nn.Linear(num_features, 1)

# Load the saved state dictionary from the specified path.
model.load_state_dict(torch.load("fine_tuning/models/ft.pth", map_location=device))
model.to(device)
model.eval()

def inference(frame):
    """
    Processes an OpenCV frame, performs inference using the fine-tuned ResNet-50,
    and returns the probability for the positive class.
    
    Args:
        frame (numpy.ndarray): A frame from OpenCV (BGR format).
    
    Returns:
        float: The probability of the positive class.
    """
    # Convert frame from BGR to RGB.
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Define the transformation matching the training preprocessing.
    transform = transforms.Compose([
        transforms.ToPILImage(),         # Convert numpy array to PIL Image.
        transforms.Resize((224, 224)),     # Resize to 224x224.
        transforms.ToTensor(),             # Convert PIL Image to tensor.
        transforms.Normalize(mean=[0.485, 0.456, 0.406],  # Normalize using ImageNet statistics.
                             std=[0.229, 0.224, 0.225])
    ])
    
    # Apply the transformation and add the batch dimension.
    input_tensor = transform(rgb_frame).unsqueeze(0).to(device)
    
    # Perform inference.
    with torch.no_grad():
        output = model(input_tensor)  # Output is a logit with shape [1, 1].
        probability = torch.sigmoid(output)  # Convert logit to probability.
    
    return probability.item()
