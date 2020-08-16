from PIL import Image, ImageTk
import pickle
import cv2
import numpy as np
import tkinter as tk
from threading import Thread, Event
from time import sleep

NN_PATH = r"E:/programming/Python/Current/week2project/analysis/"


class FaceRecognizer:
    def __init__(self):
        self.nn_age = pickle.load(open(NN_PATH + "nn_age.dat", "rb"))
        self.nn_ethnicity = pickle.load(open(NN_PATH + "nn_ethnicity.dat", "rb"))
        self.nn_gender = pickle.load(open(NN_PATH + "nn_gender.dat", "rb"))
        self.cv = cv2.VideoCapture(0)    # 0 for external camera
        self.root = tk.Tk()
        self.root.geometry("550x580")
        self.root.title("Face Recognizer v1.0.0")
        self.curr_image = None
        self.__construct_app()

    def __construct_app(self):
        image_frame = tk.Frame(self.root, width=512, height=512)
        image_frame.pack(side=tk.TOP, padx=10, pady=5)

        self.image_display = tk.Label(image_frame)
        self.image_display.pack()

        btn = tk.Button(master=self.root, text="Take Snapshot!", command=self.analysis, height=2)
        btn.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        self.predict = tk.StringVar()
        self.predict.set("Take snapshot to analyze")
        res = tk.Label(master=self.root, textvariable=self.predict, relief=tk.GROOVE)
        res.pack(fill=tk.X, padx=10, pady=5)

        self.is_running = Event()
        self.is_running.set()
        self.capturing_thread = Thread(target=self.video_loop, daemon=True)
        self.capturing_thread.start()
        self.root.mainloop()

    def video_loop(self):
        while self.is_running.is_set():
            ok, image = self.cv.read()
            if not ok:
                continue
            image = cv2.flip(image, 1)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(image)
            self.curr_image = image.copy()
            image = ImageTk.PhotoImage(image)

            self.image_display.configure(image=image)
            # Keep reference to prevent from being garbage-collected
            self.image_display.image = image

            sleep(0.1)

    def analysis(self):
        image = self.curr_image
        image = image.convert("L")
        image = image.thumbnail((64, 64), Image.ANTIALIAS)
        X = [image.getpixel((j, i)) for i in range(64) for j in range(64)]
        X = np.array(X)

        y_hat_gender = self.nn_gender.predict(X)
        y_hat_age = self.nn_age.predict(X)
        y_hat_ethnicity = self.nn_ethnicity.predict(X)

        self.predict.set(f"Gender: {y_hat_gender}\tAge: {y_hat_age}\tEthnicity: {y_hat_ethnicity}")


if __name__ == "__main__":
    vis = FaceRecognizer()