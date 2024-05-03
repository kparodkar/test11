from flask import Flask, render_template, request
import cv2
import numpy as np
from PIL import Image, ImageTk
import base64

app = Flask(__name__)
'''
def process_image(image_data):
    # Convert the base64-encoded image data to a numpy array
    nparr = np.frombuffer(base64.b64decode(image_data.split(',')[1]), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
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
    
    # Convert processed image to PIL format
    binary_inverse_pil = Image.fromarray(binary_inverse)
    
    # Resize the processed image to match the dimensions of the selected image
    binary_inverse_pil = binary_inverse_pil.resize((width, height))
    
    # Convert the processed image to base64 for display
    buffered = BytesIO()
    binary_inverse_pil.save(buffered, format="JPEG")
    processed_image_data = base64.b64encode(buffered.getvalue()).decode('utf-8')
    
    return processed_image_data  '''

@app.route('/', methods=['GET', 'POST'])
def start_page():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('start_page.html', error='No file selected')
        
        file = request.files['file']
        
        if file.filename == '':
            return render_template('start_page.html', error='No file selected')
        
    else:
        return render_template('start_page.html')

@app.route('/page_one')
def page_one():
    # Add logic for Page One
    return render_template('page_one.html')

@app.route('/page_two')
def page_two():
    # Add logic for Page Two
    return render_template('page_two.html')

if __name__ == '__main__':
    app.run(debug=True)
