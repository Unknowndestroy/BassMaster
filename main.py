import tkinter as tk
from tkinter import ttk, StringVar, IntVar

class BassControlApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bass Controller")
        self.root.geometry("600x700")
        
        # Speaker List
        self.create_speaker_selection()
        
        # Volume Controls
        self.create_volume_controls()
        
        # Bass Controls
        self.create_bass_controls()
        
        # Stereo Controls
        self.create_stereo_controls()
        
    def create_speaker_selection(self):
        frame = ttk.LabelFrame(self.root, text="SELECT HEADPHONES")
        frame.grid(row=0, column=0, padx=10, pady=5, sticky="ew")
        
        self.select_all_var = IntVar()
        check = ttk.Checkbutton(frame, text="Select All", variable=self.select_all_var, 
                               command=self.toggle_speaker_list)
        check.grid(row=0, column=0, sticky="w")
        
        self.speaker_list = tk.Listbox(frame, height=4, selectmode=tk.MULTIPLE)
        speakers = ["Speaker 1", "Headphone 1", "Bluetooth Speaker", "USB Headset"]
        for spk in speakers:
            self.speaker_list.insert(tk.END, spk)
        self.speaker_list.grid(row=1, column=0, columnspan=2, sticky="ew", pady=5)
        
    def create_volume_controls(self):
        frame = ttk.LabelFrame(self.root, text="VOLUME")
        frame.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        
        self.volume_var = IntVar(value=74)
        self.create_slider(frame, "Volume", self.volume_var)
        
    def create_bass_controls(self):
        frame = ttk.LabelFrame(self.root, text="BASS BOOST")
        frame.grid(row=2, column=0, padx=10, pady=5, sticky="ew")
        
        self.bass_var = IntVar(value=74)
        self.create_slider(frame, "Bass Boost", self.bass_var)
        
    def create_stereo_controls(self):
        # Bass Stereo
        self.bass_stereo_var = IntVar(value=1)
        bass_frame = ttk.Frame(self.root)
        bass_frame.grid(row=3, column=0, sticky="w", padx=10)
        
        check = ttk.Checkbutton(bass_frame, text="Bass Boost Stereo", 
                              variable=self.bass_stereo_var, command=self.toggle_bass_stereo)
        check.grid(row=0, column=0, sticky="w")
        
        # Bass Channels
        self.bass_channels_frame = ttk.Frame(self.root)
        self.bass_channels_frame.grid(row=4, column=0, sticky="ew", padx=10)
        
        self.right_bass_var = IntVar(value=74)
        self.left_bass_var = IntVar(value=74)
        self.create_slider(self.bass_channels_frame, "RIGHT BASS BOOST", self.right_bass_var)
        self.create_slider(self.bass_channels_frame, "LEFT BASS BOOST", self.left_bass_var)
        self.toggle_bass_stereo()
        
        # Volume Stereo
        self.volume_stereo_var = IntVar(value=1)
        vol_frame = ttk.Frame(self.root)
        vol_frame.grid(row=5, column=0, sticky="w", padx=10)
        
        check = ttk.Checkbutton(vol_frame, text="Volume Stereo", 
                              variable=self.volume_stereo_var, command=self.toggle_volume_stereo)
        check.grid(row=0, column=0, sticky="w")
        
        # Volume Channels
        self.volume_channels_frame = ttk.Frame(self.root)
        self.volume_channels_frame.grid(row=6, column=0, sticky="ew", padx=10)
        
        self.right_vol_var = IntVar(value=74)
        self.left_vol_var = IntVar(value=74)
        self.create_slider(self.volume_channels_frame, "RIGHT VOLUME", self.right_vol_var)
        self.create_slider(self.volume_channels_frame, "LEFT VOLUME", self.left_vol_var)
        self.toggle_volume_stereo()
        
    def create_slider(self, parent, text, var):
        frame = ttk.Frame(parent)
        frame.pack(fill="x", pady=5)
        
        label = ttk.Label(frame, text=text, width=15)
        label.pack(side="left")
        
        scale = ttk.Scale(frame, from_=0, to=100, variable=var,
                         command=lambda v: var.set(round(float(v))))
        scale.pack(side="left", fill="x", expand=True, padx=5)
        
        entry = ttk.Entry(frame, width=5, textvariable=var)
        entry.pack(side="left")
        
    def toggle_speaker_list(self):
        if self.select_all_var.get():
            self.speaker_list.grid_remove()
        else:
            self.speaker_list.grid()
            
    def toggle_bass_stereo(self):
        if self.bass_stereo_var.get():
            self.bass_channels_frame.grid_remove()
        else:
            self.bass_channels_frame.grid()
            
    def toggle_volume_stereo(self):
        if self.volume_stereo_var.get():
            self.volume_channels_frame.grid_remove()
        else:
            self.volume_channels_frame.grid()

if __name__ == "__main__":
    root = tk.Tk()
    app = BassControlApp(root)
    root.mainloop()
