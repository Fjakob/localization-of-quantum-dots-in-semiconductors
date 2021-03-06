import tkinter as tk
import os
import glob
import random as rnd
import numpy as np
from varname import nameof

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import ttk


class App(tk.Tk):
    def __init__(self):
        # Instanciate
        super().__init__()
        self.title('Spectrum Labelling App')

        # Specify Output file
        self.file_path = os.getcwd() + '\\LabeledSpectra.txt'
        self.file_name = ""

        # Change to Data Directory
        self.data_dir = os.getcwd() + '\\..\\Spectra Analysis\\sample'
        os.chdir(self.data_dir)

        # Create App
        self.createWidgets()
        self.open_file()


    def createWidgets(self):

        self.rowconfigure(0, minsize=400, weight=1)
        self.columnconfigure(1, minsize=400, weight=1)
        padding = {'padx': 5, 'pady': 5}

        # 1) Create Figure Frame
        self.FrameFig = tk.Frame(master=self)

        # create FigureCanvasTkAgg object
        self.figure = Figure(figsize=(6, 4), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, self.FrameFig)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        NavigationToolbar2Tk(self.canvas, self.FrameFig)

        self.FrameFig.grid(row=0, column=0)

        # 2) Create Labeling Frame
        self.FrameLabel = tk.Frame(master=self)

        # Add user entry
        userFrame = tk.Frame(master=self.FrameLabel)
        self.user_entry = tk.Entry(master=userFrame)
        self.user_entry.insert(0, "User name")
        self.user_entry.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Create Radio Buttons
        radioBtnFrame = tk.Frame(master=self.FrameLabel)
        peak = tk.StringVar(name="peak", value="1")
        noise = tk.StringVar(name="noise", value="1")
        whatever = tk.StringVar(name="whatever", value="1")
        categories = [peak, noise, whatever]
        labels = ["1", "2", "3", "4", "5"]
        for idx, category in enumerate(categories):
            tk.Label(radioBtnFrame, text=category).grid(row=idx,column=0, **padding)
            for jdx, label in enumerate(labels):
                ttk.Radiobutton(radioBtnFrame, text=label, variable=category, value=int(label)).grid(row=idx,column=jdx+1, **padding)
        self.labels = categories

        # Create Buttons
        btnFrame = tk.Frame(master=self.FrameLabel)
        submit_btn = tk.Button(master=btnFrame, text="Submit", command=self.submit)
        submit_btn.pack(side=tk.RIGHT, **padding)

        reject_btn = tk.Button(master=btnFrame, text="Next", command=self.open_file)
        reject_btn.pack(side=tk.RIGHT, **padding)

        userFrame.grid(row=0, column=0)
        radioBtnFrame.grid(row=1, column=0)
        btnFrame.grid(row=2, column=0)

        self.FrameLabel.grid(row=0, column=1)


    def open_file(self):
        """Open a file for labeling."""
        files = glob.glob(self.data_dir + '/*.' + 'DAT')
        n = len(files)
        k = rnd.randint(0, n-1)
        print("Selecting file {0} out of {1}".format(k,n))
        random_file = files[k]
        with open(random_file) as f:
            # remove file ending and extract infos from file name for spatial coordinates
            self.file_name = "".join(os.path.basename(random_file).split('.')[:-1])
            # read wavelengths
            lines = f.readlines()
            w_raw = [line.split()[0] for line in lines]
            w = np.asarray(w_raw).astype(float)
            # read spectrum
            spectrum_raw = [line.split()[1] for line in lines]
            spectrum = np.asarray(spectrum_raw).astype(float)
        self.plot_spectrum(w, spectrum)


    def plot_spectrum(self, wavelengths, amplitudes):
        """Update figure and canvas."""
        self.figure.clear()
        axes = self.figure.add_subplot()
        axes.plot(wavelengths, amplitudes)
        axes.set_title('Spectrum')
        axes.set_ylabel('Intensity')
        axes.set_xlabel('Wavelength')
        self.canvas.draw()


    def submit(self):
        """Save labeled text."""
        with open(self.file_path, mode="a", encoding="utf-8") as output_file:
            user = self.user_entry.get()
            output_file.write(self.file_name)
            output_file.write(" label ")
            for label in self.labels:
                output_file.write(label.get() + " ")
                label.set("1")
            output_file.write(" user " + user + "\n")
        self.open_file()


if __name__ == '__main__':
    app = App()
    app.mainloop()