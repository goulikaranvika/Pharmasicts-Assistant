# Pharmabot - A Smart Prescription Assistant & Diagnostic Chatbot

## Overview
Pharmabot is an AI-powered application that reads handwritten prescriptions, extracts medication details using advanced OCR techniques powered by Google Generative AI, and provides a chatbot interface for medicine-related queries. It extracts critical patient information and medication orders—including names, dosages, frequencies, and durations—from prescription images, validates them against a database, and displays the results in a user-friendly format.

## Installation
Clone the repository:
git clone https://github.com/yourusername/pharmabot.git
cd pharmabot

## Install dependencies
pip install -r requirements.txt

## Running the project
streamlit run app.py

Open the provided URL (typically http://localhost:8501) in your browser to access Pharmabot.

## Dependencies
Streamlit: Interactive web application framework.
google-generativeai: Library for accessing Google Generative AI models (Gemini Pro Vision and Gemini Pro) used for OCR and chatbot functionality.
Pillow (PIL): For image processing.
python-dotenv: To load environment variables (e.g., GOOGLE_API_KEY).
re: (Built-in) For parsing extracted text using regular expressions.
(Optional) OpenCV: For advanced image preprocessing (if needed).How AI is Used
OCR (Optical Character Recognition):
The Gemini Pro Vision model extracts text from prescription images, focusing on critical details such as medication names, dosages, frequencies, durations, and patient/doctor information.
Chatbot Integration:
The Gemini Pro model powers an interactive chatbot that answers medicine-related questions, providing guidance and clarifications based on the extracted prescription data.
## Example Usage
Upload a Prescription Image:
Drag and drop a prescription image (JPEG/PNG) using the file uploader.
Extract and Process Text:
The app processes the image using advanced OCR, extracts text, and parses patient and medication details.
View Extracted Information:
Expand sections to view patient information and a table of medication details, including dosage, frequency, and duration.
Interact with the Chatbot:
Use the chatbot interface to ask questions about medicines and receive AI-generated responses.
## Future Enhancements
Advanced OCR Integration:
Add support for additional OCR models (e.g., Microsoft Azure OCR, TrOCR) to handle more challenging handwriting.
Enhanced Parsing Logic:
Improve text parsing to support a broader range of prescription formats.
Diagnostic Capabilities:
Expand the diagnostic assistant to analyze medical images and patient data for more accurate diagnoses.
Mobile Application:
Develop a mobile version using React Native.
Medication Reminders:
Integrate alerts and reminders for patients.
## Support
For questions, issues, or contributions, please open an issue on GitHub or contact the project maintainer.

## License
This project is licensed under the MIT License.

Simply save this content as `README.md` in your repository's root directory. Adjust the repository URL, dependency details, or any other sections to fit your project's specifics.
