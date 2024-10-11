import streamlit as st
import requests

# Streamlit UI for chatbot
st.title("Chatbot Interface")

# Input box for user question
user_input = st.text_input("Ask the chatbot:")

if st.button("Send"):
    # Send the query to the Django API endpoint
    response = requests.get('http://localhost:8000/api/chatbot/', params={'question': user_input})
    st.write("Chatbot: ", response.json()['answer'])
