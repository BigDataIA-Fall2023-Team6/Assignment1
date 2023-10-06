import streamlit as st
import pandas as pd
from ydata_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report
import great_expectations as gx
import re
import os

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

                    #variables
                    path_to_repo_dir="D:\DAMG7245-BigData\Assignments\Assignment1"
                    path_to_data_dir=f"{path_to_repo_dir}/gx/data"
                    
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

                    expectation_suite_name="Origination_Data_File_Suite"

                    #Store the data in CSV format in the 'data' folder

                    df.to_csv(f"{path_to_data_dir}/Origination.csv", index=False)


                    #Initialize the GX Dir
                    context = FileDataContext.create(project_root_dir=path_to_repo_dir)

                    # Give your Datasource a name
                    datasource_name = "Local_FileSystem_Source"
                    datasource = context.sources.add_pandas_filesystem(name=datasource_name, base_directory=path_to_data_dir)

                    # Give your first Asset a name
                    asset_name = "Origination_Data"
                    path_to_data = None
                    # to use sample data uncomment next line
                    # path_to_data = "https://raw.githubusercontent.com/great-expectations/gx_tutorials/main/data/yellow_tripdata_sample_2019-01.csv"
                    asset = datasource.add_csv_asset(name=asset_name)

                    # Build batch request
                    batch_request = asset.build_batch_request()

                    data_asset = context.get_datasource(datasource_name).get_asset(asset_name)
                    batch_request=data_asset.build_batch_request()

                    context.list_expectation_suite_names()
                    context.add_or_update_expectation_suite(expectation_suite_name)

                    # validator = context.sources.pandas_default.read_csv(
                    #     f"{path_to_data_dir}/orig.csv"
                    # )

                    
                    validator = context.get_validator(batch_request=batch_request, expectation_suite_name=expectation_suite_name)
                    
                    for columnx in columns:
                        validator.expect_column_values_to_not_be_null(column=columnx)

                    validator.expect_column_values_to_match_regex(column="CREDIT SCORE", regex=r'^\\d{4}$')
                    validator.expect_column_values_to_match_regex(column="FIRST PAYMENT DATE", regex=r'^\d{6}$')
                    validator.expect_column_values_to_match_regex(column="FIRST TIME HOMEBUYER FLAG", regex=r'^[A-Za-z]$')
                    validator.expect_column_values_to_match_regex(column="MATURITY DATE", regex=r'^\\d{6}$')
                    validator.expect_column_values_to_match_regex(column="METROPOLITAN STATISTICAL AREA (MSA) OR METROPOLITAN DIVISION", regex=r'^\\d{5}$')
                    validator.expect_column_values_to_match_regex(column="MORTGAGE INSURANCE PERCENTAGE (MI %)", regex=r'^\\d{3}$')
                    validator.expect_column_values_to_match_regex(column="NUMBER OF UNITS", regex=r'^\\d{2}$')
                    validator.expect_column_values_to_match_regex(column="OCCUPANCY STATUS", regex=r'^[A-Za-z]$')

                    





                    # validator.expect_column_values_to_match_regex(column="MATURITY DATE", regex=r'^\d{6}$')
                    # validator.expect_column_values_to_be_in_set(column="METROPOLITAN STATISTICAL AREA (MSA) OR METROPOLITAN DIVISION", value_set=['99999', 'Space (5)'])
                    # validator.expect_column_values_to_be_between(column="MORTGAGE INSURANCE PERCENTAGE (MI %)", min_value=1, max_value=55)
                    # validator.expect_column_values_to_be_in_set(column="NUMBER OF UNITS", value_set=['1', '2', '3', '4', '99'])
                    # validator.expect_column_values_to_be_in_set(column="OCCUPANCY STATUS", value_set=['P', 'I', 'S', '9'])
                    # validator.expect_column_values_to_be_between(column="ORIGINAL COMBINED LOAN-TO-VALUE (CLTV)", min_value=6, max_value=200)
                    # validator.expect_column_values_to_be_in_set(column="ORIGINAL COMBINED LOAN-TO-VALUE (CLTV)", value_set=['999'])
                    # validator.expect_column_values_to_be_between(column="ORIGINAL DEBT-TO-INCOME (DTI) RATIO", min_value=0, max_value=65)
                    # validator.expect_column_values_to_be_in_set(column="ORIGINAL DEBT-TO-INCOME (DTI) RATIO", value_set=['999'])
                    # validator.expect_column_values_to_be_between(column="ORIGINAL UPB", min_value=0, max_value=None)

                    validator.save_expectation_suite()


                    checkpoint = context.add_or_update_checkpoint(
                        name="my_quickstart_checkpoint",
                        validator=validator,
                    )

                    checkpoint_result = checkpoint.run(run_name="ManualRun for Origination Data 2")

                    context.view_validation_result(checkpoint_result)

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

                    #variables
                    path_to_repo_dir="D:\DAMG7245-BigData\Assignments\Assignment1"
                    path_to_data_dir=f"{path_to_repo_dir}/gx/data"
                    
                    if not os.path.exists(path_to_data_dir):
                        os.mkdir(path_to_data_dir)
                    else:
                        # List all files in the directory
                        files = os.listdir(path_to_data_dir)

                        # Iterate through the files and remove CSV files
                        for file in files:
                            if file.endswith("Monthly.csv"):
                                file_path = os.path.join(path_to_data_dir, file)
                                os.remove(file_path)

                    expectation_suite_name="Monthly_Data_File_Suite"

                    df.to_csv(f"{path_to_data_dir}/Monthly.csv", index=False)

                    context = FileDataContext.create(project_root_dir=path_to_repo_dir)

                    # Give your Datasource a name
                    datasource_name = "Local_FileSystem_Source2"
                    datasource = context.sources.add_pandas_filesystem(name=datasource_name, base_directory=path_to_data_dir)

                    # Give your first Asset a name
                    asset_name = "Monthly_Data2"
                    path_to_data = None
                    # to use sample data uncomment next line
                    # path_to_data = "https://raw.githubusercontent.com/great-expectations/gx_tutorials/main/data/yellow_tripdata_sample_2019-01.csv"
                    asset = datasource.add_csv_asset(name=asset_name)

                    # Build batch request
                    batch_request = asset.build_batch_request()

                    data_asset = context.get_datasource(datasource_name).get_asset(asset_name)
                    batch_request=data_asset.build_batch_request()

                    context.list_expectation_suite_names()
                    context.add_or_update_expectation_suite(expectation_suite_name)

                    # validator = context.sources.pandas_default.read_csv(
                    #     f"{path_to_data_dir}/orig.csv"
                    # )

                    validator = context.get_validator(batch_request=batch_request, expectation_suite_name=expectation_suite_name)

                    for columny in columns2:
                        validator.expect_column_values_to_not_be_null(column=columny)

                    # # Validate "LOAN SEQUENCE NUMBER"
                    # validator.expect_column_values_to_match_regex(column="LOAN SEQUENCE NUMBER", regex=r'^[A-Z]{1}\d{6}$', mostly=0.95)
                    # validator.expect_column_values_to_be_in_set(column="LOAN SEQUENCE NUMBER", value_set=['F', 'A'])
                    # validator.expect_column_length_to_be_between(column="LOAN SEQUENCE NUMBER", min_value=12, max_value=12)

                    # # Validate "MONTHLY REPORTING PERIOD"
                    # validator.expect_column_values_to_match_regex(column="MONTHLY REPORTING PERIOD", regex=r'^\d{6}$', mostly=0.95)
                    # validator.expect_column_values_to_be_of_type(column="MONTHLY REPORTING PERIOD", type_="int")
                    # validator.expect_column_length_to_be_between(column="MONTHLY REPORTING PERIOD", min_value=6, max_value=6)

                    # # Validate "CURRENT ACTUAL UPB"
                    # validator.expect_column_values_to_be_of_type(column="CURRENT ACTUAL UPB", type_="float")
                    # validator.expect_column_values_to_be_between(column="CURRENT ACTUAL UPB", min_value=0)


                    validator.save_expectation_suite()


                    checkpoint = context.add_or_update_checkpoint(
                        name="my_quickstart_checkpoint_v2",
                        validator=validator,
                    )

                    checkpoint_result = checkpoint.run(run_name="Manual Run for Monthly Data")

                    context.view_validation_result(checkpoint_result)

                    context.build_data_docs()

                except Exception as e:
                    st.error(f"An error occurred: {e}")
        else:
            st.error(f"Selected Data Type does not match the uploaded file type ({selected_data_type}).")

    else:
        st.warning("Please upload a file before generating the data summary.")
