# ParrotGrabber

ParrotGrabber is a Python Flask web application that simplifies the process of batch downloading files from the Hugging Face Hub. It allows users to easily specify a repository, whether it's a model or dataset, and then select specific files or file extensions they want to download. This tool is particularly useful when you need to download multiple files from the Hugging Face Hub in one go, which is not directly supported by the official website.

## Features

- Download files from Hugging Face Hub repositories.
- Select files or file extensions to download in batch.
- Option to download from root directories or subdirectories.
- Avoids including commit messages or other unwanted lines in downloaded files.

## Installation

1. Clone the repository:

   ```git clone https://github.com/yourusername/ParrotGrabber.git```
   
2. Install the required packages using pip:
```pip install -r requirements.txt```

3. Download and configure the Chrome WebDriver for Selenium if you haven't
You can download Chrome WebDriver here: https://chromedriver.chromium.org/downloads

# Usage

Run the Flask app:
```python app.py```

Open your favorite web browser and navigate to http://localhost:5000 to access the ParrotGrabber web interface.

Enter the repository ID (e.g., Anthropic/hh-rlhf), specify whether it's a model or dataset, provide the folder name if applicable, and input the desired file extensions.

Click the "Download" button to initiate the batch download process.

# Acknowledgements

ParrotGrabber was inspired by the need to simplify the batch download process from the Hugging Face Hub. It utilizes the Flask framework for the web application, Selenium for web scraping, and the Hugging Face Hub Python library for efficient file downloads.

# License
This project is licensed under the MIT License.

