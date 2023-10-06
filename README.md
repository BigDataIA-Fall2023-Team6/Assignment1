# PDF Document Summary Tool & Pandas, Great Expectaions Data Profiling

## Codelab
-[Codelab](https://codelabs-preview.appspot.com/?file_id=1WfSlL-OB7Sc2QXrh8V9PwkwicuQSUq4kcLq5EEJOwYw)

## Table of Contents
- [PDF Document Summary Tool \& Pandas, Great Expectaions Data Profiling](#pdf-document-summary-tool--pandas-great-expectaions-data-profiling)
  - [Table of Contents](#table-of-contents)
  - [PDF Document Summary Tool](#pdf-document-summary-tool)
    - [Overview](#overview)
    - [Prerequisites](#prerequisites)
      - [Additional Prerequisite for Nougat](#additional-prerequisite-for-nougat)
    - [Usage](#usage)
    - [Evaluation and Recommendations](#evaluation-and-recommendations)
    - [Contributors](#contributors)
    - [License](#license)
    - [Acknowledgments](#acknowledgments)
    - [References](#references)
  - [Streamlit Data Profiling and Great Expectations](#streamlit-data-profiling-and-great-expectations)
    - [Overview](#overview-1)
    - [Prerequisites](#prerequisites-1)
    - [Usage](#usage-1)
    - [Evaluation and Recommendations](#evaluation-and-recommendations-1)
    - [Contributors](#contributors-1)
    - [License](#license-1)
    - [Acknowledgments](#acknowledgments-1)
  - [References](#references-1)
    - [Conclusion](#conclusion)

## PDF Document Summary Tool

### Overview
The PDF Document Summary Tool is a web application built using Streamlit. It enables analysts to load PDF documents from the U.S. Securities and Exchange Commission (SEC) website and generate summaries of these documents. This tool offers the choice between two different libraries, Nougat and PyPDF, for PDF analysis. The primary goal is to evaluate the effectiveness of these libraries in extracting and summarizing information from SEC PDF documents.

### Prerequisites
Before using the PDF Document Summary Tool, make sure you have the following dependencies installed:
- Python 3.10+
- Streamlit
- Requests
- PyPDF2 (for PyPDF library)
- Nougat (for Nougat library)

#### Additional Prerequisite for Nougat
To use the Nougat library, follow these additional steps:
1. Install the required packages in a Google Colab environment.
2. Configure `pyngrok` to establish a tunnel for the Nougat API.

### Usage
1. Clone the repository to your local machine.
2. Run the Streamlit application.
3. Access the application in your web browser.
4. Enter the URL of a PDF document from the SEC website.
5. Choose either Nougat or PyPDF as the library for PDF analysis.
6. Click the "Convert" button to initiate the analysis.
7. View the extracted text and summary information for the PDF document.

### Evaluation and Recommendations
After testing the tool with different PDF files, provide recommendations on the pros and cons of using Nougat and PyPDF for PDF analysis. Share your findings and insights with your team to inform future projects.

### Contributors
- Abhishek Sand - 33.3%
- Dilip Sharma - 33.3%
- Vivek Hanagoji - 33.3%

### License
This project is licensed under the MIT License.

### Acknowledgments
- The Streamlit team for providing an excellent framework for creating interactive web applications.
- The authors of Nougat and PyPDF for their respective libraries.
- Piyush, our TA, for constant support and help during lab sessions and TA hours.

### References
- [Nougat Library](https://nougatlib.com/)
- [PyPDF2 Library](https://pythonhosted.org/PyPDF2/)
- [U.S. Securities and Exchange Commission (SEC)](https://www.sec.gov/)

## Streamlit Data Profiling and Great Expectations

### Overview
This repository contains a Streamlit-based application that enables users to upload CSV or XLS files for data profiling and validation. It leverages Pandas Profiling and Great Expectations to provide data summaries and quality checks. Users can choose the data type (Origination Data or Monthly Performance Data) and generate reports.

### Prerequisites
Before running the application, ensure that you have the following dependencies installed:
- Python 3.10+
- Streamlit
- Pandas
- ydata_profiling
- streamlit_pandas_profiling
- great_expectations
- re
- os

### Usage
1. Clone this repository to your local machine.
2. Run the Streamlit application.
3. Access the application in your web browser.
4. Upload a CSV or XLS file.
5. Choose the data type (Origination Data or Monthly Performance Data) based on your file content.
6. Click the "Generate Data Summary" button to initiate data profiling and validation.
7. View the data summary and validation results, including Pandas Profiling reports and Great Expectations checks.

### Evaluation and Recommendations
After using the Streamlit Data Profiling and Great Expectations tool with different data files, provide recommendations on the effectiveness and usability of the tool. Consider factors such as data profiling capabilities, validation checks, and ease of use when making your recommendations.

### Contributors
Abhishek Sand - 33.3%
Dilip Sharma - 33.3%
Vivek Hanagoji - 33.3%
### License
This project is licensed under the MIT License.

### Acknowledgments
- The Streamlit team for providing a powerful framework for creating data-driven web applications.
- The creators of Pandas, ydata_profiling, streamlit_pandas_profiling, and Great Expectations for their valuable contributions to the data science community.
- Our TA, Piyush, for ongoing support and assistance during your course.

## References

- [Streamlit](https://streamlit.io/)
- [Pandas](https://pandas.pydata.org/)
- [Pandas Profiling](https://github.com/pandas-profiling/pandas-profiling)
- [Great Expectations](https://greatexpectations.io/)

### Conclusion
   This combined README provides an overview, usage instructions, and guidance for both the PDF Document Summary Tool and the Streamlit Data Profiling and Great Expectations tool. You can refer to the relevant sections based on your specific use case and requirements.

We encourage you to explore these tools, share your feedback, and contribute to their ongoing development to support data analysis and document summarization tasks.

For any questions or issues, please feel free to reach out to the contributors mentioned in the respective sections.
