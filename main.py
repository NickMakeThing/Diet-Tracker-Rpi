import pickle
import os
import requests
from textract import image_to_data
from data_extraction import get_label_data
from autofocus import autofocus

def save_response(data, filename):
    with open(filename, 'wb') as handle:
        pickle.dump(data, handle)
    
autofocus()
response = image_to_data('Label.jpg')
nutritional_data = get_label_data(response)
print(nutritional_data)
if 'error' not in nutritional_data:
    requests.post('http://54.253.49.152/api/', json=nutritional_data)
os.rename('Label.jpg','Label_old.jpg')

#save_response(response, 'response_data')


"""
TODO: 
    add api comm
    add weight sensor stuff
        when does the weight information trigger the photo?
    secure comms with ssl
"""