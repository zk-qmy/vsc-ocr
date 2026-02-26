from pypdf import PdfReader, PdfWriter
from config import settings


class PDFSplitter:
    def __init__(self,
                 input_pdf_path,
                 output_chunk_dir,
                 pages_per_split=100):
        self.input_pdf_path = input_pdf_path
        self.output_chunk_dir = output_chunk_dir
        self.pages_per_split = pages_per_split
        self._create_output_chunk_dir()

    def _create_output_chunk_dir(self):
        self.output_chunk_dir.mkdir(parents=True, exist_ok=True)

    def _get_pdf_file_name(self):
        return self.input_pdf_path.stem

    def split(self):
        reader = PdfReader(self.input_pdf_path)
        total_pages = len(reader.pages)
        print(f"Total pages in PDF: {total_pages}")

        if total_pages == 0:
            print("No pages found in the PDF.")
            return None
        elif total_pages <= self.pages_per_split:
            print(f"PDF has < {self.pages_per_split} pages. No splitting!")
            return [self.input_pdf_path]

        # create sub folder for a pdf book
        file_chunk_path = self.output_chunk_dir / self._get_pdf_file_name()
        file_chunk_path.mkdir(parents=True, exist_ok=True)
        # store created file paths to return later
        created_files = []

        for i in range(0, total_pages, self.pages_per_split):
            writer = PdfWriter()
            # add pages directly without copying full file to memory
            writer.append(
                fileobj=self.input_pdf_path,
                pages=(i, min(i+self.pages_per_split, total_pages))
            )

            output_path = file_chunk_path / \
                f"part_{i//self.pages_per_split + 1}.pdf"

            with open(output_path, "wb") as f:
                writer.write(f)
            print(f"Created: {output_path}")
            created_files.append(output_path)
        return created_files


def main():
    splitter = PDFSplitter(
        input_pdf_path=settings.pdf_full_path,
        output_chunk_dir=settings.pdf_splitted_full_path
    )
    created_chunks_paths = splitter.split()
    print(f"Created {len(created_chunks_paths)} chunks")


if __name__ == "__main__":
    main()
