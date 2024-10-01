import streamlit as st
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
import os

# Load the environment variables
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

# Initialize the LLM
llm = ChatGroq(groq_api_key=api_key, model="Gemma-7b-It")

# Email prompt template with sender and receiver names
email_Prompt = '''
Write a professional and polite email reply from {sender_name} to {receiver_name} based on the following details:

Subject: {subject}

Email Message:
{message}

Please ensure the reply addresses the points mentioned in the email, and provide a clear, courteous, and formal tone. The email should conclude with an appropriate closing and sign-off.

Reply:
'''

# Create PromptTemplate
email_prompt_temp = PromptTemplate(
    input_variables=['sender_name', 'receiver_name', 'subject', 'message'], 
    template=email_Prompt
)

# Streamlit UI
st.title("Intelligent Email Reply Assistant")

# User inputs
sender_name = st.text_input("Sender's Name")
receiver_name = st.text_input("Receiver's Name")
subject = st.text_input("Email Subject")
message = st.text_area("Email Message")

# Button to generate the reply
if st.button("Generate Reply"):
    if sender_name and receiver_name and subject and message:
        # Fill the prompt
        filled_prompt = email_prompt_temp.format(
            sender_name=sender_name,
            receiver_name=receiver_name,
            subject=subject,
            message=message
        )
        
        # Generate response using the LLM
        response = llm.invoke(filled_prompt)
        # Access the 'content' attribute of the response which contains the generated text
        generated_code = response.content

        # Replace escaped newlines with real ones to properly format the code
        formatted_response = generated_code.replace('\\n', '\n')
        
        # Display the generated email reply
        st.subheader("Generated Email Reply:")
        st.write(formatted_response)
    else:
        st.error("Please fill out all fields.")