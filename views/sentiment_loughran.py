import csv
import re
import os
from LoughranMcDonald import Load_MasterDIctionary as LM
from views.utils import get_name_of_file


def get_data(doc, lm_dictionary):
    doc = doc.upper()

    vdictionary = {}
    _odata = [0] * 10
    total_syllables = 0
    word_length = 0

    tokens = re.findall('\w+', doc)  # Note that \w+ splits hyphenated words
    print(len(tokens))
    _odata[1] = len(tokens)
    for token in tokens:
        if not token.isdigit() and len(token) > 1 and token in lm_dictionary:
            word_length += len(token)
            if token not in vdictionary:
                vdictionary[token] = 1
            if lm_dictionary[token].positive: _odata[2] += 1
            if lm_dictionary[token].negative: _odata[3] += 1
            if lm_dictionary[token].uncertainty: _odata[4] += 1
            if lm_dictionary[token].litigious: _odata[5] += 1
            if lm_dictionary[token].weak_modal: _odata[6] += 1
            if lm_dictionary[token].moderate_modal: _odata[7] += 1
            if lm_dictionary[token].strong_modal: _odata[8] += 1
            if lm_dictionary[token].constraining: _odata[9] += 1
            total_syllables += lm_dictionary[token].syllables

    return _odata


def get_sentiment_analysis(folder, output_folder):
    MASTER_DICTIONARY_FILE = os.environ.get('MASTER_DICTIONARY_FILE')
    OUTPUT_FIELDS = ['file name', 'number of words', 'positive', 'negative',
                     'uncertainty', 'litigious', 'modal-weak', 'modal moderate',
                     'modal strong', 'constraining']
    lm_dictionary = LM.load_masterdictionary(MASTER_DICTIONARY_FILE, True)

    if os.path.exists(output_folder):
        if not os.path.exists(output_folder):
            return "Output folder doesn't exist"

        if not os.path.exists(folder):
            return "Input folder doesn't exist"

        ff = os.path.join(output_folder, 'sentiment_loughran.csv')
        with open(ff, 'w') as f_out:
            wr = csv.writer(f_out, lineterminator='\n')
            wr.writerow(OUTPUT_FIELDS)

            for file in os.listdir(folder):
                with open(os.path.join(folder, file), 'r', encoding='UTF-8', errors='ignore') as f_in:
                    doc = f_in.read()
                output_data = get_data(doc, lm_dictionary)
                output_data[0] = get_name_of_file(file)
                wr.writerow(output_data)
