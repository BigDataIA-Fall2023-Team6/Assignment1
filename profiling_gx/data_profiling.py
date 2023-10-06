import streamlit as st
import pandas as pd
from ydata_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report
import great_expectations as gx
import re
import os
import time

from great_expectations.data_context import FileDataContext
from great_expectations.dataset import PandasDataset

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
                    # if uploaded_file.type == "application/vnd.ms-excel":
                    #     df = pd.read_excel(uploaded_file, engine="openpyxl")
                    # else:
                    #     df = pd.read_csv(uploaded_file,delimiter='|')

                    columns = [
                        "CREDIT SCORE",
                        "FIRST PAYMENT DATE",
                        "FIRST TIME HOMEBUYER FLAG",
                        "MATURITY DATE",
                        "METROPOLITAN STATISTICAL AREA (MSA) OR METROPOLITAN DIVISION",
                        "MORTGAGE INSURANCE PERCENTAGE (MI %)",
                        "NUMBER OF UNITS",
                        "OCCUPANCY STATUS",
                        "ORIGINAL COMBINED LOAN-TO-VALUE (CLTV)",
                        "ORIGINAL DEBT-TO-INCOME (DTI) RATIO",
                        "ORIGINAL UPB",
                        "ORIGINAL LOAN-TO-VALUE (LTV)",
                        "ORIGINAL INTEREST RATE",
                        "CHANNEL",
                        "PREPAYMENT PENALTY MORTGAGE (PPM) FLAG",
                        "AMORTIZATION TYPE (FORMERLY PRODUCT TYPE)",
                        "PROPERTY STATE",
                        "PROPERTY TYPE",
                        "POSTAL CODE",
                        "LOAN SEQUENCE NUMBER",
                        "LOAN PURPOSE",
                        "ORIGINAL LOAN TERM",
                        "NUMBER OF BORROWERS",
                        "SELLER NAME",
                        "SERVICER NAME",
                        "SUPER CONFORMING FLAG",
                        "PRE-HARP LOAN SEQUENCE NUMBER",
                        "PROGRAM INDICATOR",
                        "HARP INDICATOR",
                        "PROPERTY VALUATION METHOD",
                        "INTEREST ONLY (I/O) INDICATOR",
                        "MORTGAGE INSURANCE CANCELLATION INDICATOR"
                    ]

                    df = pd.read_csv(uploaded_file, sep="|", header=None, names=columns)

                    # Display the selected data type
                    st.write(f"Data Type: {data_type}")
                    
                    # Generate a Pandas Profiling report
                    profile = ProfileReport(df, title="Profiling Report")
                    
                    # Display the Pandas Profiling report
                    st.write("Data Summary:")
                    st_profile_report(profile)

                    ##Great Expectations##


                    path_to_repo_dir = "D:\DAMG7245-BigData\Assignment1" # TODO: change this to your local path
                    path_to_data_dir = f"{path_to_repo_dir}\gx\data"
                    expectation_suite_name = "Orig_Expecation_Suite"+str(time.time())

                    #Initialize the GX Dir
                    context = FileDataContext.create(project_root_dir=path_to_repo_dir)

                    # os.mkdir(path_to_data_dir)
                    if not os.path.exists(path_to_data_dir):
                        os.mkdir(path_to_data_dir)
                    else:
                        # List all files in the directory
                        files = os.listdir(path_to_data_dir)
                    

                    # Iterate through the files and remove CSV files
                        for file in files:
                            if file.endswith(".csv"):
                                file_path = os.path.join(path_to_data_dir, file)
                                os.remove(file_path)

                    expectation_suite_name="Origination_Data_File_Suite"+str(time.time())
                    #Store the data in CSV format in the 'data' folder

                    df.to_csv(f"{path_to_data_dir}\{expectation_suite_name}.csv", index=False)


                    
                    datasource_name = "my_orig_datasource"+str(time.time())
                    datasource = context.sources.add_pandas_filesystem(
                        name=datasource_name, base_directory=path_to_data_dir
                    )

                    asset_name = "my_orig_asset"
                    # batching_regex = r"origcopy\.csv"

                    asset = datasource.add_csv_asset(name=asset_name) #, batching_regex=batching_regex

                    batch_request = asset.build_batch_request()

                    data_asset = context.get_datasource(datasource_name).get_asset(asset_name)
                    batch_request = data_asset.build_batch_request()

                    context.list_expectation_suite_names()

                    context.add_or_update_expectation_suite(expectation_suite_name)

                    validator = context.get_validator(batch_request=batch_request, expectation_suite_name=expectation_suite_name)

                    for columnx in columns:
                        validator.expect_column_values_to_not_be_null(column=columnx)

                    validator.expect_column_values_to_match_regex(column="CREDIT SCORE", regex=r'^\\d{1,4}$')
                    validator.expect_column_values_to_match_regex(column="FIRST PAYMENT DATE", regex=r'^\d{6}$')
                    validator.expect_column_values_to_match_regex(column="FIRST TIME HOMEBUYER FLAG", regex=r'^[A-Za-z]$')
                    validator.expect_column_values_to_match_regex(column="MATURITY DATE", regex=r'^\\d{6}$')
                    validator.expect_column_values_to_match_regex(column="METROPOLITAN STATISTICAL AREA (MSA) OR METROPOLITAN DIVISION", regex=r'^\\d{5}$')
                    validator.expect_column_values_to_match_regex(column="MORTGAGE INSURANCE PERCENTAGE (MI %)", regex=r'^\\d{1,3}$')
                    validator.expect_column_values_to_match_regex(column="NUMBER OF UNITS", regex=r'^\\d{1,2}$')
                    validator.expect_column_values_to_match_regex(column="OCCUPANCY STATUS", regex=r'^[A-Za-z]$')
                    validator.expect_column_values_to_match_regex(column="ORIGINAL COMBINED LOAN-TO-VALUE (CLTV)", regex=r'^\\d{1,3}$')
                    validator.expect_column_values_to_match_regex(column="ORIGINAL DEBT-TO-INCOME (DTI) RATIO", regex=r'^\\d{3}$')
                    validator.expect_column_values_to_match_regex(column="ORIGINAL UPB", regex=r'^\\d{1,12}$')
                    validator.expect_column_values_to_match_regex(column="ORIGINAL LOAN-TO-VALUE (LTV)", regex=r'^\\d{1,3}$')
                    validator.expect_column_values_to_match_regex(column="ORIGINAL INTEREST RATE", regex=r'^\d{6}\.\d{3}$')						
                    validator.expect_column_values_to_match_regex(column="CHANNEL", regex=r'^[A-Za-z]$')
                    validator.expect_column_values_to_match_regex(column="PREPAYMENT PENALTY MORTGAGE (PPM) FLAG", regex=r'^[A-Za-z]$')
                    validator.expect_column_values_to_match_regex(column="AMORTIZATION TYPE (FORMERLY PRODUCT TYPE)", regex=r'^[A-Za-z]{5}$')
                    validator.expect_column_values_to_match_regex(column="PROPERTY STATE", regex=r'^[A-Za-z]{2}$')
                    validator.expect_column_values_to_match_regex(column="PROPERTY TYPE", regex=r'^[A-Za-z]{2}$')
                    validator.expect_column_values_to_match_regex(column="POSTAL CODE", regex=r'^\d{5}$')
                    validator.expect_column_values_to_match_regex(column="LOAN SEQUENCE NUMBER", regex=r'^[A-Za-z]\d{2}Q\d{1}n\d{7}$')
                    validator.expect_column_values_to_match_regex(column="LOAN PURPOSE", regex=r'^[A-Za-z]$')
                    validator.expect_column_values_to_match_regex(column="ORIGINAL LOAN TERM", regex=r'^\\d{3}$')
                    validator.expect_column_values_to_match_regex(column="NUMBER OF BORROWERS", regex=r'^\\d{2}$')
                    validator.expect_column_values_to_match_regex(column="SELLER NAME", regex=r'^[A-Za-z0-9]{1,60}$')
                    validator.expect_column_values_to_match_regex(column="SERVICER NAME", regex=r'^[A-Za-z0-9]{1,60}$')
                    validator.expect_column_values_to_match_regex(column="SUPER CONFORMING FLAG", regex=r'^[A-Za-z]$')
                    validator.expect_column_values_to_match_regex(column="PRE-HARP LOAN SEQUENCE NUMBER", regex=r'^[A-Za-z]{1}[A-Za-z]{3}\\d{7}$')
                    validator.expect_column_values_to_match_regex(column="PROGRAM INDICATOR", regex=r'^[A-Za-z0-9]{1}$')
                    validator.expect_column_values_to_match_regex(column="HARP INDICATOR", regex=r'^[A-Za-z]{1}$')
                    validator.expect_column_values_to_match_regex(column="PROPERTY VALUATION METHOD", regex=r'^\\d{1}$')
                    validator.expect_column_values_to_match_regex(column="INTEREST ONLY (I/O) INDICATOR", regex=r'^[A-Za-z]{1}$')
                    validator.expect_column_values_to_match_regex(column="MORTGAGE INSURANCE CANCELLATION INDICATOR", regex=r'^[A-Za-z]{1}$')

                    validator.save_expectation_suite(discard_failed_expectations=False)

                    checkpoint = context.add_or_update_checkpoint(
                        name="Origination",
                        validator=validator
                    )

                    checkpoint_result = checkpoint.run(run_name="Manual_run Orgination Data")

                    context.build_data_docs()                    

                except Exception as e:
                    st.error(f"An error occurred: {e}")
            elif data_type == "Monthly Performance Data":
                # Process Monthly Performance Data here
                try:
                    # if uploaded_file.type == "application/vnd.ms-excel":
                    #     df = pd.read_excel(uploaded_file, engine="openpyxl")
                    # else:
                    #     df = pd.read_csv(uploaded_file,delimiter='|')

                    columns2 = [
                        "LOAN SEQUENCE NUMBER",
                        "MONTHLY REPORTING PERIOD",
                        "CURRENT ACTUAL UPB",
                        "CURRENT LOAN DELINQUENCY STATUS",
                        "LOAN AGE",
                        "REMAINING MONTHS TO LEGAL MATURITY",
                        "DEFECT SETTLEMENT DATE",
                        "MODIFICATION FLAG",
                        "ZERO BALANCE CODE",
                        "ZERO BALANCE EFFECTIVE DATE",
                        "CURRENT INTEREST RATE",
                        "CURRENT DEFERRED UPB",
                        "DUE DATE OF LAST PAID INSTALLMENT (DDLPI)",
                        "MI RECOVERIES",
                        "NET SALES PROCEEDS",
                        "NON MI RECOVERIES",
                        "EXPENSES",
                        "LEGAL COSTS",
                        "MAINTENANCE AND PRESERVATION COSTS",
                        "TAXES AND INSURANCE",
                        "MISCELLANEOUS EXPENSES",
                        "ACTUAL LOSS CALCULATION",
                        "MODIFICATION COST",
                        "STEP MODIFICATION FLAG",
                        "DEFERRED PAYMENT PLAN",
                        "ESTIMATED LOAN-TO-VALUE (ELTV)",
                        "ZERO BALANCE REMOVAL UPB",
                        "DELINQUENT ACCRUED INTEREST",
                        "DELINQUENCY DUE TO DISASTER",
                        "BORROWER ASSISTANCE STATUS CODE",
                        "CURRENT MONTH MODIFICATION COST",
                        "INTEREST BEARING UPB"
                    ]

                    df = pd.read_csv(uploaded_file, sep="|", header=None, names=columns2)

                    # Display the selected data type
                    st.write(f"Data Type: {data_type}")
                    
                    # Generate a Pandas Profiling report
                    profile = ProfileReport(df, title="Profiling Report")
                    
                    # Display the Pandas Profiling report
                    st.write("Data Summary:")
                    st_profile_report(profile)



                    ##### Great Expectations:

                    path_to_repo_dir = "D:\DAMG7245-BigData\Assignment1" # TODO: change this to your local path
                    path_to_data_dir = f"{path_to_repo_dir}\gx\data"
                    expectation_suite_name = "Monthly_Data_File_Suite"+str(time.time())

                    #Initialize the GX Dir
                    context = FileDataContext.create(project_root_dir=path_to_repo_dir)

                    # os.mkdir(path_to_data_dir)
                    if not os.path.exists(path_to_data_dir):
                        os.mkdir(path_to_data_dir)
                    else:
                        # List all files in the directory
                        files = os.listdir(path_to_data_dir)
                    

                    # Iterate through the files and remove CSV files
                        for file in files:
                            if file.endswith(".csv"):
                                file_path = os.path.join(path_to_data_dir, file)
                                os.remove(file_path)

                    expectation_suite_name="Monthly_Data_File_Suite"+str(time.time())
                    #Store the data in CSV format in the 'data' folder

                    df.to_csv(f"{path_to_data_dir}\{expectation_suite_name}.csv", index=False)


                    
                    datasource_name = "my_monthly_datasource"+str(time.time())
                    datasource = context.sources.add_pandas_filesystem(
                        name=datasource_name, base_directory=path_to_data_dir
                    )

                    asset_name = "Monthly_Data"
                    # batching_regex = r"origcopy\.csv"

                    asset = datasource.add_csv_asset(name=asset_name) #, batching_regex=batching_regex

                    batch_request = asset.build_batch_request()

                    data_asset = context.get_datasource(datasource_name).get_asset(asset_name)
                    batch_request = data_asset.build_batch_request()

                    context.list_expectation_suite_names()

                    context.add_or_update_expectation_suite(expectation_suite_name)

                    validator = context.get_validator(batch_request=batch_request, expectation_suite_name=expectation_suite_name)

                    for columnx in columns2:
                        validator.expect_column_values_to_not_be_null(column=columnx)

                    validator.expect_column_values_to_match_regex(column="LOAN SEQUENCE NUMBER", regex=r'^[A-Za-z0-9]{12}$')
                    validator.expect_column_values_to_match_regex(column="MONTHLY REPORTING PERIOD", regex=r'^\d{6}$')
                    validator.expect_column_values_to_match_regex(column="CURRENT ACTUAL UPB", regex=r'^\d{1,12}(\.\d{1,2})?$')
                    validator.expect_column_values_to_match_regex(column="CURRENT LOAN DELINQUENCY STATUS", regex=r'^[A-Za-z0-9]{1,3}$')
                    validator.expect_column_values_to_match_regex(column="LOAN AGE", regex=r'^\d{1,3}$')
                    validator.expect_column_values_to_match_regex(column="REMAINING MONTHS TO LEGAL MATURITY", regex=r'^\d{1,3}$')
                    validator.expect_column_values_to_match_regex(column="DEFECT SETTLEMENT DATE", regex=r'^\d{6}$')
                    validator.expect_column_values_to_match_regex(column="MODIFICATION FLAG", regex=r'^[A-Za-z]{1}$')
                    validator.expect_column_values_to_match_regex(column="ZERO BALANCE CODE", regex=r'^\d{1,2}$')
                    validator.expect_column_values_to_match_regex(column="ZERO BALANCE EFFECTIVE DATE", regex=r'^\d{6}$')

                    validator.save_expectation_suite(discard_failed_expectations=False)

                    checkpoint = context.add_or_update_checkpoint(
                        name="Origination",
                        validator=validator
                    )

                    checkpoint_result = checkpoint.run(run_name="Manual Run for Monthly Data")

                    context.build_data_docs()   

                except Exception as e:
                    st.error(f"An error occurred: {e}")
        else:
            st.error(f"Selected Data Type does not match the uploaded file type ({selected_data_type}).")

    else:
        st.warning("Please upload a file before generating the data summary.")
