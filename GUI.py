#Loads the model and runs the GUI app
from keras.models import load_model
from tkinter import *
import tkinter as tk
import win32gui
from PIL import ImageGrab,  ImageOps
import numpy as np
from matplotlib import pyplot as plt

model = load_model('final_model.h5')


def predict_digit(img):
    plt.imshow(img, interpolation='nearest')  # check the captured image
    plt.show()

    # resize image to 28x28 pixels
    img = img.resize((28, 28))
    # convert rgb to grayscale
    img = img.convert('L')
    img = ImageOps.invert(img)  # need to invert the image because i need a black background
    img = np.array(img)

    # reshaping to support our model input and normalizing
    img = img.reshape(1, 28, 28, 1)
    img = img / 255.0
    # checking the image on which model will predict
    plt.imshow(img[0], cmap='gray', interpolation='nearest')
    plt.show()

    # predicting the class
    res = model.predict([img])[0]
    return np.argmax(res), max(res)


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.x = self.y = 0

        window_width = 850
        window_height = 350

        # get the screen dimension
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # find the center point
        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)

        # set the position of the window to the center of the screen
        self.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

        # Creating elements
        self.canvas = tk.Canvas(self, width=300, height=300, bg="white", cursor="cross")
        self.label = tk.Label(self, text="Draw..", font=("Helvetica", 48))
        self.classify_btn = tk.Button(self, text="Recognise", command=self.classify_handwriting)
        self.button_clear = tk.Button(self, text="Clear", command=self.clear_all)

        # Grid structure
        self.canvas.grid(row=0, column=0, pady=2, sticky=W, )
        self.label.grid(row=0, column=1, pady=2, padx=2)
        self.classify_btn.grid(row=1, column=1, pady=2, padx=2)
        self.button_clear.grid(row=1, column=0, pady=2)

        # self.canvas.bind("<Motion>", self.start_pos)
        self.canvas.bind("<B1-Motion>", self.draw_lines)  # draws lines when we use mouse to click

    def clear_all(self):
        self.canvas.delete("all")

    def classify_handwriting(self):
        HWND = self.canvas.winfo_id()  # get the handle of the canvas
        rect = win32gui.GetWindowRect(HWND)  # get the coordinate of the canvas
        a, b, c, d = rect
        # rect=(a+50,b+60,c+50,d+30)  #difficult to tune. because the tkinter window opens at different place every time
        # i fix the position of window and do the final tuning
        rect = (a + 95, b + 80, c + 160, d + 140)

        im = ImageGrab.grab(rect)
        digit, acc = predict_digit(im)
        self.label.configure(text=str(digit) + ',Confidence:' + str(int(acc * 100)) + '%')

    def draw_lines(self, event):
        self.x = event.x
        self.y = event.y
        r = 6  # thickness of lines
        self.canvas.create_oval(self.x - r, self.y - r, self.x + r, self.y + r, fill='black')
        # self.canvas.create_line(self.x-r, self.y-r, self.x + r, self.y + r, fill='black',capstyle='round' )


app = App()

mainloop()
