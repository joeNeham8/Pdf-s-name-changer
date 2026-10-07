# PDF Pupil Name & Admission Number Renamer

A Python-based OCR tool that automatically extracts a **pupil's name** and **admission number** from scanned PDF documents and renames the PDFs accordingly.

This project is designed to simplify the process of organizing large numbers of scanned student documents.

## Features

- Upload multiple PDF files at once
- Supports scanned/image-based PDFs
- Extracts text using OCR
- Automatically detects:
  - Pupil Name
  - Admission Number
- Renames PDFs using the format:

```text
Pupil Name_Admission Number.pdf
```

- Handles duplicate filenames
- Processes multiple PDFs in a single run
- Creates a ZIP file containing all renamed PDFs
- Provides a processing summary
- Identifies PDFs where required information could not be found
- Runs directly in Google Colab

## Example

If a scanned PDF contains:

```text
Name of Pupil: RAHUL KUMAR
Admission No: 15482
```

The original file:

```text
scan001.pdf
```

will be renamed to:

```text
RAHUL KUMAR_15482.pdf
```

After processing multiple files, the program creates:

```text
renamed_pupil_pdfs.zip
```

containing all the renamed PDFs.

## Technologies Used

- Python
- Tesseract OCR
- pytesseract
- pdf2image
- Poppler
- Google Colab

## Requirements

The project requires:

- Python 3.x
- Tesseract OCR
- Poppler
- Python packages:
  - `pytesseract`
  - `pdf2image`

When running in Google Colab, the required dependencies can be installed with:

```bash
!apt-get update -qq
!apt-get install -y -qq poppler-utils tesseract-ocr
!pip install -q pytesseract pdf2image
```

## How to Use

### 1. Open Google Colab

Create a new notebook in [Google Colab](https://colab.research.google.com/) and run the installation command above.

### 2. Run the Python Script

Run the main Python script.

You will be prompted to upload your PDF files.

### 3. Upload PDFs

Select one or more scanned PDF files from your computer.

The program will process each PDF and attempt to identify the pupil's name and admission number.

### 4. Download the Results

After processing, all successfully renamed PDFs are placed into:

```text
renamed_pdfs/
```

The program then creates:

```text
renamed_pupil_pdfs.zip
```

Download the ZIP file to get all processed PDFs at once.

## Processing Workflow

```text
Upload PDFs
     |
     v
Convert PDF pages to images
     |
     v
OCR using Tesseract
     |
     v
Extract pupil name
     |
     v
Extract admission number
     |
     v
Generate new filename
     |
     v
Rename PDF
     |
     v
Create ZIP archive
     |
     v
Download results
```

## Filename Format

The generated filename follows this format:

```text
<Name of Pupil>_<Admission Number>.pdf
```

For example:

```text
ANU MARIA JOSEPH_15482.pdf
```

## Handling Failed Files

If the program cannot find the pupil's name or admission number, the file is not renamed.

The program displays the reason, for example:

```text
❌ FILES THAT NEED ATTENTION:

student01.pdf
→ Pupil name not found

student02.pdf
→ Admission number not found
```

This makes it easy to manually check problematic documents.

## OCR Accuracy

The accuracy of the extracted information depends on the quality of the scanned PDF.

For best results:

- Use high-resolution scans
- Ensure the document is not heavily blurred
- Use clear printed text
- Avoid rotated or distorted pages
- Ensure the name and admission number are clearly visible

Handwritten text may not be recognized accurately by standard Tesseract OCR.

## Duplicate Files

If two PDFs have the same pupil name and admission number, the program prevents overwriting.

For example:

```text
RAHUL KUMAR_15482.pdf
RAHUL KUMAR_15482 (1).pdf
RAHUL KUMAR_15482 (2).pdf
```

## Project Structure

A simple repository structure can look like:

```text
pdf-pupil-renamer/
│
├── README.md
├── pdf_renamer.py
└── requirements.txt
```

## requirements.txt

You can create a `requirements.txt` file containing:

```text
pytesseract
pdf2image
```

Note that **Tesseract OCR** and **Poppler** are system dependencies and are installed separately when using Google Colab.

## Future Improvements

Possible improvements include:

- Better OCR preprocessing
- Support for handwritten text
- Automatic correction of common OCR errors
- Support for different document layouts
- Desktop GUI application
- Excel/CSV report generation
- Automatic organization by class
- Automatic organization by academic year
- Progress bar for large batches
- Support for additional student information

## License

This project is licensed under the MIT License.

You are free to use, modify, and distribute this project in accordance with the license terms.

## Contributing

Contributions are welcome.

If you would like to improve the project:

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Commit your changes
5. Push the branch
6. Open a Pull Request

## Author

Developed as a tool for automating the organization and renaming of scanned student PDF documents.

---

**If you find this project useful, consider giving the repository a ⭐ star on GitHub!**
