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

# Create a button to trigger data summary
if st.button("Generate Data Summary"):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the uploaded file using Pandas
        try:

            columns = [
                "Credit Score",
                "First Payment Date",
                "First Time Homebuyer Flag",
                "Maturity Date",
                "Metropolitan Statistical Area (MSA) Or Metropolitan Division",
                "Mortgage Insurance Percentage (MI %)",
                "Number of Units",
                "Occupancy Status",
                "Original Combined Loan-to-Value (CLTV)",
                "Original Debt-to-Income (DTI) Ratio",
                "Original UPB",
                "Original Loan-to-Value (LTV)",
                "Original Interest Rate",
                "Channel",
                "Prepayment Penalty Mortgage (PPM) Flag",
                "Amortization Type (Formerly Product Type)",
                "Property State",
                "Property Type",
                "Postal Code",
                "Loan Sequence Number",
                "Loan Purpose",
                "Original Loan Term",
                "Number of Borrowers",
                "Seller Name",
                "Servicer Name",
                "Super Conforming Flag",
                "Pre-HARP Loan Sequence Number",
                "Program Indicator",
                "HARP Indicator",
                "Property Valuation Method",
                "Interest Only (I/O) Indicator",
                "Mortgage Insurance Cancellation Indicator"
            ]

            df = pd.read_csv(uploaded_file, sep="|", header=None, names=columns)

            #variables
            path_to_repo_dir="C:/Users/91730/Desktop/BigData"
            path_to_data_dir=f"{path_to_repo_dir}/gx/data"
            expectation_suite_name="Origination_Data_File_Suite"

            context = FileDataContext.create(project_root_dir=path_to_repo_dir)

            df.to_csv(f"{path_to_data_dir}/orig.csv", index=False)

            # # Give your Datasource a name
            # datasource_name = "Local_FileSystem_Source"
            # datasource = context.sources.add_pandas_filesystem(name=datasource_name, base_dir=path_to_data_dir)

            # # Give your first Asset a name
            # asset_name = None
            # path_to_data = None
            # # to use sample data uncomment next line
            # # path_to_data = "https://raw.githubusercontent.com/great-expectations/gx_tutorials/main/data/yellow_tripdata_sample_2019-01.csv"
            # asset = datasource.add_csv_asset(asset_name, filepath_or_buffer=path_to_data)

            # # Build batch request
            # batch_request = asset.build_batch_request()

            validator = context.sources.pandas_default.read_csv(
                f"{path_to_data_dir}/orig.csv"
            )

            validator.expect_column_values_to_be_between(column="Credit Score", min_value=300, max_value=9999)
            # validator.expect_column_values_to_be_between(column="CREDIT SCORE", min_value=300, max_value=9999)
            # validator.expect_column_values_to_be_in_set(column="FIRST TIME HOMEBUYER FLAG", value_set=['Y', 'N'])
            # validator.expect_column_values_to_be_between(column="MORTGAGE INSURANCE PERCENTAGE (MI %)", min_value=0, max_value=35)
            # validator.expect_column_values_to_be_in_set(column="NUMBER OF UNITS", value_set=[1, 2, 3, 4])
            # validator.expect_column_values_to_be_in_set(column="OCCUPANCY STATUS", value_set=['P', 'I', 'S', '9'])
            # validator.expect_column_values_to_be_between(column="ORIGINAL COMBINED LOAN-TO-VALUE (CLTV)", min_value=1, max_value=200)

            checkpoint = context.add_or_update_checkpoint(
                name="my_quickstart_checkpoint",
                validator=validator,
            )

            checkpoint_result = checkpoint.run(run_name="Manual Run")

            context.view_validation_result(checkpoint_result)


            

        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please upload a file before generating the data summary.")


