# ✍️ Signature Fraud Detection Using Machine Learning

## 📌 Project Overview

**Signature Fraud Detection** is a machine learning-based web application designed to identify whether a handwritten signature is **Genuine or Forged**. The system uses a **Convolutional Neural Network (CNN)** to analyze signature images and classify them based on patterns learned from genuine and forged signature samples.

The application provides a simple web interface where users can upload a signature image and receive an automated verification result.

## 🎯 Objective

The main objective of this project is to automate handwritten signature verification and reduce the manual effort involved in identifying forged signatures.

## 🚀 Features

* Upload handwritten signature images
* Image preprocessing before prediction
* CNN-based signature classification
* Detects **Genuine** and **Forged** signatures
* Displays the uploaded signature
* Flask-based backend
* Simple and user-friendly web interface
* Automated signature verification

## 🛠️ Technologies Used

* **Python**
* **TensorFlow / Keras**
* **Convolutional Neural Network (CNN)**
* **Flask**
* **HTML**
* **CSS**
* **JavaScript**
* **NumPy**
* **Pillow**

## 🔄 Project Workflow

```text
User Uploads Signature
        ↓
Flask Backend
        ↓
Image Preprocessing
        ↓
Grayscale Conversion
        ↓
Image Resizing & Normalization
        ↓
Trained CNN Model
        ↓
Prediction
        ↓
Genuine / Forged
        ↓
Result Displayed
```

## 📂 Project Structure

```text
Signature-Fraud-Detection/
│
├── app.py
├── signature_model.h5
├── templates/
│   ├── index.html
│   └── result.html
│
├── static/
│   ├── style.css
│   └── uploads/
│
└── README.md
```

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/your-username/Signature-Fraud-Detection.git
```

Go to the project directory:

```bash
cd Signature-Fraud-Detection
```

Install the required Python libraries:

```bash
pip install flask tensorflow numpy pillow
```

## ▶️ Running the Application

Run the Flask application:

```bash
python app.py
```

Open the following address in your browser:

```text
http://127.0.0.1:5000
```

Upload a signature image and click **Detect** to view the prediction.

## 🧠 Machine Learning Model

The project uses a **Convolutional Neural Network (CNN)** for image classification. Signature images are preprocessed before being passed to the model. The model learns visual characteristics and patterns from the training dataset and classifies the uploaded signature as either **Genuine** or **Forged**.

## 📊 Applications

This system can be useful for:

* Banking and cheque verification
* Financial institutions
* Legal document verification
* Insurance claim verification
* Identity authentication
* Document security

## ⚠️ Limitations

The prediction accuracy depends on the quality, size, and diversity of the training dataset. Blurred, noisy, or significantly different signature samples may affect the model's prediction.

## 🔮 Future Enhancements

* Train the model using a larger dataset
* Improve prediction accuracy
* Implement Siamese Networks for advanced signature verification
* Add user authentication
* Add database support
* Deploy the application to a cloud platform
* Develop a mobile application for real-time verification

## 👩‍💻 Author

**Tejaswini**

---

⭐ If you find this project useful, consider giving the repository a star!
