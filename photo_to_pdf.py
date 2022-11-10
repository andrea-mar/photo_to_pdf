import os
import sys
from pathlib import Path
from PIL import Image, UnidentifiedImageError
from zipfile import ZipFile


def main():
    if len(sys.argv) < 3:
        sys.exit(
            "Usage: photo_to_pdf.py <path to folder containing the files to be converted> <name of new pdf document> <[optional] name of zip file>"
        )

    # Get the list of all files and directories in the given directory
    path = Path(sys.argv[1])
    pages = get_files(path)
    # convert the photos in page into one pdf file of the chosed name abd save file on desktop
    new_pdf_doc = convert_to_pdf(pages, sys.argv[2])

    if sys.argv[3]:
        zip_file(new_pdf_doc, sys.argv[3])


def get_files(folder_path):
    images = []
    # get a sorted list of the files and documents in the given folder
    files = sorted(os.listdir(folder_path))
    for file in files:
        try:
            image = Image.open(f"{folder_path}/{file}")
        except UnidentifiedImageError:
            pass
        except IsADirectoryError:
            pass
        else:
            if image.mode == "RGBA":
                image = image.convert("RGB")
            # save the image in the list
            images.append(image)
    return images


def convert_to_pdf(list, file_name, path=os.environ["HOME"] + "/Desktop/"):
    new_pdf_doc = f"{path}{file_name}.pdf"
    if len(list) > 1:
        list[0].save(new_pdf_doc, save_all=True, append_images=list[1:])
    elif len(list) == 1:
        list[0].save(new_pdf_doc)
    else:
        sys.exit("no files to convert")
    return new_pdf_doc


def zip_file(file_path, zip_name):
    zip_file_path = f'{os.environ["HOME"]}/Desktop/{zip_name}.zip'
    with ZipFile(zip_file_path, "w") as zip:
        zip.write(file_path)
    return zip_file_path


if __name__ == "__main__":
    main()
