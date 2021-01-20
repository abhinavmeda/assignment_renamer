import os, io
from google.cloud import vision

from PIL import Image

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'google_api.json'

client = vision.ImageAnnotatorClient()

FOLDER_PATH = '/Users/abhinavmeda/Desktop/problem_sets'
TEMPORARY_FOLDER_PATH = '/Users/abhinavmeda/Desktop/temporary_images_for_app/'


def get_name(image_path):
    file_path = os.path.join(TEMPORARY_FOLDER_PATH, image_path)

    with io.open(file_path, 'rb') as image_file:
        content = image_file.read()
        # print(type(content))
    image = vision.Image(content=content)
    response = client.document_text_detection(image=image)
    actual = response.full_text_annotation.text
    return actual


def change_name():
    assignments = os.listdir(FOLDER_PATH)
    assignments.remove('.DS_Store')
    for picture in assignments:
        im = Image.open(os.path.join(FOLDER_PATH, picture))
        (left, top, right, bottom) = (0, 0, 300, 100)
        img = im.crop((left, top, right, bottom))
        img.show()
        img.save(TEMPORARY_FOLDER_PATH + picture, 'JPEG')
        name = get_name(picture).rstrip("\n")
        name += '.jpg'
        os.rename(os.path.join(FOLDER_PATH, picture),
                  os.path.join(FOLDER_PATH, name))
        os.remove(TEMPORARY_FOLDER_PATH + picture)


if __name__ == '__main__':
    change_name()
