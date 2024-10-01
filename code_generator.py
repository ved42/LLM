import streamlit as st
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
import os

# Load environment variables
load_dotenv()

# Initialize API key for Groq
api_key = os.getenv("GROQ_API_KEY")

# Initialize the model
llm = ChatGroq(api_key=api_key, model="Gemma-7b-It")

# Define the prompt template
temp = """ 
You are a helpful assistant, generating the code in the mentioned language.
Code: {code}
Language: {language}
"""
pro = PromptTemplate(input_variables=['code', 'language'], template=temp)

# Streamlit UI components
st.title("Code Generator")

# User inputs for code generation
code_prompt = st.text_input("Enter the code prompt")
language_choice = st.text_input("Enter the programming language")

# Button to generate code
if st.button("Generate Code"):
    # Format the prompt
    response = pro.format(code=code_prompt, language=language_choice)

    # Get the response from the model
    with st.spinner("Generating code..."):
        final_output = llm.invoke(response)
        code_output = final_output.content

    # Display the generated code
    st.subheader(f"Generated Code in {language_choice}:")
    st.code(code_output, language=language_choice.lower())