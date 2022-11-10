from photo_to_pdf import get_files, convert_to_pdf, zip_file
from PIL import Image, ImageDraw
import os
import pytest


# create test directory and store it on desktop
test_dir = "test_photos"
parent_dir = os.path.abspath(os.getcwd())
path = os.path.join(parent_dir, test_dir)
try:
    os.mkdir(path)
except FileExistsError:
    pass

# create new image for tests
image1 = Image.new(mode="RGB", size=(200, 70), color="red")
image2 = Image.new(mode="RGB", size=(200, 70), color="red")

# save the files into a test folder
image1.save(f"{path}/img01.png")
image2.save(f"{path}/img02.png")


def test_get_files_valid_path():
    assert len(get_files(path)) == 2


def test_convert_to_pdf_creates_file():
    assert (
        convert_to_pdf(get_files(path), "test")
        == f'{os.environ["HOME"]}/Desktop/test.pdf'
    )
    os.remove(f'{os.environ["HOME"]}/Desktop/test.pdf')


def test_zip_file():
    assert (
        zip_file(f"{path}/img01.png", "img01")
        == f'{os.environ["HOME"]}/Desktop/img01.zip'
    )
    os.remove(f'{os.environ["HOME"]}/Desktop/img01.zip')


def test_empty_folder():
    os.remove(f"{path}/img01.png")
    os.remove(f"{path}/img02.png")
    with pytest.raises(SystemExit):
        convert_to_pdf(get_files(path), "test")
