from diagrams import Diagram, Cluster
from diagrams.onprem.client import Users
from diagrams.aws.compute import LambdaFunction
from diagrams.aws.ml import Sagemaker
from diagrams.gcp.analytics import BigQuery
from diagrams.aws.storage import S3

# Define custom nodes for Nougat API and Streamlit
class NougatNode(LambdaFunction):
    def __init__(self, label):
        super().__init__(label)

# Define custom nodes for PyPDF, Nougat API, and Streamlit
class PyPDFNode(LambdaFunction):
    def __init__(self, label):
        super().__init__(label)

with Diagram("Streamlit PDF Report Generation", show=False):
    with Cluster("Users"):
        users = Users("Users")
    
    with Cluster("Select Library"):
        select_library = Sagemaker("Select Library")
    
    with Cluster("PyPDF Library"):
        py_pdf = PyPDFNode("PyPDF")
    
    with Cluster("Nougat API (Google Colab)"):
        nougat_api = NougatNode("Nougat API")
    
    with Cluster("Streamlit App"):
        streamlit_app = Sagemaker("Streamlit App")
    
    with Cluster("Report Generation"):
        report_generation = BigQuery("Report Generation")

    users >> select_library >> py_pdf >> streamlit_app >> report_generation 
    users >> select_library >> nougat_api >> streamlit_app >> report_generation 
