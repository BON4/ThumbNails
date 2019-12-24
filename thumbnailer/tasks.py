from celery import shared_task
import time
import os
from zipfile import ZipFile
from PIL import Image
from django.conf import settings


@shared_task
def test_task(x, y):
    time.sleep(5)
    return x + y


@shared_task
def make_thumbnail(file_path, thumbnails=[]):
    os.chdir(settings.IMAGES_DIR)
    print("debug")
    path, file = os.path.split(file_path)
    file_name, ext = os.path.splitext(file)

    zip_file = f"{file_name}.zip"
    results = {"archive_path": f"{settings.MEDIA_URL}images/{zip_file}"}

    try:
        img = Image.open(file_path)
        zipper = ZipFile(zip_file, 'w')
        zipper.write(file)
        os.remove(file_path)
        for w, h in thumbnails:
            img_copy = img.copy()
            img_copy.thumbnail((w, h))
            thumbnail_file = f'{file_name}_{w}x{h}.{ext}'
            img_copy.save(thumbnail_file)
            zipper.write(thumbnail_file)
            os.remove(thumbnail_file)

        img.close()
        zipper.close()
    except IOError as e:
        print(e)

    return results
