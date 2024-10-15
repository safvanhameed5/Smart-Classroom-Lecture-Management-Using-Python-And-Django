# Smart Classroom Face Recognition Django Application

This project is a Django-based web application that provides a convenient and secure way to access lecture materials using facial recognition instead of traditional username and password authentication. Users are automatically redirected to a management interface for their lecture materials upon successful login.

## Features

- User registration and login using face recognition.
- Automatic redirection to a dashboard for managing lecture materials after login.
- Capture and store user facial data for training the recognition model.
- Add, view, and manage modules and notes associated with users.
- Dynamic web interface built with Django templates.
- Real-time face detection and recognition using OpenCV.

## Technologies Used

- **Django**: A high-level Python web framework for rapid development.
- **OpenCV**: A library for computer vision and image processing.
- **NumPy**: A library for numerical operations, particularly for handling arrays.
- **Pillow (PIL)**: A library for image manipulation.
- **SQLite**: Default database used by Django for data storage (can be changed to other databases).

## Machine Learning Component

This project utilizes machine learning for face recognition through the **LBPH (Local Binary Patterns Histograms)** algorithm. The key aspects include:

- **Feature Extraction**: The application captures and processes facial images during user registration to extract distinguishing features.
- **Model Training**: The captured images are used to train the LBPH face recognizer, allowing it to learn and store unique features of each user's face.
- **Prediction**: During login, the application compares the captured live image with the trained model to identify the user, providing a secure and efficient authentication method.

## Installation

### Prerequisites

Make sure you have the following installed:

- Python 3.x
- pip (Python package manager)

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/yourproject.git
   cd yourproject
