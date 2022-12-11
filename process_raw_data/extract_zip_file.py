
import os
from zipfile import ZipFile


directory = 'data'


for filename in os.listdir(directory):
    f = os.path.join(directory, filename)

    with ZipFile(f, 'r') as zip:
        zip.printdir()

        print('Extracting all the files now...')
        zip.extractall('data')
        print('Done!')
