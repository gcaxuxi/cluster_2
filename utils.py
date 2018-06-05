# -*- coding: utf-8 -*-
import pickle

def save_pickle(file_name, input_data):
    with open(file_name, 'wb') as f:
        pickle.dump(input_data, f) 
        
def load_pickle(file_name):
    with open(file_name, 'rb') as f:
        output_data = pickle.load(f)
    return output_data