from diagrams import Cluster, Diagram
from diagrams.onprem.client import Users
from diagrams.onprem.compute import Server
from diagrams.programming.language import Python
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB

# Define a custom node for file uploads
class FileUpload(Python):
    def __init__(self, label):
        super().__init__(label)

with Diagram("Streamlit Data Profiling and Great Expectations", show=False):
    with Cluster("Users"):
        users = Users("Users")
    
    with Cluster("Streamlit Server"):
        streamlit_server = Server("Streamlit Server")
    
    with Cluster("Data Processing"):
        file_upload = FileUpload("User File Upload")
        pandas_profiling = Python("Pandas Profiling")
        great_expectations = EC2("Great Expectations")
        report_generation = RDS("Report Generation")

    users >> file_upload
    file_upload >> pandas_profiling >> great_expectations >> report_generation
    streamlit_server >> file_upload
