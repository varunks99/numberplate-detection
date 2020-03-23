#4 extra libraries needed: OpenCV (cv2), imutils, pytesseract, and pillow (PIL). Please download them.

import tkinter as tk
import cv2
import imutils
import pytesseract
from tkinter import filedialog
from PIL import ImageTk, Image

#This is for OCR. You will have to download Tesseract on your device.
#Refer to this page on how to download: https://github.com/tesseract-ocr/tesseract/wiki
#Once you download tesseract, you will have to place the path of the exe file below
pytesseract.pytesseract.tesseract_cmd = 'E:/Program Files/Tesseract-OCR/tesseract.exe'

#Function to open image and display it in the GUI
def open_img():
    x = openfilename()
    img = Image.open(x)
    img = img.resize((300,300), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)
    panel = tk.Label(root, image=img)
    panel.image = img
    panel.grid(row=2)

#Function to open dialog box to open image
def openfilename():
    global filename
    filename = filedialog.askopenfilename(title="Select an image")
    return filename

def detect():
    img = cv2.imread(filename)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #A filter helps remove noise
    gray = cv2.bilateralFilter(gray, 17, 19, 19)
    edged = cv2.Canny(gray, 170, 200)
    contours, hierarchy = cv2.findContours(edged, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
    rect = []
    #Detecting the rectangular contours
    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, 0.02*cv2.arcLength(cnt, True), True)
        if len(approx) == 4:
            (x, y, w, h) = cv2.boundingRect(approx)
            if not (h>=0.95 and h<=1.05):
                rect.append(cnt)
    #Selecting the biggest rectangular contour which should be the numberplate
    maxCnt = max(rect,key=cv2.contourArea)
    (x, y, w, h) = cv2.boundingRect(maxCnt)
    #Cropping the image to extract only the numberplate 
    plate = img[y:y+h, x:x+w, :]
    plate = cv2.cvtColor(plate, cv2.COLOR_BGR2RGB)
    #Extracting the numberplate details in the form of a string
    txt.set("The license plate number is " + get_text(plate))
    plate = Image.fromarray(plate)
    plate = plate.resize((100, 50), Image.ANTIALIAS)
    plate = ImageTk.PhotoImage(plate)
    #Updating the label to image with numberplate marked
    panel1 = tk.Label(root, image=plate)
    panel1.image = plate
    panel1.grid(row=3)
    #Marking the numberplate in the image
    cv2.drawContours(img, maxCnt, -1, (0, 255, 0), 4)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    res = Image.fromarray(img)
    res = res.resize((300,300), Image.ANTIALIAS)
    res = ImageTk.PhotoImage(res)
    panel2 = tk.Label(root, image=res)
    panel2.image = res
    panel2.grid(row=2)

#Function for OCR to extract numberplate details
def get_text(image):
    config = ('-l eng --oem 1 --psm 3')
    text = pytesseract.image_to_string(image, config=config)
    return text

#Main code 
root = tk.Tk()
root.title("Numberplate detection")
root.geometry("400x400+30+30")
b1 = tk.Button(root, text="Open image", command=open_img).place(x = 265, y = 350)
b2 = tk.Button(root, text="Detect", command=detect).place(x = 350, y = 350)
txt = tk.StringVar()
panel3 = tk.Label(root, textvariable=txt)
panel3.grid(row=4)
root.mainloop()


