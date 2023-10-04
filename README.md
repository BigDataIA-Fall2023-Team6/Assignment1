# PDF Document Summary Tool

## Overview

This repository contains a Streamlit-based application that allows analysts to load PDF documents from the U.S. Securities and Exchange Commission (SEC) website and generate summaries of these documents. The tool offers the choice between two different libraries, Nougat and PyPDF, for PDF analysis.

The primary goal of this project is to evaluate the effectiveness of these libraries in extracting and summarizing information from SEC PDF documents. The tool facilitates the comparison of the two libraries based on their performance in handling a variety of PDF files.

## Prerequisites

Before running the application, ensure that you have the following dependencies installed:

- Python 3.6+
- Streamlit
- Requests
- PyPDF2 (for PyPDF library)
- Nougat (for Nougat library)

### Additional Prerequisite for Nougat

To use the Nougat library, follow these additional steps:

1. Run the following commands in a Google Colab environment:

   ```python
   !pip3 install "nougat-ocr[api]"
   !nougat_api &>/content/logs.txt &
   ```

2. Run the following Bash script to print the Nougat API logs:

   ```python
   %%bash
   cat /content/logs.txt
   ```

3. Install the `pyngrok` package:

   ```python
   !pip install pyngrok
   ```

4. Configure `pyngrok` to establish a tunnel for the Nougat API:

   ```python
   from pyngrok import ngrok, conf
   import getpass

   conf.get_default().auth_token = "2WDcosyZ4JynOwYd83PWrT9Mg9G_6UjtpDnVkGKLnnzGhZEgW"

   port = 8503

   public_url = ngrok.connect(port)

   print(" * ngrok tunnel \"{}\" -> \"http://127.0.0.1:{}/\"".format(public_url, port))
   ```

Ensure that the Nougat API is running and accessible via the ngrok tunnel before using the Nougat library in the application.

## Usage

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/BigDataIA-Fall2023-Team6/Assignment1.git
   cd Assignment1
   ```

2. Run the Streamlit application:

   ```bash
   streamlit run pdf_summary_app.py
   ```

3. Access the application in your web browser at the provided URL (usually http://localhost:8501).

4. Enter the URL of a PDF document from the SEC website.

5. Choose either Nougat or PyPDF as the library for PDF analysis.

6. Click the "Convert" button to initiate the analysis.

7. View the extracted text and summary information for the PDF document.

## Evaluation and Recommendations

After testing the tool with 5-10 different PDF files from the SEC website, provide your recommendations regarding the pros and cons of using Nougat and PyPDF for PDF analysis. Consider factors such as accuracy, speed, and ease of use when making your recommendations. Share your findings and insights with your team to help them make an informed decision about which library to use for future projects.

## Contributors

- Your Name (@yourusername)
- Additional contributors (if applicable)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- The Streamlit team for providing an excellent framework for creating interactive web applications.
- The authors of Nougat and PyPDF for their respective libraries.
- Piyush our TA for the course Big-Data Systems and Intelligent Analytics for constant support and help for with lab sessions and TA hours.

## References

- [Nougat Library](https://nougatlib.com/)
- [PyPDF2 Library](https://pythonhosted.org/PyPDF2/)
- [U.S. Securities and Exchange Commission (SEC)](https://www.sec.gov/)
