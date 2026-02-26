
from core.pdf_splitter import PDFSplitter
from core.ocr_api import OCRClient
from core.saver import ResultSaver
from config import settings
import time


def main():
    # Split PDF into smaller chunks
    splitter = PDFSplitter(
        input_pdf_path=settings.pdf_full_path,
        output_chunk_dir=settings.pdf_splitted_full_path
    )
    created_files = splitter.split()

    # Call OCR API for each created chunk
    ocr_api = OCRClient(
        api_url=settings.API_URL,
        ocr_token=settings.OCR_TOKEN
    )
    saver = ResultSaver(book_root=settings.ocr_book_root)

    for file in created_files:
        try:
            result = ocr_api.process_file(file)
            saver.save_all(result)
            time.sleep(2)
        except Exception as e:
            print(f"Failed processing {file}: {e}")


if __name__ == "__main__":
    main()
