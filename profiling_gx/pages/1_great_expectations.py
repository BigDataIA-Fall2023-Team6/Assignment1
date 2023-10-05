import streamlit as st
import pandas as pd
from ydata_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report
import great_expectations as gx
from great_expectations.data_context import FileDataContext
from great_expectations.dataset import PandasDataset

# Set the title and description of your app
st.title("CSV/XLS File Upload App")
st.write("Upload a CSV or XLS file and indicate if it is Origination/Monthly performance data.")

# Create a file upload widget
uploaded_file = st.file_uploader("Upload a CSV or XLS file", type=["txt"])

# Create a radio button for data type selection
data_type = st.radio("Select Data Type:", ("Origination Data", "Monthly Performance Data"))

# Create a button to trigger data summary
if st.button("Generate Data Summary"):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the uploaded file using Pandas
        try:

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

            #variables
            path_to_repo_dir="D:\DAMG7245-BigData\Assignments\Assignment1" # Change with individual paths

            path_to_data_dir=f"{path_to_repo_dir}/gx/data"
            expectation_suite_name="Origination_Data_File_Suite"

            context = FileDataContext.create(project_root_dir=path_to_repo_dir)

            df.to_csv(f"{path_to_data_dir}/orig.csv", index=False)

            # Give your Datasource a name
            datasource_name = "Local_FileSystem_Source2"
            datasource = context.sources.add_pandas_filesystem(name=datasource_name, base_directory=path_to_data_dir)

            # Give your first Asset a name
            asset_name = "Origination_Data2"
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

            validator.expect_column_values_to_be_between(column="Credit Score", min_value=300, max_value=9999)
            validator.expect_column_values_to_be_in_set(column="FIRST TIME HOMEBUYER FLAG", value_set=['Y', 'N'])
            validator.expect_column_values_to_be_between(column="MORTGAGE INSURANCE PERCENTAGE (MI %)", min_value=0, max_value=35)
            validator.expect_column_values_to_be_in_set(column="NUMBER OF UNITS", value_set=[1, 2, 3, 4])
            validator.expect_column_values_to_be_in_set(column="OCCUPANCY STATUS", value_set=['P', 'I', 'S', '9'])
            validator.expect_column_values_to_be_between(column="ORIGINAL COMBINED LOAN-TO-VALUE (CLTV)", min_value=1, max_value=200)

            validator.expect_column_values_to_be_between(column="CREDIT SCORE", min_value=300, max_value=850)
            validator.expect_column_values_to_be_of_type(column="CREDIT SCORE", type_="int")
            validator.expect_column_values_to_be_in_set(column="FIRST TIME HOMEBUYER FLAG", value_set=['Y', 'N', '9'])
            validator.expect_column_values_to_match_regex(column="FIRST PAYMENT DATE", regex=r'^\d{6}$')
            validator.expect_column_values_to_match_regex(column="MATURITY DATE", regex=r'^\d{6}$')
            validator.expect_column_values_to_be_in_set(column="METROPOLITAN STATISTICAL AREA (MSA) OR METROPOLITAN DIVISION", value_set=['99999', 'Space (5)'])
            validator.expect_column_values_to_be_between(column="MORTGAGE INSURANCE PERCENTAGE (MI %)", min_value=1, max_value=55)
            validator.expect_column_values_to_be_in_set(column="NUMBER OF UNITS", value_set=['1', '2', '3', '4', '99'])
            validator.expect_column_values_to_be_in_set(column="OCCUPANCY STATUS", value_set=['P', 'I', 'S', '9'])
            validator.expect_column_values_to_be_between(column="ORIGINAL COMBINED LOAN-TO-VALUE (CLTV)", min_value=6, max_value=200)
            validator.expect_column_values_to_be_in_set(column="ORIGINAL COMBINED LOAN-TO-VALUE (CLTV)", value_set=['999'])
            validator.expect_column_values_to_be_between(column="ORIGINAL DEBT-TO-INCOME (DTI) RATIO", min_value=0, max_value=65)
            validator.expect_column_values_to_be_in_set(column="ORIGINAL DEBT-TO-INCOME (DTI) RATIO", value_set=['999'])
            validator.expect_column_values_to_be_between(column="ORIGINAL UPB", min_value=0, max_value=None)



            validator.save_expectation_suite()


            checkpoint = context.add_or_update_checkpoint(
                name="my_quickstart_checkpoint_v1",
                validator=validator,
            )

            checkpoint_result = checkpoint.run(run_name="Manual Run")

            context.view_validation_result(checkpoint_result)

            context.build_data_docs()


            

        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please upload a file before generating the data summary.")


