import tkinter as tk
from tkinter import messagebox
import cv2
from PIL import Image, ImageTk
import os

SAVE_DIR = "posture_detection/images"
os.makedirs(SAVE_DIR, exist_ok=True)

class WebcamLabeler:
    def __init__(self, root):
        self.root = root
        self.video_capture = cv2.VideoCapture(0)

        self.canvas = tk.Label(root)
        self.canvas.pack()

        self.label_entry = tk.Entry(root)
        self.label_entry.pack(pady=5)

        self.capture_button = tk.Button(root, text="Capture & Save", command=self.capture_and_save)
        self.capture_button.pack(pady=5)

        self.update_frame()

    def update_frame(self):
        ret, frame = self.video_capture.read()

        if ret:
            self.current_frame = frame
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            self.canvas.imgtk = imgtk
            self.canvas.configure(image=imgtk)

        self.root.after(10, self.update_frame)

    def capture_and_save(self):
        # Get label
        label = self.label_entry.get().strip()
        
        if not (label == "0" or label == "1"):
            messagebox.showerror("Bad label")
            return
    
        # Create the id
        seen = set()
        for file in os.listdir(SAVE_DIR):
            # img_000.jpg
            seen.add(int(file[4:7]))
        
        id = 0
        while id in seen:
            id += 1
        
        id = str(id)
        while len(id) < 3:
            id = "0" + id

        # Save image
        img_name = f"img_{id}.png"
        img_path = os.path.join(SAVE_DIR, img_name)

        out_name = f"out_{id}.txt"
        out_path = os.path.join(SAVE_DIR, out_name)

        cv2.imwrite(img_path, self.current_frame)

        with open(out_path, "w") as file:
            file.write(label)

        # Done
        self.label_entry.delete(0, tk.END)

    def __del__(self):
        if self.video_capture.isOpened():
            self.video_capture.release()

root = tk.Tk()
app = WebcamLabeler(root)
root.mainloop()
