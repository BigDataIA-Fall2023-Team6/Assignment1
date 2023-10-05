import streamlit as st
import pandas as pd
from ydata_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report
import great_expectations as gx
import re

# Set the title and description of your app
st.title("CSV/XLS File Upload App")
st.write("Upload a CSV or XLS file and indicate if it is Origination/Monthly performance data.")

# Create a file upload widget
uploaded_file = st.file_uploader("Upload a CSV or XLS file", type=["csv", "xls", "xlsx","txt"])

# Create a radio button for data type selection
data_type = st.radio("Select Data Type:", ("Origination Data", "Monthly Performance Data"))

def get_data_type(filename):
    if re.search(r'orig', filename, re.IGNORECASE):
        return "Origination Data"
    elif re.search(r'svcg', filename, re.IGNORECASE):
        return "Monthly Performance Data"
    elif re.search(r'(historical_data|sample_orig)_\d{4}Q\d.txt', filename, re.IGNORECASE):
        return "Origination Data"
    elif re.search(r'(historical_data_time|sample_svcg|historical_data_excl_time)_\d{4}Q\d.txt', filename, re.IGNORECASE):
        return "Monthly Performance Data"
    else:
        return "Unknown"

# Create a button to trigger data summary
if st.button("Generate Data Summary"):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the uploaded file using Pandas

        filename = uploaded_file.name
        selected_data_type = get_data_type(filename)

        # Check if the selected data type matches the uploaded file
        if data_type == selected_data_type:
            st.success(f"Selected Data Type: {data_type}")
            
            # Read and display the uploaded file
            if data_type == "Origination Data":
                # Process Origination Data here
                try:
                    if uploaded_file.type == "application/vnd.ms-excel":
                        df = pd.read_excel(uploaded_file, engine="openpyxl")
                    else:
                        df = pd.read_csv(uploaded_file,delimiter='|')
                    
                    # Display the selected data type
                    st.write(f"Data Type: {data_type}")
                    
                    # Generate a Pandas Profiling report
                    profile = ProfileReport(df, title="Profiling Report")
                    
                    # Display the Pandas Profiling report
                    st.write("Data Summary:")
                    st_profile_report(profile)
                except Exception as e:
                    st.error(f"An error occurred: {e}")
            elif data_type == "Monthly Performance Data":
                # Process Monthly Performance Data here
                try:
                    if uploaded_file.type == "application/vnd.ms-excel":
                        df = pd.read_excel(uploaded_file, engine="openpyxl")
                    else:
                        df = pd.read_csv(uploaded_file,delimiter='|')
                    
                    # Display the selected data type
                    st.write(f"Data Type: {data_type}")
                    
                    # Generate a Pandas Profiling report
                    profile = ProfileReport(df, title="Profiling Report")
                    
                    # Display the Pandas Profiling report
                    st.write("Data Summary:")
                    st_profile_report(profile)
                except Exception as e:
                    st.error(f"An error occurred: {e}")
        else:
            st.error(f"Selected Data Type does not match the uploaded file type ({selected_data_type}).")

    else:
        st.warning("Please upload a file before generating the data summary.")
