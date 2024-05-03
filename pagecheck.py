import tkinter as tk
from tkinter import ttk, filedialog
import cv2
import numpy as np
from PIL import Image, ImageTk

class SampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Multi-Page App")
        self.geometry("400x200")
        
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        for F in (StartPage, PageOne, PageTwo):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame("StartPage")
    
    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        label = ttk.Label(self, text="Start Page")
        label.pack(side="top", fill="x", pady=10)
        
        # Image selection functionality
        self.img_label = tk.Label(self)
        self.img_label.pack()
        
        select_button = ttk.Button(self, text="Select Image", command=self.upload_image)
        select_button.pack()
        
        # Next button to move to the next page
        next_button = ttk.Button(self, text="Next", command=lambda: controller.show_frame("PageOne"))
        next_button.pack()

    def upload_image(self):
        self.controller.img_filename = filedialog.askopenfilename(initialdir="/", title="Select an Image File",
                                                                   filetypes=(("JPEG files", ".jpg;.jpeg"),
                                                                              ("PNG files", "*.png")))
        img = cv2.imread(self.controller.img_filename)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB for displaying in Tkinter
        img = cv2.resize(img, (400, 300))  # Resize image to fit the window
        img = Image.fromarray(img)
        img = ImageTk.PhotoImage(image=img)
        self.img_label.config(image=img)
        self.img_label.image = img  # Keep a reference to avoid garbage collection

class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        # Label for Page One
        label = ttk.Label(self, text="Page One")
        label.grid(row=0, column=1, pady=10, sticky="e")
        
        # Process Image button
        self.process_button = ttk.Button(self, text="Process Image", command=self.process_image)
        self.process_button.grid(row=1, column=1, pady=10)
        
        # Button to go back to Start Page
        self.back_button = ttk.Button(self, text="Go back to Start Page", command=lambda: controller.show_frame("StartPage"))
        self.back_button.grid(row=2, column=1, pady=10)

        # Label to display the processed image
        self.processed_img_label = tk.Label(self)
        self.processed_img_label.grid(row=3, column=1, pady=10)

    def process_image(self):
        # Retrieve the image filename selected in the StartPage
        img_filename = self.controller.img_filename
        
        # Read the image
        img = cv2.imread(img_filename)
        
        # Get the dimensions of the selected image
        height, width, _ = img.shape
        
        # Convert to Grayscale
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Gaussian Blur
        img_blur = cv2.GaussianBlur(img_gray, (3, 3), 0)

        # Canny Edge Detection
        img_edge = cv2.Canny(img_gray, 100, 200)

        # Dilate Edges
        kernel_dilate = np.ones((1, 1), np.uint8)
        thick = cv2.dilate(img_edge, kernel_dilate, iterations=1)

        # Sharpening
        kernel_sharpen = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
        sharpened = cv2.filter2D(thick, -1, kernel_sharpen)

        # Thresholding
        threshold_value = 120
        _, binary_inverse = cv2.threshold(sharpened, threshold_value, 255, cv2.THRESH_BINARY_INV)
        
        # Store the processed image in the controller for access on PageTwo
        self.controller.processed_image = binary_inverse
        
        # Convert processed image to PIL format
        binary_inverse_pil = Image.fromarray(binary_inverse)
        
        # Resize the processed image to match the dimensions of the selected image
        binary_inverse_pil = binary_inverse_pil.resize((width, height))
        
        # Convert the processed image to PhotoImage
        binary_inverse_pil = ImageTk.PhotoImage(image=binary_inverse_pil)
        
        # Update the label with the processed image
        self.processed_img_label.config(image=binary_inverse_pil)
        self.processed_img_label.image = binary_inverse_pil  # Keep a reference to avoid garbage collection

class PageTwo(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        label = ttk.Label(self, text="Page Two")
        label.pack(side="top", fill="x", pady=10)
        
        # Display the processed image from PageOne
        self.processed_img_label = tk.Label(self)
        self.processed_img_label.pack()
    
    def show_processed_image(self):
        # Retrieve the processed image from the controller
        processed_image = self.controller.processed_image
        
        # Convert processed image to PIL format
        processed_img_pil = Image.fromarray(processed_image)
        processed_img_pil = processed_img_pil.resize((400, 100))  # Resize the image
        processed_img_pil = ImageTk.PhotoImage(image=processed_img_pil)
        
        # Update the label with the processed image
        self.processed_img_label.config(image=processed_img_pil)
        self.processed_img_label.image = processed_img_pil  # Keep a reference to avoid garbage collection

    def on_show(self):
        # When the page is shown, display the processed image
        self.show_processed_image()

if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
