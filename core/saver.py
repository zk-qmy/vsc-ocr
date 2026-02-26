import json
import requests


class ResultSaver:
    def __init__(self, book_root):
        # self.session = session
        self.book_root = book_root
        self.raw_dir = book_root / "raw"
        self.md_dir = book_root / "markdown"
        self.img_dir = book_root / "images"
        self._create_dirs()

    def _create_dirs(self):
        self.raw_dir.mkdir(parents=True, exist_ok=True)
        self.md_dir.mkdir(parents=True, exist_ok=True)
        self.img_dir.mkdir(parents=True, exist_ok=True)

    def save_raw_json(self, result: dict, filename: str):
        path = self.raw_dir / f"{filename}.json"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=4)
        print(f"Raw JSON saved at {path}")

    def save_img_from_markdown(self, result, filename: str):
        for img_path, img in result["markdown"]["images"].items():
            full_img_path = self.img_dir / img_path
            full_img_path.parent.mkdir(parents=True, exist_ok=True)

            response = requests.get(img)
            response.raise_for_status()  # Ensure we got a successful response

            with open(full_img_path, "wb") as img_file:
                img_file.write(response.content)
            print(f"Image saved to: {full_img_path}")

    def save_img_from_output_images(self, result, filename: str):
        for img_name, img in result["outputImages"].items():
            img_response = requests.get(img)
            if img_response.status_code == 200:
                file_path = self.img_dir / f"{img_name}_{filename}.jpg"
                with open(file_path, "wb") as f:
                    f.write(img_response.content)
                print(f"Image saved to: {file_path}")
            else:
                print(
                    f"Failed to download image {img_name}, status code {img_response.status_code}")

    def save_all(self, result):
        # output_path.mkdir(parents=True, exist_ok=True)
        for i, res in enumerate(result["layoutParsingResults"]):
            base_name = f"page_{i}"

            # Save each layout parsing result as a separate JSON file
            self.save_raw_json(res, base_name)

            # Save combined markdown text to a single .md file
            md_filename = self.md_dir / f"{base_name}.md"
            with open(md_filename, "w", encoding="utf-8") as md_file:
                md_file.write(res["markdown"]["text"])
            print(f"Markdown document saved at {md_filename}")

            # Save images from markdown
            self.save_img_from_markdown(res, base_name)

            # Save images from outputImages
            self.save_img_from_output_images(res, base_name)
