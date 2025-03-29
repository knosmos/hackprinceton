import cv2
import os

for img in os.listdir('.'):
    if img.endswith('.png'):
        # Read the image
        image = cv2.imread(img)

        # Resize the image to 512x512
        resized_image = cv2.resize(image, (240, 240), interpolation=cv2.INTER_NEAREST)

        # Save the resized image with a new name
        new_name = f"resized_{img}"
        cv2.imwrite(new_name, resized_image)