from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
import streamlit as st

# Load environment variables
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

# Initialize the model
llm = ChatGroq(groq_api_key=api_key, model="Gemma-7b-It")

# Define the template and code_prompt
code_prompt = """
You are a Python code generator. Based on the given description, give me the code,please generate Python code:
Description: {text}
Python Code:
"""

# Create a PromptTemplate object
code_template = PromptTemplate(input_variables=['text'], template=code_prompt)

# Streamlit UI
st.title("Python Code Generator")
st.write("Describe the code you'd like to generate:")

# Text input from user
text_input = st.text_input("Enter the description of the code:", "")

# Button to generate code
if st.button("Generate Python Code"):
    if text_input.strip():
        # Generate the formatted prompt
        final_prompt = code_template.format(text=text_input)
        
        # Print the prompt (for debugging purposes)
        st.text(f"Prompt sent to model:\n{final_prompt}")

        # Assuming llm.invoke() gives you the response as an AIMessage object
        response = llm.invoke(final_prompt)

        # Access the 'content' attribute of the response which contains the generated text
        generated_code = response.content

        # Replace escaped newlines with real ones to properly format the code
        formatted_response = generated_code.replace('\\n', '\n')

        # Display the generated code
        st.code(formatted_response, language="python")
    else:
        st.warning("Please provide a description to generate the Python code.")