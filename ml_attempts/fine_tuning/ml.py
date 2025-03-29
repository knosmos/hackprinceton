import os
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from torchvision import models, transforms
from PIL import Image

# Custom dataset that loads input images and corresponding label text files.
class BinaryPairedTextLabelDataset(Dataset):
    def __init__(self, root_dir, input_prefix="img_", label_prefix="out_", input_transform=None):
        """
        Args:
            root_dir (str): Directory containing the images and text labels.
            input_prefix (str): Prefix for input image filenames.
            label_prefix (str): Prefix for label text filenames.
            input_transform (callable, optional): Transformations to apply to input images.
        """
        self.root_dir = root_dir
        self.input_prefix = input_prefix
        self.label_prefix = label_prefix
        self.input_transform = input_transform
        
        # List all input image files with the proper naming convention.
        self.input_files = sorted([
            f for f in os.listdir(root_dir)
            if f.startswith(self.input_prefix) and f.endswith(".png")
        ])
    
    def __len__(self):
        return len(self.input_files)
    
    def __getitem__(self, idx):
        # Determine the input image and corresponding label file.
        input_filename = self.input_files[idx]
        number_part = input_filename[len(self.input_prefix):-4]  # Remove prefix and ".png"
        label_filename = f"{self.label_prefix}{number_part}.txt"
        
        input_path = os.path.join(self.root_dir, input_filename)
        label_path = os.path.join(self.root_dir, label_filename)
        
        # Load the input image.
        input_image = Image.open(input_path).convert("RGB")
        if self.input_transform:
            input_image = self.input_transform(input_image)
        
        # Read the label from the text file.
        with open(label_path, 'r') as f:
            label_str = f.read().strip()
        
        # Convert the label to a float value.
        try:
            label_value = float(label_str)
        except ValueError:
            # If the text is not numeric, handle common cases.
            if label_str.lower() == "yes":
                label_value = 1.0
            elif label_str.lower() == "no":
                label_value = 0.0
            else:
                raise ValueError(f"Label in file {label_path} is not recognized: {label_str}")
        
        # Wrap the label in a tensor with shape [1].
        label = torch.tensor([label_value], dtype=torch.float32)
        
        return input_image, label

# Define image transformations (resize, convert to tensor, and normalize).
input_transforms = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],  # ImageNet mean
                         std=[0.229, 0.224, 0.225])   # ImageNet std
])

# Create the dataset and dataloader.
dataset = BinaryPairedTextLabelDataset(root_dir="fine_tuning/images", input_transform=input_transforms)
dataloader = DataLoader(dataset, batch_size=16, shuffle=True)

# Load the pre-trained ResNet-50 model.
model = models.resnet50(pretrained=True)
num_features = model.fc.in_features
# Replace the final fully connected layer with a new one for binary classification.
model.fc = nn.Linear(num_features, 1)

# Optionally freeze all layers except the final layer if the dataset is small.
for param in model.parameters():
    param.requires_grad = False
for param in model.fc.parameters():
    param.requires_grad = True

# Define the loss function and optimizer.
criterion = nn.BCEWithLogitsLoss()
optimizer = optim.Adam(model.fc.parameters(), lr=0.001)

# Set device and move the model.
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Training loop.
num_epochs = 10
for epoch in range(num_epochs):
    model.train()
    running_loss = 0.0
    for inputs, labels in dataloader:
        inputs = inputs.to(device)
        labels = labels.to(device)  # Expected shape: [batch_size, 1]
        
        optimizer.zero_grad()
        outputs = model(inputs)     # Output shape: [batch_size, 1]
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        
        running_loss += loss.item() * inputs.size(0)
    
    epoch_loss = running_loss / len(dataset)
    print(f"Epoch {epoch+1}/{num_epochs}, Loss: {epoch_loss:.4f}")

# Save the model state dictionary
torch.save(model.state_dict(), "fine_tuning/models/ft.pth")
