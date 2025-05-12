import torch
import cv2
import numpy as np

import tkinter as tk

from PIL import Image, ImageTk

from ultralytics.nn.tasks import DetectionModel

cap = cv2.VideoCapture(0)
from ultralytics import YOLO

labels = ['Facepalm', 'GoodBye', 'Please','RaisedHand','Shh'] 



torch.serialization.add_safe_globals([DetectionModel])
model = YOLO("best.pt")

model.eval() 

class RoundedToggle(tk.Frame):
    def __init__(self, master=None, on_toggle=None, **kwargs):
        super().__init__(master, **kwargs)
        self.is_on = False
        self.on_toggle = on_toggle

        self.canvas = tk.Canvas(self, width=60, height=30, bg=self["bg"], highlightthickness=0)
        self.canvas.pack()

        self.bg = self.canvas.create_oval(0, 0, 30, 30, fill="#e5e7eb", outline="")
        self.bg2 = self.canvas.create_oval(30, 0, 60, 30, fill="#e5e7eb", outline="")
        self.bg_rect = self.canvas.create_rectangle(15, 0, 45, 30, fill="#e5e7eb", outline="")

        self.knob = self.canvas.create_oval(3, 3, 27, 27, fill="white", outline="")

        self.canvas.bind("<Button-1>", self.toggle)

    def toggle(self, event=None):
        self.is_on = not self.is_on
        if self.is_on:
            self.canvas.itemconfig(self.bg, fill="#4ade80")
            self.canvas.itemconfig(self.bg2, fill="#4ade80")
            self.canvas.itemconfig(self.bg_rect, fill="#4ade80")
            self.canvas.coords(self.knob, 33, 3, 57, 27)
        else:
            self.canvas.itemconfig(self.bg, fill="#e5e7eb")
            self.canvas.itemconfig(self.bg2, fill="#e5e7eb")
            self.canvas.itemconfig(self.bg_rect, fill="#e5e7eb")
            self.canvas.coords(self.knob, 3, 3, 27, 27)

        if self.on_toggle:
            self.on_toggle(self.is_on)

def toggle_voice_feedback(state):
    if state:
        voice_toggle_label.config(text="Voice Feedback Enabled")
    else:
        voice_toggle_label.config(text="Voice Feedback Disabled")

def update_camera():
    ret, frame = cap.read()
    if ret:
        frame = cv2.flip(frame, 1)
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        
        img_resized = cv2.resize(img, (640, 640))  
        img_tensor = torch.from_numpy(img_resized).float().permute(2, 0, 1)  
        img_tensor /= 255.0  

        
        img_tensor = img_tensor.unsqueeze(0)

        
        with torch.no_grad():
            results = model(img_tensor)
            pred = results[0].boxes.data 


       
        pred = pred[pred[:, 4] > 0.5]  
        pred[:, :4] = pred[:, :4] * 640 

       
        for det in pred:
            xmin, ymin, xmax, ymax = det[:4].int().tolist() 
            class_id = int(det[5])  
            label = labels[class_id]

            
            cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
            cv2.putText(frame, label, (xmin, ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

           
            gesture_text.config(text=label)

        
        img = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        img = Image.fromarray(img)
        imgtk = ImageTk.PhotoImage(image=img)
        camera_label.imgtk = imgtk
        camera_label.configure(image=imgtk)

    camera_label.after(10, update_camera)

def capture_images(label):
    
    pass

def start_capture_thread():
    
    pass

root = tk.Tk()
root.title("Hand Gesture Recognizer")
root.geometry("1000x700")
root.configure(bg="#f6f9fc")

title = tk.Label(root, text="Hand Gesture Recognizer", font=("Segoe UI", 24, "bold"), bg="#f6f9fc")
title.pack(pady=(20, 0))

subtitle = tk.Label(root, text="Display hand gestures as text and hear them spoken aloud", font=("Segoe UI", 12),
                    fg="#6b7280", bg="#f6f9fc")
subtitle.pack(pady=(5, 20))

main_frame = tk.Frame(root, bg="#f6f9fc")
main_frame.pack(fill="both", expand=True, padx=20, pady=10)

camera_frame = tk.Frame(main_frame, bg="#f6f9fc")
camera_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))

camera_box = tk.Frame(camera_frame, bg="#fee2e2", width=640, height=400,
                      highlightbackground="#60a5fa", highlightcolor="#60a5fa", highlightthickness=2)
camera_box.pack(fill="both", expand=True)
camera_box.pack_propagate(False)

camera_label = tk.Label(camera_box, text="Camera initializing...", bg="#fee2e2", fg="#b91c1c",
                        font=("Segoe UI", 12))
camera_label.pack(expand=True)

gesture_frame = tk.Frame(main_frame, width=300, height=400, bg="white", bd=1, relief="solid")
gesture_frame.pack(side="left", fill="y", padx=(10, 0))
gesture_frame.pack_propagate(False)

gesture_title = tk.Label(gesture_frame, text="Recognized Gesture", font=("Segoe UI", 16, "bold"), bg="white")
gesture_title.pack(pady=(20, 10))

gesture_text = tk.Label(gesture_frame, text="No gesture detected", font=("Segoe UI", 12), fg="#6b7280", bg="white")
gesture_text.pack()

bottom_frame = tk.Frame(root, bg="#f6f9fc")
bottom_frame.pack(side="bottom", fill="x", pady=10, padx=20)

voice_toggle = RoundedToggle(bottom_frame, on_toggle=toggle_voice_feedback, bg="#f6f9fc")
voice_toggle.pack(side="left", padx=(0, 5))

voice_toggle_label = tk.Label(bottom_frame, text="Voice Feedback Disabled", font=("Segoe UI", 10),
                              fg="#374151", bg="#f6f9fc")
voice_toggle_label.pack(side="left", padx=5)

capture_button = tk.Button(bottom_frame, text="Start Image Capture", command=start_capture_thread,
bg="#60a5fa", fg="white", font=("Segoe UI", 10, "bold"))
capture_button.pack(side="right")

update_camera()

root.mainloop()
