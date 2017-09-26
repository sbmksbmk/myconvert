import apng
import os
import re
import requests
import sys


# lineUrlParser = 'https://stickershop.line-scdn.net/stickershop/v1/sticker/(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+.png'
# lineUrlParser = 'https://stickershop.line-scdn.net/stickershop/v1/sticker/([0-9])+/android/sticker.png'
lineUrlParser = 'https://stickershop.line-scdn.net/stickershop/v1/sticker/([0-9]+?)/android/sticker.png'

"""
re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', url)


https://stickershop.line-scdn.net/stickershop/v1/sticker/10006222/android/sticker.png;compress=true
https://stickershop.line-scdn.net/stickershop/v1/sticker/10006222/IOS/sticker_animation@2x.png

https://stickershop.line-scdn.net/stickershop/v1/sticker/585876/android/sticker.png;compress=true
https://stickershop.line-scdn.net/stickershop/v1/sticker/585876/ANDROID/sticker.png
"""


def download_data(url=None, file_path=None):
    chunk = 1024
    res = requests.get(url, stream=True)
    if res.status_code == 200:
        try:
            with open(file_path, 'wb') as f:
                for data in res.iter_content(chunk):
                    f.write(data)
        except:
            pass


def get_img_id(url=None):
    if url is None:
        return None
    id_list = []
    res = requests.get(url)
    if res.status_code == 200:
        id_list = re.findall(lineUrlParser, res.content)

    return id_list


"""
def convert_img_url(id_list=None):
    img_list = []
    for i in id_list:
        img_list.append('https://stickershop.line-scdn.net/stickershop/v1/sticker/{}/ANDROID/sticker.png'.format(i))
    return img_list


def convert_aimg_url(id_list):
    img_list = []
    for i in id_list:
        img_list.append('https://stickershop.line-scdn.net/stickershop/v1/sticker/{}/IOS/sticker_animation@2x.png'.format(i))
    return img_list
"""
def convert_img_url(img_id=None):
    return 'https://stickershop.line-scdn.net/stickershop/v1/sticker/{}/ANDROID/sticker.png'.format(img_id)


def convert_aimg_url(img_id=None):
    return 'https://stickershop.line-scdn.net/stickershop/v1/sticker/{}/IOS/sticker_animation@2x.png'.format(img_id)


def main(url=None, animation=False):
    current_path = os.path.abspath('')
    download_path = os.path.join(current_path, 'download')
    if os.path.exists(download_path) is False:
        os.makedirs(download_path)
    id_list = get_img_id(url)
    for img_id in id_list:
        if animation is True:
            url = convert_aimg_url(img_id=img_id)
        else:
            url = convert_img_url(img_id=img_id)
        file_name = '{}.png'.format(img_id)
        file_path = os.path.join(download_path, file_name)
        download_data(url=url, file_path=file_path)
        print("Downloaded {}".format(file_name))


if __name__ == '__main__':
    if len(sys.argv) > 1:
        animation = False
        try:
            if sys.argv[2].lower().startswith('a'):
                animation = True
        except:
            pass
        main(url=sys.argv[1], animation=animation)
