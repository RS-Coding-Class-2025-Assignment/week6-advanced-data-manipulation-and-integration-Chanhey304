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

def calculate_band_math():
    def task():
        band1_number = int(band1_entry.get())
        band2_number = int(band2_entry.get())

        with rasterio.open(image_path) as dataset:
            data=dataset.read()
        band1 = data[band1_number-1, :, :]
        band2 = data[band2_number-1, :, :]

        math_result = (band1 - band2)/(band1 + band2 +1e-6)
        
        plt.imshow(math_result, cmap='gray')
        plt.colorbar()
        plt.title(f"Band Math: (Band {band1_number} - Band {band2_number})/(Band {band1_number} + Band {band2_number})")
        plt.axis('off')
        plt.show()

        progress['value'] = 100
        progress_label.config(text="Calculation complete!")

    threading.Thread(target=task).start()
   


root = tk.Tk()
root.title("Hyperspectral Band math Calculator")
root.geometry("500x350")

browse_button = tk.Button(root, text="Browse Hyperspectral Image", command=browse_file)
browse_button.pack(pady=10)

band1_label = tk.Label(root, text="Enter Band 1 Number :")
band1_label.pack()
band1_entry = tk.Entry(root)
band1_entry.pack(pady=10)
band1_entry.insert(0, "217")


band2_label = tk.Label(root, text="Enter Band 1 Number :")
band2_label.pack()
band2_entry = tk.Entry(root)
band2_entry.pack(pady=10)
band2_entry.insert(0, "213")

calc_button = tk.Button(root, text="Calculate Band math", command=calculate_band_math)
calc_button.pack(pady=10)

progress=ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
progress.pack(pady=10)

progress_label = tk.Label(root, text="Progress")
progress_label.pack(pady=10)

root.mainloop()



# %%
