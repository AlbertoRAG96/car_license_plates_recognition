# Car Plates Detector

![License Plates](./assets/license-plates-banner.jpg)
_Photo by [Tom Grünbauer](https://unsplash.com/@tomgruenbauer?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText) on [Unsplash](https://unsplash.com/photos/WElrXyQnTiM?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)_

This repository contains a car plates detector using [YOLOv8](https://docs.ultralytics.com) and [PyTesseract](https://pypi.org/project/pytesseract/). It's a powerful and efficient tool for detecting and recognizing license plates in images. The repo includes a Flask application where you can upload an image and the detector will identify the license plate for you.

## Table of Contents

* [Features](#features)
* [Getting Started](#getting_started)
* [Installation](#installation)
* [Usage](#usage)
* [Example Notebook](#example_notebook)
* [Contributing](#contributing)
* [License](#license)

## Features<a name="features"></a>

* License plate detection using YOLOv8.
* License plate recognition using PyTesseract.
* Flask web application for easy user interaction.
* Example notebook to demonstrate YOLO model usage.

## Getting Started<a name="getting_started"></a>

To get started, clone this repository to your local machine:

```
git clone https://github.com/AlbertoRAG96/car_license_plates_recognition.git
cd car_license_plates_recognition
```

## Installation<a name="installation"></a>

To install all the necessary libraries and dependencies, run the following command:

```
pip install -r requirements.txt
```

## Usage<a name="usage"></a>

1. Start the Flask application:

```
python app.py
```

2. Open a web browser and navigate to:

```
http://127.0.0.1:5000/
```

3. Upload an image and let the detector identify the license plate for you.

## Example Notebook<a name="example_notebook"></a>

An example notebook is included in the `examples` folder to show you how to use the YOLOv8 model. You can find it [here](https://github.com/AlbertoRAG96/car_license_plates_recognition/tree/main/examples).

## Contributing<a name="contributing"></a>

If you want to contribute to this project, please submit a pull request with your changes, or create an issue to discuss your ideas.

## License<a name="license"></a>

This project is licensed under the [MIT License](https://opensource.org/license/mit/).
