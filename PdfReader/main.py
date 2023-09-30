import streamlit as st
from pypdf import PdfReader, PdfWriter
import requests
from io import BytesIO
import time
# from langdetect import detect

# Function to convert a PDF from a URL to text
def pdf_url_summary(pdf_url):
    try:
        # Download the PDF file from the URL
        response = requests.get(pdf_url)
        response.raise_for_status()

        # Create a PDF file object from the downloaded content
        pdf_file = BytesIO(response.content)

        start_time=time.time()
        # Create a PDF reader object
        pdf_reader = PdfReader(pdf_file)

        end_time = time.time()

        # Initialize variables for summarization
        num_pages = len(pdf_reader.pages)
        total_chars = 0
        special_chars = set()
        

        # Initialize a variable to store the extracted text
        text = ''

        start_time2=time.time()
        # Iterate through each page and extract the text
        for page_num in range(num_pages):
            page = pdf_reader.pages[page_num]
            page_text = page.extract_text()
            text += page_text
            
            # Update character count and collect special characters
            total_chars += len(page_text)
            special_chars.update(char for char in page_text if not char.isalnum())
        
        end_time2=time.time()

        computation_time = end_time-start_time

        computation_time2= end_time2-start_time2

        # Create a summary dictionary
        summary = {
            "Number of Pages": num_pages,
            "Total Characters": total_chars,
            "Special Characters": ", ".join(special_chars),
            "Computation time (s) for PyReader ":round(computation_time,4),
            "Computation time (s) for Extract Text":round(computation_time2,4),
        }

        return text, summary

    except Exception as e:
        return f"An error occurred: {e}"

# Streamlit app
def main():
    st.title("PDF to Text Converter")

    # Input field for the PDF URL
    pdf_url = st.text_input("Enter the URL of the PDF:")

    page_names = ['PyPDF','Nougat']
    page = st.radio('Select Library', page_names)

    if page =='PyPDF':
        st.subheader('Analysing PDF using: PyPDF')

        if st.button("Convert"):
            if pdf_url:
                # Call the conversion and summarization function
                text, summary = pdf_url_summary(pdf_url)

                if text:
                    st.subheader("Extracted Text:")
                    st.text(text)

                    st.subheader("Summary:")
                    st.write(summary)
                else:
                    st.error("Unable to extract text from the PDF.")
            else:
                st.warning("Please enter a valid PDF URL.")


    if page =='Nougat':
        st.subheader('Analysing PDF using: Nougat')
        endpoint = st.text_input('Enter the Endpoint', '')
        st.write('The current Endpoint is', endpoint)

        if st.button("Convert"):
            if pdf_url:
                # Call the conversion function and display the result
                text = pdf_url_summary(pdf_url)
                if text:
                    st.subheader("Extracted Text:")
                    st.text(text)
                else:
                    st.error("Unable to extract text from the PDF.")
            else:
                st.warning("Please enter a valid PDF URL.")

if __name__ == "__main__":
    main()
