import streamlit as st
import pandas as pd
from ydata_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report
import great_expectations as gx

# Set the title and description of your app
st.title("CSV/XLS File Upload App")
st.write("Upload a CSV or XLS file and indicate if it is Origination/Monthly performance data.")

# Create a file upload widget
uploaded_file = st.file_uploader("Upload a CSV or XLS file", type=["csv", "xls", "xlsx"])

# Create a radio button for data type selection
data_type = st.radio("Select Data Type:", ("Origination Data", "Monthly Performance Data"))

# Create a button to trigger data summary
if st.button("Generate Data Summary"):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the uploaded file using Pandas
        try:
            if uploaded_file.type == "application/vnd.ms-excel":
                df = pd.read_excel(uploaded_file, engine="openpyxl")
            else:
                df = pd.read_csv(uploaded_file)
            
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
        st.warning("Please upload a file before generating the data summary.")
