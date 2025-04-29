import tkinter as tk

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

root = tk.Tk()
root.title("Hand Gesture Recognizer")
root.geometry("1000x700")
root.configure(bg="#f6f9fc")

title = tk.Label(root, text="Hand Gesture Recognizer", font=("Segoe UI", 24, "bold"), bg="#f6f9fc")
title.pack(pady=(20, 0))

subtitle = tk.Label(root, text="Display hand gestures as text and hear them spoken aloud", font=("Segoe UI", 12), fg="#6b7280", bg="#f6f9fc")
subtitle.pack(pady=(5, 20))

main_frame = tk.Frame(root, bg="#f6f9fc")
main_frame.pack(fill="both", expand=True, padx=20, pady=10)

camera_frame = tk.Frame(main_frame, bg="#f6f9fc")
camera_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))

camera_box = tk.Frame(camera_frame, bg="#fee2e2", width=640, height=400, highlightbackground="#60a5fa", highlightcolor="#60a5fa", highlightthickness=2)
camera_box.pack(fill="both", expand=True)
camera_box.pack_propagate(False)

camera_text = tk.Label(camera_box, text="Camera access denied or not available", bg="#fee2e2", fg="#b91c1c", font=("Segoe UI", 12))
camera_text.pack(expand=True)

detection_label = tk.Label(camera_frame, text="● Detection Active", fg="#22c55e", bg="#f6f9fc",font=("Segoe UI", 10, "bold"))
detection_label.pack(pady=5)


gesture_frame = tk.Frame(main_frame, width=300, height=400, bg="white", bd=1, relief="solid")
gesture_frame.pack(side="left", fill="y", padx=(10, 0))
gesture_frame.pack_propagate(False)

gesture_title = tk.Label(gesture_frame, text="Recognized Gesture", font=("Segoe UI", 16, "bold"), bg="white")
gesture_title.pack(pady=(20, 10))

gesture_icon = tk.Label(gesture_frame, text="📷", font=("Segoe UI", 32), bg="white", fg="#cbd5e1")
gesture_icon.pack(pady=10)

gesture_text = tk.Label(gesture_frame, text="No gesture detected", font=("Segoe UI", 12), fg="#6b7280", bg="white")
gesture_text.pack()

gesture_subtext = tk.Label(gesture_frame, text="Show your hand to the camera", font=("Segoe UI", 10),fg="#9ca3af", bg="white")
gesture_subtext.pack(pady=(5, 0))

bottom_frame = tk.Frame(root, bg="#f6f9fc")
bottom_frame.pack(side="bottom", fill="x", pady=10, padx=20)

voice_toggle = RoundedToggle(bottom_frame, on_toggle=toggle_voice_feedback, bg="#f6f9fc")
voice_toggle.pack(side="left", padx=(0, 5))

voice_toggle_label = tk.Label(bottom_frame, text="Voice Feedback Disabled", font=("Segoe UI", 10), fg="#374151", bg="#f6f9fc")
voice_toggle_label.pack(side="left")

root.mainloop()