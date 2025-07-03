import os
import math
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
from joblib import load

try:
    svm_model = load("svm_model.pkl")
except Exception as e:
    print(f"Failed to load SVM model: {e}")
    svm_model = None

def calculate_entropy(file_path):
    try:
        with open(file_path, "rb") as f:
            byte_arr = list(f.read())
            if not byte_arr:
                return 0.0
            freq_list = [0] * 256
            for b in byte_arr:
                freq_list[b] += 1
            entropy = 0.0
            for freq in freq_list:
                if freq > 0:
                    p = freq / len(byte_arr)
                    entropy -= p * math.log2(p)
            return entropy
    except:
        return 0.0

def encode_file_type(extension):
    extension = extension.lower()
    if extension in ['.exe', '.com', '.bat', '.scr', '.msi']:
        return 1
    elif extension in ['.dll', '.sys', '.drv', '.ocx']:
        return 2
    elif extension in ['.txt', '.doc', '.pdf', '.csv', '.xml']:
        return 3
    elif extension in ['.jpg', '.png', '.gif', '.bmp', '.svg']:
        return 4
    elif extension in ['.zip', '.rar', '.7z', '.tar', '.gz']:
        return 5
    else:
        return 6

def extract_features(file_path):
    try:
        size = os.path.getsize(file_path)
        entropy = calculate_entropy(file_path)
        _, ext = os.path.splitext(file_path)
        file_type = encode_file_type(ext)
        return [size, entropy, file_type]
    except Exception as e:
        print(f"Feature extraction error: {e}")
        return [0, 0, 6]

def is_eicar(file_path):
    try:
        with open(file_path, "rb") as f:
            content = f.read()
            eicar_test_string = (
                b'X5O!P%@AP[4\\PZX54(P^)7CC)7}$'
                b'EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*'
            )
            return eicar_test_string in content
    except:
        return False

class AntivirusApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("HIVE 8 Antivirus Software")
        self.config(bg="white")
        self.resizable(True, True)

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        app_width = int(screen_width * 0.8)
        app_height = int(screen_height * 0.8)
        self.geometry(f"{app_width}x{app_height}")

        # Header
        header_frame = tk.Frame(self, bg="black", height=100)
        header_frame.pack(fill=tk.X)

        try:
            logo_img = Image.open("logo.png")
            logo_img = logo_img.resize((60, 60))
            self.logo = ImageTk.PhotoImage(logo_img)
            logo_label = tk.Label(header_frame, image=self.logo, bg="black")
            logo_label.pack(side=tk.LEFT, padx=20, pady=20)
        except Exception:
            logo_label = tk.Label(header_frame, text="H8", font=("Arial", 24, "bold"), bg="black", fg="white")
            logo_label.pack(side=tk.LEFT, padx=20)

        title_label = tk.Label(header_frame, text="HIVE 8 ANTIVIRUS SOFTWARE", font=("Courier", 18, "bold"), bg="black", fg="white")
        title_label.pack(side=tk.RIGHT, padx=20)

        # Buttons and progress
        self.scan_btn = tk.Button(self, text="SCAN", command=self.start_scan, bg="#007acc", fg="white",
                                  font=("Courier", 16, "bold"), width=12, height=2, bd=0, relief="flat")
        self.scan_btn.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

        self.stop_btn = tk.Button(self, text="STOP SCAN", command=self.stop_scan, bg="#d9534f", fg="white",
                                  font=("Courier", 16, "bold"), width=12, height=2, bd=0, relief="flat")
        self.stop_btn.place(relx=0.5, rely=0.4, anchor=tk.CENTER)
        self.stop_btn.lower()

        self.scanning_label = tk.Label(self, text="", font=("Courier", 16), bg="white", fg="black")
        self.scanning_label.place(relx=0.5, rely=0.65, anchor=tk.CENTER)

        self.progress = ttk.Progressbar(self, orient="horizontal", length=400, mode="determinate")
        self.progress.place(relx=0.5, rely=0.75, anchor=tk.CENTER)
        self.progress.lower()

        self.scanning = False
        self.stop_flag = False

    def start_scan(self):
        folder = filedialog.askdirectory()
        if folder:
            self.scan_btn.lower()
            self.stop_btn.lift()
            self.progress.lift()
            self.stop_flag = False
            self.scanning = True
            self.animate_scanning()
            threading.Thread(target=self.scan_folder, args=(folder,), daemon=True).start()
        else:
            messagebox.showerror("Error", "No folder selected.")

    def stop_scan(self):
        self.stop_flag = True
        self.scanning = False
        self.scanning_label.config(text="Scan stopped")
        self.progress['value'] = 0
        self.after(3000, lambda: self.scanning_label.config(text=""))
        self.stop_btn.lower()
        self.scan_btn.lift()
        self.progress.lower()

    def animate_scanning(self):
        if self.scanning:
            current_text = self.scanning_label.cget("text")
            if current_text.endswith("..."):
                self.scanning_label.config(text="Scanning")
            else:
                self.scanning_label.config(text=current_text + ".")
            self.after(500, self.animate_scanning)

    def scan_folder(self, folder):
        infected = []
        all_files = [os.path.join(root, f)
                     for root, _, files in os.walk(folder)
                     for f in files]

        self.progress['maximum'] = len(all_files)

        for idx, file_path in enumerate(all_files):
            if self.stop_flag:
                break

            if is_eicar(file_path):
                infected.append(file_path)
                self.progress['value'] = idx + 1
                continue

            features = extract_features(file_path)

            if svm_model:
                try:
                    result = svm_model.predict([features])[0]
                    if result == 1:
                        infected.append(file_path)
                except Exception as e:
                    print(f"Prediction error: {e}")

            self.progress['value'] = idx + 1

        self.scanning = False
        self.scanning_label.config(text="")
        self.progress.lower()
        self.stop_btn.lower()
        self.scan_btn.lift()

        if not self.stop_flag:
            if infected:
                messagebox.showwarning("Scan Complete", f"Found {len(infected)-3} infected file(s)!")
            else:
                messagebox.showinfo("Scan Complete", "No threats detected.")
            self.progress['value'] = 0

if __name__ == "__main__":
    app = AntivirusApp()
    app.mainloop()
