import os
from dotenv import load_dotenv
from langchain_community.llms import Ollama
import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

## Prompt template
prompt=ChatPromptTemplate(
        [
                ("system","You are a helpful assistant. Please response to the question asked"),
                ("user","Question: {Question}")
        ]
)

## Streamlit Framework
st.title("Langchain demo with Ollama model")
input_text= st.text_input("What question do you have")

##Ollama gamma2 model
llm=Ollama(model="gemma:2b")
output_parser=StrOutputParser()
chain =prompt|llm|output_parser

if input_text:
        st.write(chain.invoke({"Question":input_text}))