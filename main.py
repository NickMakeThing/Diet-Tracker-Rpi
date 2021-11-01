import pickle
import os
import requests
from datetime import datetime
from textract import image_to_data
from data_extraction import get_label_data
from autofocus import autofocus
from loadcell import sense_weight
from time import sleep

def save_response(data, filename):
    with open(filename, 'wb') as handle:
        pickle.dump(data, handle)

last_weight = 9999
while(True):
    weight = sense_weight(last_weight)
    autofocus()
    print('picture taken.')
    response = image_to_data('Label.jpg')
    print('extracting ...')
    nutritional_data = get_label_data(response)
    print(nutritional_data)
    if 'error' not in nutritional_data:
        nutritional_data['date']=str(datetime.now())[:23]
        nutritional_data['weight'] = weight
        print('sending ...')
        response = requests.post('http://3.104.80.43/api/', json=nutritional_data)
        print('response code: ',response.status_code)
        if response.status_code == 200:
            last_weight = weight
    os.rename('Label.jpg','Label_old.jpg')

