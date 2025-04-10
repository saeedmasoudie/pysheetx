import sys
import os
import json
import openai
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QFileDialog,
    QLineEdit, QTextEdit, QStackedLayout, QMessageBox, QVBoxLayout,
    QGridLayout, QSizePolicy, QComboBox
)
from PySide6.QtGui import QIcon, QFont
from PySide6.QtCore import Qt
from google.oauth2 import service_account
from googleapiclient.discovery import build

class SheetSmartApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SheetSmart Dashboard")
        self.setMinimumSize(800, 600)

        self.credentials_path = None
        self.api_key = None
        self.uploaded_file_label = QLabel()

        self.layout = QStackedLayout()
        self.init_main_page()
        self.init_page1()
        self.init_page2()

        self.setLayout(self.layout)
        self.setStyleSheet("""
            QWidget { background-color: #121212; color: #e0e0e0; }
            QLabel { font-size: 15px; }
            QPushButton {
                padding: 10px;
                font-size: 15px;
                border-radius: 10px;
                background-color: #1e88e5;
                color: white;
            }
            QPushButton:hover {
                background-color: #1565c0;
            }
            QLineEdit, QTextEdit {
                font-size: 15px;
                padding: 8px;
                border: 1px solid #555;
                border-radius: 6px;
                background-color: #1e1e1e;
                color: white;
            }
            QTextEdit { min-height: 100px; }
        """)

    def init_main_page(self):
        page = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        title = QLabel("📈 Welcome to SheetSmart")
        title.setStyleSheet("font-size: 28px; font-weight: bold; margin-bottom: 30px;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        start_button = QPushButton("📊 Start SheetSmart")
        start_button.setFixedWidth(250)
        start_button.setFixedHeight(50)
        start_button.clicked.connect(lambda: self.layout.setCurrentIndex(1))

        layout.addWidget(start_button, alignment=Qt.AlignCenter)
        page.setLayout(layout)
        self.layout.addWidget(page)

    def init_page1(self):
        page = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        title = QLabel("🔐 Step 1: API Key & Credentials")
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        form_layout = QGridLayout()
        form_layout.setSpacing(15)
        form_layout.setColumnStretch(0, 1)
        form_layout.setColumnStretch(1, 3)

        self.api_input = QLineEdit()
        self.api_input.setPlaceholderText("Enter OpenAI API Key")

        self.upload_button = QPushButton("📂 Upload credentials.json")
        self.upload_button.clicked.connect(self.upload_json)

        self.validate_button = QPushButton("✅ Validate and Continue")
        self.validate_button.clicked.connect(self.validate_credentials)

        self.uploaded_file_label.setStyleSheet("color: #81c784; font-style: italic;")

        form_layout.addWidget(QLabel("🔑 OpenAI API Key:"), 0, 0)
        form_layout.addWidget(self.api_input, 0, 1)
        form_layout.addWidget(QLabel("📁 Upload credentials.json:"), 1, 0)
        form_layout.addWidget(self.upload_button, 1, 1)
        form_layout.addWidget(self.uploaded_file_label, 2, 1)
        form_layout.addWidget(self.validate_button, 3, 1)

        layout.addLayout(form_layout)
        page.setLayout(layout)
        self.layout.addWidget(page)

    def init_page2(self):
        page = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        title = QLabel("📊 Step 2: Sheet ID, Range, and AI Prompt")
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        form_layout = QGridLayout()
        form_layout.setSpacing(15)
        form_layout.setColumnStretch(0, 1)
        form_layout.setColumnStretch(1, 3)

        self.sheet_id_input = QLineEdit()
        self.sheet_id_input.setPlaceholderText("Enter Google Sheet ID")

        self.range_input = QLineEdit()
        self.range_input.setPlaceholderText("Enter range (e.g., A1:D10)")

        self.prompt_input = QTextEdit()
        self.prompt_input.setPlaceholderText("Enter your AI prompt")

        self.action_select = QComboBox()
        self.action_select.addItem("Read Data (Only AI Process)")
        self.action_select.addItem("Add Data to Sheet (AI Process & Add)")

        self.submit_button = QPushButton("🤖 Submit to AI")
        self.submit_button.clicked.connect(self.process_sheet_with_ai)

        self.result_box = QTextEdit()
        self.result_box.setReadOnly(True)
        self.result_box.setPlaceholderText("AI output will appear here")
        self.result_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        form_layout.addWidget(QLabel("🆔 Google Sheet ID:"), 0, 0)
        form_layout.addWidget(self.sheet_id_input, 0, 1)
        form_layout.addWidget(QLabel("📌 Range (e.g., A1:D10):"), 1, 0)
        form_layout.addWidget(self.range_input, 1, 1)
        form_layout.addWidget(QLabel("📝 AI Prompt:"), 2, 0)
        form_layout.addWidget(self.prompt_input, 2, 1)
        form_layout.addWidget(QLabel("Choose Action:"), 3, 0)
        form_layout.addWidget(self.action_select, 3, 1)
        form_layout.addWidget(self.submit_button, 4, 1)
        form_layout.addWidget(QLabel("📬 AI Output:"), 5, 0)
        form_layout.addWidget(self.result_box, 5, 1)

        layout.addLayout(form_layout)
        page.setLayout(layout)
        self.layout.addWidget(page)

    def upload_json(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select credentials.json", "", "JSON Files (*.json)")
        if file_path:
            self.credentials_path = file_path
            self.uploaded_file_label.setText(f"✅ Loaded: {os.path.basename(file_path)}")

    def validate_credentials(self):
        self.api_key = self.api_input.text().strip()
        if not self.api_key:
            QMessageBox.warning(self, "Missing", "Please enter the OpenAI API key.")
            return
        if not self.credentials_path:
            QMessageBox.warning(self, "Missing", "Please upload credentials.json.")
            return
        try:
            client = openai.OpenAI(api_key=self.api_key)
            client.models.list()
            self.layout.setCurrentIndex(2)
        except Exception as e:
            QMessageBox.critical(self, "API Error", f"OpenAI API key is invalid.{str(e)}")

    def process_sheet_with_ai(self):
        sheet_id = self.sheet_id_input.text().strip()
        cell_range = self.range_input.text().strip()
        prompt = self.prompt_input.toPlainText().strip()

        if not all([sheet_id, cell_range, prompt]):
            QMessageBox.warning(self, "Missing", "Please fill in all fields.")
            return

        try:
            credentials = service_account.Credentials.from_service_account_file(self.credentials_path)
            service = build('sheets', 'v4', credentials=credentials)
            sheet = service.spreadsheets()

            result = sheet.values().get(spreadsheetId=sheet_id, range=cell_range).execute()
            values = result.get('values', [])

            if not values:
                self.result_box.setPlainText("No data found in the specified range.")
                return

            action = self.action_select.currentText()

            instruction_line = "Please provide your response in a clean and structured manner, with only relevant data included. If asked to add data to the sheet, make sure to format it as a row with comma-separated values."
            data_str = "\n".join([", ".join(row) for row in values])

            if action == "Add Data to Sheet (AI Process & Add)":
                full_prompt = f"{instruction_line}\n{prompt}\n\nData:\n{data_str}"
            else:
                full_prompt = f"{prompt}\n\nData:\n{data_str}"

            client = openai.OpenAI(api_key=self.api_key)
            completion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "developer", "content": full_prompt}]
            )
            ai_reply = completion.choices[0].message.content.strip()

            structured_response = ai_reply.split("\n")[0] 
            normal_response = ai_reply[len(structured_response):].strip()

            self.result_box.setPlainText(normal_response)

            lines = normal_response.split("\n")
            valid_data = [line.split(",") for line in lines if "," in line]

            if not valid_data:
                QMessageBox.warning(self, "Invalid AI Output", "AI response doesn't include valid data.")
                return

            if action == "Add Data to Sheet (AI Process & Add)":
                new_row = valid_data[0]
                current_row_count = len(values)
                start_col_letter = cell_range.split(":")[0][0]
                insert_range = f"{start_col_letter}{current_row_count + 1}"

                sheet.values().update(
                    spreadsheetId=sheet_id,
                    range=insert_range,
                    valueInputOption="RAW",
                    body={"values": [new_row]}
                ).execute()

                metadata = service.spreadsheets().get(spreadsheetId=sheet_id).execute()
                sheet_id_number = metadata['sheets'][0]['properties']['sheetId']

                highlight_request = {
                    "repeatCell": {
                        "range": {
                            "sheetId": sheet_id_number,
                            "startRowIndex": current_row_count,
                            "endRowIndex": current_row_count + 1,
                        },
                        "cell": {
                            "userEnteredFormat": {
                                "backgroundColor": {
                                    "red": 0.9,
                                    "green": 1.0,
                                    "blue": 0.9
                                }
                            }
                        },
                        "fields": "userEnteredFormat.backgroundColor"
                    }
                }

                service.spreadsheets().batchUpdate(
                    spreadsheetId=sheet_id,
                    body={"requests": [highlight_request]}
                ).execute()

                QMessageBox.information(self, "Success", "✅ AI-generated data was added and highlighted!")

            else:
                QMessageBox.information(self, "Read Complete", "✅ AI has processed the data.")

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SheetSmartApp()
    window.show()
    sys.exit(app.exec())
