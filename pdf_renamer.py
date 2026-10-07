import os
import re
import zipfile
import shutil
import pytesseract

from pdf2image import convert_from_path
from google.colab import files


# ==========================================
# UPLOAD ALL PDF FILES
# ==========================================

uploaded = files.upload()

print(f"\n📂 {len(uploaded)} PDF files uploaded.\n")


# ==========================================
# CREATE OUTPUT FOLDER
# ==========================================

output_folder = "renamed_pdfs"

if os.path.exists(output_folder):
    shutil.rmtree(output_folder)

os.makedirs(output_folder)


# ==========================================
# RESULTS
# ==========================================

successful = []
failed = []


# ==========================================
# PROCESS EACH PDF
# ==========================================

for file_number, pdf_filename in enumerate(uploaded.keys(), start=1):

    print("=" * 60)
    print(f"📄 Processing {file_number}/{len(uploaded)}: {pdf_filename}")
    print("=" * 60)

    if not pdf_filename.lower().endswith(".pdf"):
        print("❌ Not a PDF")
        failed.append((pdf_filename, "Not a PDF"))
        continue

    try:

        # ==========================================
        # CONVERT PDF TO IMAGES
        # ==========================================

        pages = convert_from_path(
            pdf_filename,
            dpi=300
        )

        print(f"📑 Pages: {len(pages)}")


        # ==========================================
        # OCR
        # ==========================================

        full_text = ""

        for page_number, page in enumerate(pages, start=1):

            print(
                f"   🔍 OCR page {page_number}/{len(pages)}..."
            )

            text = pytesseract.image_to_string(
                page,
                config="--psm 6"
            )

            full_text += "\n" + text


        # ==========================================
        # FIND PUPIL NAME
        # ==========================================

        name_patterns = [

            r"Name\s+of\s+(?:the\s+)?Pupil\s*[:\-]?\s*(.+)",

            r"Name\s+of\s+(?:the\s+)?Student\s*[:\-]?\s*(.+)",

            r"Name\s*[:\-]\s*(.+)"

        ]

        pupil_name = None

        for pattern in name_patterns:

            match = re.search(
                pattern,
                full_text,
                re.IGNORECASE
            )

            if match:

                pupil_name = match.group(1).strip()

                break


        # ==========================================
        # FIND ADMISSION NUMBER
        # ==========================================

        admission_patterns = [

            r"Admission\s*(?:No|Number|Num)\.?\s*[:\-]?\s*([A-Za-z0-9\/\-]+)",

            r"Admission\s*[:\-]?\s*([A-Za-z0-9\/\-]+)",

            r"Adm\.?\s*(?:No|Number)\.?\s*[:\-]?\s*([A-Za-z0-9\/\-]+)"

        ]

        admission_no = None

        for pattern in admission_patterns:

            match = re.search(
                pattern,
                full_text,
                re.IGNORECASE
            )

            if match:

                admission_no = match.group(1).strip()

                break


        # ==========================================
        # CLEAN NAME
        # ==========================================

        if pupil_name:

            pupil_name = pupil_name.strip(
                " :-._"
            )

            pupil_name = re.sub(
                r"\s+",
                " ",
                pupil_name
            )

            pupil_name = re.sub(
                r'[<>:"/\\|?*]',
                "",
                pupil_name
            )

            pupil_name = pupil_name.strip()


        # ==========================================
        # CLEAN ADMISSION NUMBER
        # ==========================================

        if admission_no:

            admission_no = admission_no.strip()

            admission_no = re.sub(
                r'[<>:"/\\|?*]',
                "",
                admission_no
            )


        # ==========================================
        # CREATE NEW NAME
        # ==========================================

        if pupil_name and admission_no:

            new_filename = (
                f"{pupil_name}_{admission_no}.pdf"
            )

            new_path = os.path.join(
                output_folder,
                new_filename
            )


            # ==========================================
            # HANDLE DUPLICATE NAMES
            # ==========================================

            counter = 1

            while os.path.exists(new_path):

                name, extension = os.path.splitext(
                    new_filename
                )

                new_filename = (
                    f"{name} ({counter}){extension}"
                )

                new_path = os.path.join(
                    output_folder,
                    new_filename
                )

                counter += 1


            # ==========================================
            # COPY PDF WITH NEW NAME
            # ==========================================

            shutil.copy2(
                pdf_filename,
                new_path
            )


            successful.append(
                (
                    pdf_filename,
                    new_filename
                )
            )

            print("\n✅ SUCCESS")
            print(f"   Name       : {pupil_name}")
            print(f"   Admission  : {admission_no}")
            print(f"   New file   : {new_filename}")


        else:

            reason = []

            if not pupil_name:
                reason.append("Pupil name not found")

            if not admission_no:
                reason.append("Admission number not found")

            reason = ", ".join(reason)

            failed.append(
                (
                    pdf_filename,
                    reason
                )
            )

            print(f"\n❌ FAILED: {reason}")


    except Exception as e:

        failed.append(
            (
                pdf_filename,
                str(e)
            )
        )

        print(f"\n❌ ERROR: {e}")


# ==========================================
# CREATE ZIP FILE
# ==========================================

zip_filename = "renamed_pupil_pdfs.zip"

with zipfile.ZipFile(
    zip_filename,
    "w",
    zipfile.ZIP_DEFLATED
) as zip_file:

    for filename in os.listdir(output_folder):

        file_path = os.path.join(
            output_folder,
            filename
        )

        zip_file.write(
            file_path,
            arcname=filename
        )


# ==========================================
# FINAL REPORT
# ==========================================

print("\n")
print("=" * 60)
print("                 FINAL REPORT")
print("=" * 60)

print(f"\n📊 Total files     : {len(uploaded)}")
print(f"✅ Successful      : {len(successful)}")
print(f"❌ Failed          : {len(failed)}")


if failed:

    print("\n❌ FILES THAT NEED ATTENTION:")
    print("-" * 60)

    for filename, reason in failed:

        print(f"• {filename}")
        print(f"  → {reason}")


print("\n📦 ZIP created:")
print(f"   {zip_filename}")

print("\n⬇️ Downloading ZIP...")


# ==========================================
# DOWNLOAD ONLY ONE FILE
# ==========================================

files.download(zip_filename)
