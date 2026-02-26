# VSC-OCR

A OCR pipeline for extracting Vietnamese printed text from PDF documents.

This project provides a structured workflow to:

* Split PDFs into chunks
* Send chunks to PaddleOCR API
* Optionally post-process text (correction)
* Save structured outputs

---

## 📌 Features

* 📄 PDF → PDF chunks
* 🖼 OCR processing
* 💾 Structured output saving
* ⚙️ Environment-based configuration
* 🔐 Token-based API authentication

---

## 🏗 Project Structure

```
vsc-ocr/
│
├── core/
│   ├── ocr_api.py          # Send image to OCR API
│   ├── pdf_splitter.py     # Split PDF into images
│   ├── saver.py            # Save output results
│   └── __init__.py
│
├── input/
│   ├── image/              # Test images
│   └── pdf-doc/            # Test PDFs
│
├── config.py               # Configuration loader
├── main.py                 # Entry point
├── pyproject.toml
├── .env.example
└── README.md
```

---

# ⚙️ Workflow

The OCR pipeline follows this flow:

```
PDF 
      ↓
Split PDF into chunks (100 pages each)
      ↓
Send each chunk to OCR API
      ↓
(Optional) Text correction
      ↓
Save ordered output
```

### Step-by-step explanation

### 1️⃣ Input

* Accepts:

  * PDF file

### 2️⃣ PDF Splitting

`core/pdf_splitter.py`

* Converts PDF pages into smaller chunks
* Ensures page order is preserved

### 3️⃣ OCR API Processing

`core/ocr_api.py`

* Sends image (base64 encoded) to PaddleOCR API
* Uses Token authentication
* Receives extracted Vietnamese text in JSON format

### 4️⃣ (Optional) Text Correction

* Sends raw OCR text to correction API
* Improves Vietnamese diacritics & formatting

### 5️⃣ Saving Output

`core/saver.py`

* Writes text results
* Keeps correct page ordering
* Can store JSON, markdown, images

---

# 🚀 How to Run

## 1️⃣ Clone the repository

```bash
git clone https://github.com/your-username/viet-ocr-lite.git
cd vsc-ocr
```

---

## 2️⃣ Create Virtual Environment

```bash
python -m venv .venv
```

Activate it:

**Windows (PowerShell):**

```bash
.venv\Scripts\activate
```

**Mac/Linux:**

```bash
source .venv/bin/activate
```

---

## 3️⃣ Install Dependencies

If using `uv`:

```bash
uv sync
```
---

## 4️⃣ Configure Environment Variables

Create a `.env` file based on `.env.example`:

```
API_URL=your_ocr_api_url
TOKEN=your_api_token
PDF_PATH=path_to_pdf
```

Or export manually:

```bash
set API_URL=...
set TOKEN=...
```

---

## 5️⃣ Run the Application

```bash
python main.py
```

If processing a specific PDF:

```bash
python main.py --input input/pdf-doc/test.pdf
```

---

# 🧠 Configuration

Configuration is managed via:

* `config.py`
* Environment variables
* `.env` file

Main settings:

* `API_URL`
* `TOKEN`
* `PDF_PATH`
* Output directory

---

# 📦 Example Output

After processing:

```
output/
├── book-A/
│   ├── raw/  # Save raw json response
│   ├── markdown/  # Save in markdown format 
│   └── imgs/  # Save Layout images
└── ...
```

Each page is preserved in correct order.

---

# 🛠 Tech Stack

* Python 3.10+
* Requests
* PDF processing tools

---

# 🧪 Example Use Case

This project is designed for:

* Vietnamese book digitization
* Academic document OCR
* Structured text extraction
* OCR experimentation and benchmarking

---

# 🔮 Future Improvements

* Batch processing support
* Parallel OCR requests
* Confidence score filtering
* Layout-aware extraction

