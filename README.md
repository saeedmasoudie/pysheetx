
# PySheetX

PySheetX is a Python-based application that integrates with Google Sheets and OpenAI's GPT models to automate data management and analysis. It enables users to interact with Google Sheets by providing an easy-to-use interface that connects to Google Sheets API and allows AI-powered prompts to manipulate data within the spreadsheet.

**Note:** This project is currently in **Beta** and not fully complete. Some features may still be under development.

## Features

- **Google Sheets Integration**: Load, read, and update data from Google Sheets.
- **AI-Powered Automation**: Use OpenAI's GPT models to analyze and generate new data based on spreadsheet content.
- **Interactive Interface**: User-friendly UI built with PySide6 to guide users through API key setup, Google Sheet selection, and AI prompt submission.
- **Prompt Customization**: Set custom prompts to control how the AI processes the spreadsheet data (e.g., read, add new rows, etc.).
- **Validation and Authentication**: Securely authenticate Google Sheets API using `credentials.json` and OpenAI API key.

## Installation

### Prerequisites

1. Python 3.x installed on your system.
2. The following Python packages should be installed:

   ```bash
   pip install PySide6 google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client openai
   ```

3. Google Sheets API enabled and a `credentials.json` file obtained from the [Google Cloud Console](https://console.cloud.google.com/).
4. An OpenAI API key.

### Steps to Run

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/pysheetx.git
   cd pysheetx
   ```

2. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

3. Launch the application:

   ```bash
   python pysheetx.py
   ```

4. Follow the on-screen instructions to upload your `credentials.json`, input the OpenAI API key, and select the Google Sheet and range to interact with.

## How to Use

1. **Step 1**: Enter your OpenAI API key and upload your `credentials.json` file to authenticate with Google Sheets.
2. **Step 2**: Input the Google Sheet ID, specify the range of data you want to interact with, and enter your AI prompt. The AI can either read the data, update existing rows, or add new rows based on your input.
3. **Step 3**: Click "Submit to AI" to process the data. The AI will generate a response and update the spreadsheet accordingly.

## How to get API and Credentials
1- Download [Google Sheets API Credentials](https://console.cloud.google.com/project)
- Go to the Google Developers Console.
- Create a new project (or select an existing one).
- Enable the Google Sheets API and the Google Drive API.
- Download the credentials.json file.
- Upload the credentials.json file in the app when prompted.

2- Set OpenAI API Key
- Sign up on [OpenAI's website](https://openai.com/api/) to get an API key. Enter the key in the application when prompted.

## Development

If you wish to contribute or make changes to the project, please fork the repository and submit a pull request.

### Project Structure

```
pysheetx/
├── main.py                   # Main application file
├── requirements.txt          # Python dependencies
└── README.md                 # Project documentation
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
