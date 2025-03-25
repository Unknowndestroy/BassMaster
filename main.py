import tkinter as tk
from tkinter import ttk
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
import math

class DeepTuneBassController:
    def __init__(self, root):
        self.root = root
        self.root.title("DeepTune Bass Controller")
        self.root.geometry("600x700")
        self.setup_audio_interface()
        self.create_widgets()
        self.setup_bindings()

    def setup_audio_interface(self):
        # Audio aygıtlarını ve ses arabirimlerini başlat
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.volume_interface = interface.QueryInterface(IAudioEndpointVolume)
        
        # Bass seviyesi için varsayılan aralık (-65.25 dB - 0.0 dB)
        self.min_db, self.max_db, _ = self.volume_interface.GetVolumeRange()

    def create_widgets(self):
        # Speaker seçim bölümü
        self.create_speaker_selection()
        
        # Ana kontrol panelleri
        self.create_volume_controls()
        self.create_bass_controls()
        self.create_stereo_controls()

    def create_speaker_selection(self):
        frame = ttk.LabelFrame(self.root, text="SELECT OUTPUT DEVICE")
        frame.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

        # Ses aygıtlarını listele
        self.device_list = ttk.Combobox(frame, values=self.get_audio_devices())
        self.device_list.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        self.device_list.set("Default Device")

    def get_audio_devices(self):
        # Sistemdeki ses çıkış aygıtlarını listele (Basitleştirilmiş)
        return ["Default Device", "Headphones", "Speakers", "Digital Output"]

    def create_volume_controls(self):
        frame = ttk.LabelFrame(self.root, text="MASTER VOLUME")
        frame.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        self.volume_var = tk.DoubleVar()
        self.volume_scale = ttk.Scale(frame, from_=0, to=100, 
                                    variable=self.volume_var,
                                    command=self.update_volume)
        self.volume_scale.pack(fill="x", padx=5, pady=5)
        
        self.volume_label = ttk.Label(frame, text="74%")
        self.volume_label.pack()

    def create_bass_controls(self):
        frame = ttk.LabelFrame(self.root, text="BASS ENHANCER")
        frame.grid(row=2, column=0, padx=10, pady=5, sticky="ew")

        self.bass_var = tk.DoubleVar()
        self.bass_scale = ttk.Scale(frame, from_=-24, to=24, 
                                   variable=self.bass_var,
                                   command=self.update_bass)
        self.bass_scale.set(0)
        self.bass_scale.pack(fill="x", padx=5, pady=5)
        
        self.bass_label = ttk.Label(frame, text="0 dB")
        self.bass_label.pack()

    def create_stereo_controls(self):
        frame = ttk.LabelFrame(self.root, text="STEREO BALANCE")
        frame.grid(row=3, column=0, padx=10, pady=5, sticky="ew")
        
        self.balance_var = tk.DoubleVar()
        self.balance_scale = ttk.Scale(frame, from_=-1, to=1,
                                      variable=self.balance_var,
                                      command=self.update_balance)
        self.balance_scale.set(0)
        self.balance_scale.pack(fill="x", padx=5, pady=5)
        
        self.balance_label = ttk.Label(frame, text="Center")
        self.balance_label.pack()

    def setup_bindings(self):
        self.volume_var.trace_add("write", self.update_volume_text)
        self.bass_var.trace_add("write", self.update_bass_text)
        self.balance_var.trace_add("write", self.update_balance_text)

    def update_volume(self, val):
        volume = float(val) / 100
        self.volume_interface.SetMasterVolumeLevelScalar(volume, None)

    def update_bass(self, val):
        # Bass boost için equalizer ayarı (Örnek implementasyon)
        db = float(val)
        normalized = db / 100
        bass_boost = math.exp(normalized * 2) - 1  # Logaritmik dönüşüm
        print(f"Bass boost applied: {bass_boost:.2f} dB")  # Gerçek implementasyon için API çağrısı

    def update_balance(self, val):
        balance = float(val)
        self.volume_interface.SetChannelVolumeLevelScalar(0, max(0, 1 - balance), None)  # Left
        self.volume_interface.SetChannelVolumeLevelScalar(1, max(0, 1 + balance), None)  # Right

    def update_volume_text(self, *args):
        self.volume_label.config(text=f"{self.volume_var.get():.0f}%")

    def update_bass_text(self, *args):
        self.bass_label.config(text=f"{self.bass_var.get():.0f} dB")

    def update_balance_text(self, *args):
        value = float(self.balance_var.get())
        if value < -0.8:
            text = "Full Left"
        elif value > 0.8:
            text = "Full Right"
        else:
            text = ["Left", "Mid-Left", "Center", "Mid-Right", "Right"][int((value+1)*2)]
        self.balance_label.config(text=text)

if __name__ == "__main__":
    root = tk.Tk()
    app = DeepTuneBassController(root)
    root.mainloop()
