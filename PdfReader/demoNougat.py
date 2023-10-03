import streamlit as st
import requests

st.title("Streamlit App")
name = st.text_input("Enter your name:")

if st.button("Say Hi"):
    payload = {"name": name}
    response = requests.post("http://127.0.0.1:5000/hi", json=payload)
    if response.status_code == 200:
        st.write("Flask says:", response.text)
    else:
        st.write(f"Failed to communicate with Flask. Status Code: {response.status_code}")
        st.write("Response Content:", response.text)