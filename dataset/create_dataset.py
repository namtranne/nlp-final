import nltk
import pandas as pd
from tqdm import tqdm
import re
import itertools
import sys
sys.path.append("..")
from params import MAXLEN, NGRAM

import numpy as np
import time
'''
structure of csv:

index   |      sentence
  0     |   Oracle Application Server được ưa chuộng  
  1     |   Hãng phần mềm doanh nghiệp hàng đầu thế giới 

'''


class CreateDataset():
    def __init__(self, txt_path='../data/samples_sentence.csv', save_path="../data/list_ngrams.npy"):
        self.txt_path = txt_path
        self.alphabets_regex = '^[aAàÀảẢãÃáÁạẠăĂằẰẳẲẵẴắẮặẶâÂầẦẩẨẫẪấẤậẬbBcCdDđĐeEèÈẻẺẽẼéÉẹẸêÊềỀểỂễỄếẾệỆfFgGhHiIìÌỉỈĩĨíÍịỊjJkKlLmMnNoOòÒỏỎõÕóÓọỌôÔồỒổỔỗỖốỐộỘơƠờỜởỞỡỠớỚợỢpPqQrRsStTuUùÙủỦũŨúÚụỤưƯừỪửỬữỮứỨựỰvVwWxXyYỳỲỷỶỹỸýÝỵỴzZ0123456789!"#$%&''()*+,-./:;<=>?@[\]^_`{|}~ ]'
        self.save_path = save_path


    def processing(self):
        batch_size = 1000
        index = 1
        terminate_index = 0
        skip_index = 1
        # read text file
        with open(self.txt_path, 'r') as fn:
            batch = []
            for line in fn:   
                if skip_index <= 18:
                    skip_index+=1
                elif skip_index <= 55:
                    if skip_index==55:
                        skip_index=1
                    else:
                        skip_index +=1
                    continue
                if terminate_index < 36000000:
                    terminate_index+=1
                else:
                    break
                if(len(batch) < batch_size):
                    batch.append(line)
                if(len(batch) == batch_size):
                    print('Create dataset batch: ' + str(index))
                    index+=1
                    batch = [self.preprocessing_data(sentence) for sentence in batch]
                    phrases = itertools.chain.from_iterable(self.extract_phrases(text) for text in batch)
                    phrases = [p.strip() for p in phrases if len(p.split()) > 1]

                    # generate ngrams
                    list_ngrams = []
                    for p in tqdm(phrases):
                        if not re.match(self.alphabets_regex, p.lower()):
                            continue
                        if len(phrases) == 0:
                            continue

                        for ngr in self.gen_ngrams(p, NGRAM):
                            if len(" ".join(ngr)) < MAXLEN:
                                list_ngrams.append(" ".join(ngr))
                    print("DONE extract ngrams, total ngrams: ", len(list_ngrams))

                    # save ngrams
                    self.save_ngrams(list_ngrams, save_path=self.save_path)
                    batch = []
                    time.sleep(0.01)

        print("Done create dataset - ngrams")

    def preprocessing_data(self, row):
        processed = re.sub(
            r'[^aAàÀảẢãÃáÁạẠăĂằẰẳẲẵẴắẮặẶâÂầẦẩẨẫẪấẤậẬbBcCdDđĐeEèÈẻẺẽẼéÉẹẸêÊềỀểỂễỄếẾệỆfFgGhHiIìÌỉỈĩĨíÍịỊjJkKlLmMnNoOòÒỏỎõÕóÓọỌôÔồỒổỔỗỖốỐộỘơƠờỜởỞỡỠớỚợỢpPqQrRsStTuUùÙủỦũŨúÚụỤưƯừỪửỬữỮứỨựỰvVwWxXyYỳỲỷỶỹỸýÝỵỴzZ0123456789!"#$%&''()*+,-./:;<=>?@[\]^_`{|}~ ]',
            "", row)
        return processed


    def extract_phrases(self, text):
        return re.findall(r'\w[\w ]+', text)

    def gen_ngrams(self, text, n=5):
        tokens = text.split()

        if len(tokens) < n:
            return [tokens]

        return nltk.ngrams(text.split(), n)

    def save_ngrams(self, list_ngrams, save_path='ngrams_list.npy'):
        with open(save_path, 'ab') as f:
            np.save(f, list_ngrams)
        print("Saved dataset - ngrams")


if __name__ == "__main__":

    creater = CreateDataset(txt_path='./corpus-full.txt', save_path="./list_ngrams.npy")
    creater.processing()
