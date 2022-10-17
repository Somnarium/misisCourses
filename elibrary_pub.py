import requests
import shutil
import os
from tqdm import tqdm
from PIL import Image


def getpage(s, pagenum):
    while True:
        try:
            page = s.get(f'http://elibrary.misis.ru/plugins/SecView/getDoc.php?id={book}&page={pagenum}&type=large/slow', stream=True)
            break
        except:
            continue
    with open(f'{book}/{pagenum}.jpg', 'wb') as out_file:
        shutil.copyfileobj(page.raw, out_file)
    progress.update(1)
    return Image.open(f'{book}/{pagenum}.jpg')


if __name__ == '__main__':
    login = '1911626'
    password = 'Альберт'
    book = input('Book: ').strip()
    try:
        os.makedirs(f'{book}')
    except:
        pass
    images = list()
    with requests.session() as s:
        s.post('http://elibrary.misis.ru/login.php', data={'username': login, 'password': password, 'redirect': '', 'language': 'ru_UN', 'action': 'login', 'cookieverify': ''})
        _pages = s.get(f'http://elibrary.misis.ru/action.php?kt_path_info=ktcore.SecViewPlugin.actions.document&fDocumentId={book}')
        pages = 0
        for line in _pages.text.split('\n'):
            if '\'PageCount\'' in line:
                pages = int(line.split('\'')[3])
                break
        progress = tqdm(total=pages)
        for i in range(0, pages):
            images.append(getpage(s, i))
    images[0].save(f'{book}.pdf', "PDF", resolution=100.0, save_all=True, append_images=images[1:])

