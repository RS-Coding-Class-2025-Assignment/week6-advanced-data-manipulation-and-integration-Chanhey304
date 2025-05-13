#%%
import tkinter as tk
from tkinter import filedialog
import threading
from tkinter import ttk
import rasterio
import numpy as np
import matplotlib.pyplot as plt

def browse_file():
    global image_path
    image_path = filedialog.askopenfilename(title="Select a Hyperspectral Image", filetypes=[("TIF Files", "*.tif")])
    progress['value'] = 0
    progress_label.config(text="File Selected")

def plot_rgb():
    def task():
        r_band = int(r_entry.get())
        g_band = int(g_entry.get())
        b_band = int(b_entry.get())

        with rasterio.open(image_path) as dataset:
            data = dataset.read()
        red = data[r_band-1, :, :]
        blue= data[b_band-1, :, :]
        green= data[g_band-1, :, :]

        rgb = np.dstack((red, green, blue))
        rgb_norm = rgb/np.max(rgb)

        plt. imshow(rgb_norm)
        plt.title(f'RGB Composite (Bands {r_band}, {g_band}, {b_band})')
        plt.axis('off')
        plt.show()

        progress["value"] = 100
        progress_label.config(text="Display Complete!")
    
    threading.Thread(target=task).start()

root = tk.Tk()
root.title("Hyperspectral RGB Viewer")
root.geometry("500x350")

browse_button = tk.Button(root, text="Browse Hyperspectral Image", command=browse_file)
browse_button.pack(pady=10)

r_entry = tk.Entry(root)
r_entry.pack(pady=5)
r_entry.insert(0,"200")

g_entry = tk.Entry(root)
g_entry.pack(pady=5)
g_entry.insert(0,"155")

b_entry = tk.Entry(root)
b_entry.pack(pady=5)
b_entry.insert(0,"150")

plot_button = tk.Button(root, text="Plot RGB Composite", command=plot_rgb)
plot_button.pack(pady=10)

progress = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
progress.pack(pady=0)

progress_label = tk.Label(root, text="Progress")
progress_label.pack()

root.mainloop()

# %%
