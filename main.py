import tkinter as tk
from tkinter import ttk
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL

class BassMaster:
    def __init__(self, root):
        self.root = root
        self.root.title("BassMaster v1.2")
        self.root.geometry("400x650")
        
        # Audio setup
        self.setup_audio()
        
        # GUI Components
        self.create_device_selection()
        self.create_global_controls()
        self.create_bass_controls()
        self.create_stereo_controls()
        
    def setup_audio(self):
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.volume = interface.QueryInterface(IAudioEndpointVolume)
        
    def create_device_selection(self):
        frame = ttk.LabelFrame(self.root, text="Active Device")
        frame.pack(padx=10, pady=5, fill='x')
        
        self.devices = ttk.Combobox(frame, values=self.get_devices())
        self.devices.pack(padx=5, pady=2, fill='x')
        self.devices.set("Primary Sound Driver")
        
    def get_devices(self):
        return [d.FriendlyName for d in AudioUtilities.GetAllDevices() if d.State == 1]
    
    def create_global_controls(self):
        frame = ttk.LabelFrame(self.root, text="Master Controls")
        frame.pack(padx=10, pady=5, fill='x')
        
        # Volume
        ttk.Label(frame, text="Volume").pack(anchor='w')
        self.vol_var = tk.IntVar(value=74)
        self.create_slider_entry(frame, self.vol_var, 0, 100, self.set_volume)
        
        # Bass
        ttk.Label(frame, text="Bass Enhancer (dB)").pack(anchor='w')
        self.bass_var = tk.IntVar(value=36)
        self.create_slider_entry(frame, self.bass_var, -60, 60, self.set_bass)
        
    def create_bass_controls(self):
        self.bass_frame = ttk.LabelFrame(self.root, text="Bass Channels")
        self.bass_frame.pack(padx=10, pady=5, fill='x')
        
        # Stereo Checkbox
        self.bass_stereo = tk.BooleanVar(value=True)
        ttk.Checkbutton(self.bass_frame, text="Stereo Bass", 
                        variable=self.bass_stereo, command=self.toggle_bass).pack(anchor='w')
        
        # Channel Controls
        self.bass_controls = ttk.Frame(self.bass_frame)
        self.bass_controls.pack(fill='x')
        
        self.left_bass = tk.IntVar(value=36)
        self.right_bass = tk.IntVar(value=36)
        self.create_channel_control(self.bass_controls, "Left", self.left_bass)
        self.create_channel_control(self.bass_controls, "Right", self.right_bass)
        
    def create_stereo_controls(self):
        self.stereo_frame = ttk.LabelFrame(self.root, text="Stereo Channels")
        self.stereo_frame.pack(padx=10, pady=5, fill='x')
        
        # Stereo Checkbox
        self.vol_stereo = tk.BooleanVar(value=True)
        ttk.Checkbutton(self.stereo_frame, text="Stereo Volume", 
                       variable=self.vol_stereo, command=self.toggle_volume).pack(anchor='w')
        
        # Channel Controls
        self.vol_controls = ttk.Frame(self.stereo_frame)
        self.vol_controls.pack(fill='x')
        
        self.left_vol = tk.IntVar(value=74)
        self.right_vol = tk.IntVar(value=74)
        self.create_channel_control(self.vol_controls, "Left", self.left_vol)
        self.create_channel_control(self.vol_controls, "Right", self.right_vol)
        
    def create_slider_entry(self, parent, var, from_, to, command):
        frame = ttk.Frame(parent)
        frame.pack(fill='x')
        
        scale = ttk.Scale(frame, from_=from_, to=to, variable=var,
                         command=lambda v: var.set(round(float(v))))
        scale.pack(side='left', fill='x', expand=True, padx=2)
        
        entry = ttk.Entry(frame, width=5, textvariable=var)
        entry.pack(side='right', padx=2)
        var.trace_add('write', lambda *_: command())
        
    def create_channel_control(self, parent, text, var):
        frame = ttk.Frame(parent)
        frame.pack(fill='x', pady=2)
        
        ttk.Label(frame, text=text, width=6).pack(side='left')
        self.create_slider_entry(frame, var, -60, 60, self.update_channels)
        
    def toggle_bass(self):
        if self.bass_stereo.get():
            self.bass_controls.pack_forget()
            self.set_bass()
        else:
            self.bass_controls.pack(fill='x')
            self.update_channels()
            
    def toggle_volume(self):
        if self.vol_stereo.get():
            self.vol_controls.pack_forget()
            self.set_volume()
        else:
            self.vol_controls.pack(fill='x')
            self.update_channels()
    
    def set_volume(self):
        if self.vol_stereo.get():
            vol = self.vol_var.get()/100
            self.volume.SetMasterVolumeLevelScalar(vol, None)
            
    def set_bass(self):
        if self.bass_stereo.get():
            print(f"Setting global bass to {self.bass_var.get()}dB")  # API call here
            
    def update_channels(self):
        if not self.vol_stereo.get():
            print(f"L: {self.left_vol.get()}% | R: {self.right_vol.get()}%")
            
        if not self.bass_stereo.get():
            print(f"Bass L: {self.left_bass.get()}dB | R: {self.right_bass.get()}dB")

if __name__ == "__main__":
    root = tk.Tk()
    app = BassMaster(root)
    root.mainloop()
