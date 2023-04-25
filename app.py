import os
import re
import cv2
import pyheif
from PIL import Image
import numpy as np
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import pytesseract
from ultralytics import YOLO

app = Flask(__name__)

app.config["IMAGE_UPLOADS"] = "static/uploads/"
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG", "GIF", "WEBP"]

def allowed_image(filename):
    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False

@app.route("/", methods=["GET", "POST"])
def upload_image():
    if request.method == "POST":
        if request.files:
            image = request.files["image"]

            if image.filename == "":
                print("No filename")
                return redirect(request.url)

            if allowed_image(image.filename):
                image.save(os.path.join(app.config["IMAGE_UPLOADS"], image.filename))
                return redirect(url_for("process_image", filename=image.filename))
            else:
                print("That file extension is not allowed")
                return redirect(request.url)

    return render_template("upload_image.html")

def process_plate_numbers(plate_numbers):
    plate_numbers = re.sub('[^a-zA-Z0-9 \n\.]', '', plate_numbers)
    return plate_numbers

@app.route("/process_image/<filename>")
def process_image(filename):
    image_path = os.path.join(app.config["IMAGE_UPLOADS"], filename)

    # Apply the YOLOv8 model on the image
    yolo_model = YOLO("model/best.pt")
    results_list = yolo_model(source=image_path)
    print(f"RESULTS: {results_list}")

    # Load image using CV2
    img = cv2.imread(image_path)

    # Convert BGR to RGB
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    car_plates = {}
    # Iterate through the results list
    for i, results in enumerate(results_list):
        # Iterate through the data
        for result in results.boxes:
            # Extract bounding box coordinates
            x1, y1, x2, y2 = int(result.xyxy[0][0]), int(result.xyxy[0][1]), int(result.xyxy[0][2]), int(result.xyxy[0][3])

            # Crop the frame to the license plate region
            plate_region = img[y1-3:y2+3, x1-3:x2+3]
            plate_region_path = os.path.join(app.config["IMAGE_UPLOADS"], filename.split('.')[0] + f'_car_plate_{i}.png')
            plate_pil = Image.fromarray(plate_region)
            plate_pil.save(plate_region_path)

            # Extract license plate numbers using Tesseract
            plate_numbers = pytesseract.image_to_string(plate_region)
            plate_numbers = process_plate_numbers(plate_numbers)
            car_plates[f'car_plate_{i}'] = {'plate_region': plate_region_path.replace('static/',''), 
                                            'plate_numbers': plate_numbers}
            print(f"\nPlate numbers: {plate_numbers}\n")

            # Define box color and thickness
            color = (255, 0, 0)
            thickness = 2
            
            # Draw the bounding box on the image
            cv2.rectangle(img_rgb, (x1, y1), (x2, y2), color, thickness)

    # Save the new image 
    modified_image_path = os.path.join(app.config["IMAGE_UPLOADS"], filename.split('.')[0] + '_modified.png')
    image_pil = Image.fromarray(img_rgb)
    image_pil.save(modified_image_path)

    return render_template("display_image.html", 
                           filename=modified_image_path.replace('static/',''), 
                           car_plates=car_plates)

@app.route("/display/<filename>")
def display_image(filename):
    return send_from_directory(app.config["IMAGE_UPLOADS"], filename)

if __name__ == "__main__":
    app.run(debug=True)
