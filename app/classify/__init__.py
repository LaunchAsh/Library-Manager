import tensorflow as tf
import string
import pickle
import numpy as np
from keras.utils.data_utils import pad_sequences
from keras.preprocessing.text import Tokenizer

LINK_MODEL = 'app\classify\model.h5'
LINK_TOKENIZER = 'app/classify/tokenizer.pickle'
def clean_text(text ): 
    delete_dict = {sp_character: ''for sp_character in string.punctuation}
    delete_dict[' '] = ' '
    delete_dict['.'] = ' '
    table = str.maketrans(delete_dict)
    text1 = text.translate(table)
    textArr = text1.split()
    text2 = ' '.join([w for w in textArr if (not w.isdigit() and (not w.isdigit() and len(w) > 2))])
    return text2.lower()

def change_result(arr):
    table = {
        0: [1.0, 0.0, 0.0, 0.0, 0.0],
        1: [0.0, 1.0, 0.0, 0.0, 0.0],
        2: [0.0, 0.0, 1.0, 0.0, 0.0],
        3: [0.0, 0.0, 0.0, 1.0, 0.0],
        4: [0.0, 0.0, 0.0, 0.0, 1.0]
    }
    vector = np.array(arr)
    table_values = np.array(list(table.values()))
    result = np.argmax(np.dot(vector, table_values.T))
    return result + 1

def convert_re(arr):
    # Tìm vị trí lớn nhất cuối cùng
    max_idx = np.where(arr == np.max(arr))[1][-1]

    # Tạo mảng kết quả
    result = np.zeros_like(arr)
    result[0, max_idx] = 1
    res = change_result(result)
    return res

def rating_for_comment(comment):
    model = tf.keras.models.load_model(LINK_MODEL)

    with open(LINK_TOKENIZER, 'rb') as f:
        tokenizer = pickle.load(f)
    
    text = clean_text(comment)
    test = tokenizer.texts_to_sequences([text])
    num_test = pad_sequences(test,padding='post',maxlen = 120)
    result = model.predict(num_test)
    result = convert_re(result)
    return result