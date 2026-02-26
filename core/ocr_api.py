# Please make sure the requests library is installed
# pip install requests
import base64
import requests
from pathlib import Path
from config import settings
import os
import sys


class OCRClient:
    def __init__(self, api_url: str,
                 ocr_token: str):
        self._validate_settings()
        self.api_url = api_url
        self.ocr_token = ocr_token
        # self.timeout = timeout
        # self.session = requests.Session()

        '''self.session.headers.update({
            "Authorization": f"token {self.ocr_token}",
            "Content-Type": "application/json"
        })
        '''

    # Validate that required settings are present
    def _validate_settings(self):
        if not settings.API_URL:
            raise ValueError("API_URL is not set")
        if not settings.OCR_TOKEN:
            raise ValueError("OCR_TOKEN is not set")

    def _encode_file_to_base64(self, input_chunk_path) -> str:
        with open(input_chunk_path, "rb") as file:
            file_bytes = file.read()
            return base64.b64encode(file_bytes).decode("ascii")

    def _call_ocr_api(self, file_data: str) -> dict:
        headers = {
            "Authorization": f"token {self.ocr_token}",
            "Content-Type": "application/json"
        }
        required_payload = {
            "file": file_data,
            "fileType": 0,  # For PDF documents, set `fileType` to 0;
                            # for images, set `fileType` to 1
        }

        optional_payload = {
            "useDocOrientationClassify": False,
            "useDocUnwarping": False,
            "useChartRecognition": False,
        }

        payload = {**required_payload, **optional_payload}

        response = requests.post(self.api_url,
                                 json=payload,
                                 headers=headers)
        if response.status_code != 200:
            raise Exception(
                f"API call failed - status code {response.status_code}: {response.text}")
        return response.json()["result"]

    def process_file(self, file_path):
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        print(f"Processing: {file_path}")
        # Original size
        original_size = os.path.getsize(file_path) / 1024 / 1024
        print(f"Original size: {original_size:.2f} MB")

        file_data = self._encode_file_to_base64(file_path)

        # Base64 size in MB
        base64_size = sys.getsizeof(file_data) / 1024 / 1024
        print(f"Base64 size: {base64_size:.2f} MB")

        return self._call_ocr_api(file_data)

    # def close(self):
    #  self.session.close()


if __name__ == "__main__":
    ocr_client = OCRClient(
        api_url=settings.API_URL,
        ocr_token=settings.OCR_TOKEN)
    path = "G:\\viet-ocr-lite\\input\\image\\test-1.pdf"
    ocr_client.process_file(Path(path))
    # ocr_client.close()
