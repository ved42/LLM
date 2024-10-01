from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

# Load environment variables
load_dotenv()

# Configure Google API Key
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

# Function to load the model and get a response
def get_gemini_response(image_data, input_text, prompt):
    try:
        # Using Google's Gemini model for invoice processing
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content([input_text, image_data[0], prompt])
        return response.text
    except Exception as e:
        return f"Error generating response: {str(e)}"

# Function to handle image setup for API input
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        # Read the image file into bytes
        bytes_data = uploaded_file.getvalue()
        # Prepare the image data for the API
        image_parts = [{
            "mime_type": uploaded_file.type,
            "data": bytes_data
        }]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Initialize Streamlit app
st.set_page_config(page_title="Gemini Image Demo")
st.header("Gemini Invoice Processing App")

# Text input for the prompt
input_text = st.text_input("Input Prompt: ", key="input")

# File uploader for the image (invoice)
uploaded_file = st.file_uploader("Choose an invoice image...", type=["jpg", "jpeg", "png"])

# Display the uploaded image
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Invoice Image", use_column_width=True)

# Submit button
submit = st.button("Process Invoice")

# Input prompt to instruct the model
input_prompt = """
You are an expert in understanding invoices. 
You will receive input images of invoices, which could be in any language.
Your task is to:
1. Extract all relevant invoice data.
2. Translate any non-English content into English, including names, addresses, item descriptions, dates, and other text.
3. Convert any non-English date formats (e.g., "2023年10月31日") into English date formats (e.g., "October 31, 2023").
4. Convert any currency symbols into English (e.g., "¥10,000" to "10,000 JPY").
5. Provide the final structured data in a well-formatted JSON format, ensuring all data is in English.
"""


# Handle the invoice processing when the button is clicked
if submit:
    try:
        # Prepare the image for API input
        image_data = input_image_setup(uploaded_file)
        
        # Get the model response
        response = get_gemini_response(image_data, input_text, input_prompt)
        
        # Display the response
        st.subheader("Response:")
        st.write(response)

    except FileNotFoundError as fnf_error:
        st.error(f"Error: {fnf_error}")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
