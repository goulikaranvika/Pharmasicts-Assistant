import streamlit as st
import google.generativeai as genai
import os
from PIL import Image
import re
from dotenv import load_dotenv
import easyocr
import numpy as np
import pandas as pd  # Import pandas

load_dotenv()

# --- EasyOCR Setup ---
reader = easyocr.Reader(['en'])

# --- Google API Configuration ---
try:
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
except KeyError:
    st.error("GOOGLE_API_KEY environment variable not found in .env file. Please add it.")
    st.stop()

# --- Model Setup ---
def get_gemini_pro_model():
    return genai.GenerativeModel('gemini-2.0-flash')

# --- Image Processing and Text Extraction (EasyOCR) ---
def extract_text_from_image_easyocr(image):
    try:
        if image.mode != 'RGB':
            image = image.convert('RGB')
        img_array = np.array(image)
        results = reader.readtext(img_array, detail=1, paragraph=False,
                                  contrast_ths=0.05, adjust_contrast=0.7,
                                  decoder='beamsearch', beamWidth=10)
        extracted_text = " ".join([text for (_, text, _) in results])
        return extracted_text.strip()
    except Exception as e:
        st.error(f"Error during EasyOCR text extraction: {e}")
        return None

# --- Gemini Interaction ---
def get_structured_data_from_gemini(text, model):
    """Gets structured data from Gemini, handling potential errors."""
    prompt = f"""
    Analyze the following prescription text and extract the key information into a structured format.
    Prioritize extracting: Patient Name, Doctor's Name, Doctor's License Number, Date, Medication Name, Dosage, Frequency, and Duration.
    If any information is not found, indicate it as "<NA>".  Output in a consistent, table-like format, as shown below:

    Patient Information:
    - Patient's Full Name: [Patient Name]
    - Patient's Age: [Age]
    - Patient's Gender: [Gender]
    - Prescription Date: [Date]
    - Doctor's Full Name: [Doctor's Name]
    - Doctor's License Number: [License Number]

    Medications:
    - Medication Name: [Medication 1 Name]
      Dosage: [Dosage 1]
      Frequency: [Frequency 1]
      Duration: [Duration 1]
    - Medication Name: [Medication 2 Name]
      Dosage: [Dosage 2]
      Frequency: [Frequency 2]
      Duration: [Duration 2]
    ... (and so on for other medications)

    Prescription Text:
    {text}
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"Error getting structured data from Gemini: {e}")
        return "Error: Could not retrieve structured data."

def parse_gemini_output(gemini_output):
    """Parses Gemini's output into a dictionary for easy table creation."""
    data = {"Patient Information": {}, "Medications": []}
    lines = gemini_output.split("\n")

    section = None
    for line in lines:
        line = line.strip()
        if not line:
            continue

        if "Patient Information:" in line:
            section = "Patient Information"
            continue
        elif "Medications:" in line:
            section = "Medications"
            continue

        if section == "Patient Information":
            match = re.match(r"- (.*?): (.*)", line)
            if match:
                key, value = match.groups()
                data[section][key.strip()] = value.strip()

        elif section == "Medications":
            if line.startswith("- Medication Name:"):
                med_name = line.replace("- Medication Name:", "").strip()
                data["Medications"].append({"Medication Name": med_name})
            elif ":" in line and data["Medications"]: # Check if medications list is not empty
                key, value = line.split(":", 1)  # Split only on the first colon
                data["Medications"][-1][key.strip()] = value.strip()

    return data


def display_data_as_table(data):
    """Displays the parsed data in Streamlit tables."""
    if data:
        st.subheader("Patient Information")
        if data['Patient Information']:
          st.table(pd.DataFrame([data["Patient Information"]])) # Wrap in a list
        else:
           st.write("No Patient information Found")

        st.subheader("Medications")
        if data['Medications']:
          st.table(pd.DataFrame(data["Medications"]))
        else:
          st.write("No Medicine Information Found")

# --- Chatbot --- (Remains the same as before)
def get_chatbot_response(question, model):
    try:
        response = model.generate_content(question)
        return response.text
    except Exception as e:
        st.error(f"Error in chatbot response: {e}")
        return "Sorry, I couldn't process that question."

# --- Streamlit UI ---
st.set_page_config(page_title="Pharmabot", layout="wide")
st.title("Pharmabot")

with st.container():
    col1, col2 = st.columns([0.6, 0.4])  # Adjusted column widths

    with col1:
        st.subheader("Upload a Prescription Image")
        uploaded_file = st.file_uploader("Drag and drop file here", type=["jpg", "jpeg", "png"], label_visibility="collapsed")
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Prescription Image", use_column_width=True)

            extracted_text = extract_text_from_image_easyocr(image)

            if extracted_text:
                gemini_model = get_gemini_pro_model()
                structured_data = get_structured_data_from_gemini(extracted_text, gemini_model)

                # Parse and display the structured data
                parsed_data = parse_gemini_output(structured_data)
                display_data_as_table(parsed_data)


            else:
                st.warning("No text could be extracted from the image.")

    with col2:
        st.subheader("Ask Pharmabot a Question")
        user_question = st.text_input("Type your question here", key="user_input", label_visibility="collapsed")
        chatbot_model = get_gemini_pro_model()

        if user_question:
            response = get_chatbot_response(user_question, chatbot_model)
            st.write(f"**You:** {user_question}")
            st.write(f"**Pharmabot:** {response}")