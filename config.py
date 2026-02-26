from pathlib import Path
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Base directory of project
    BASE_DIR: Path = Path(__file__).resolve().parent

    # Environment variables
    PDF_PATH: str

    OUTPUT_ROOT: str
    PDF_CHUNK_ROOT: str

    API_URL: str
    OCR_TOKEN: str
    # PROTONX_API_KEY: str

    # base paths
    @property
    def pdf_full_path(self) -> Path:
        return self.BASE_DIR / self.PDF_PATH

    # OUUPUT DIRS
    @property
    def output_root(self) -> Path:
        return self.BASE_DIR / self.OUTPUT_ROOT

    @property
    def pdf_splitted_full_path(self) -> Path:
        return self.BASE_DIR / self.PDF_CHUNK_ROOT

    # Dynamic output paths for OCR results
    @property
    def book_name(self) -> str:
        return self.pdf_full_path.stem

    @property
    def ocr_book_root(self) -> Path:
        return self.output_root / self.book_name

    @property
    def ocr_json_dir(self) -> Path:
        return self.ocr_book_root / "raw"

    @property
    def ocr_md_dir(self) -> Path:
        return self.ocr_book_root / "markdown"

    @property
    def ocr_img_dir(self) -> Path:
        return self.ocr_book_root / "images"

    class Config:
        env_file = ".env"


settings = Settings()
