from models.trainer import Trainer
from params import alphabets
import numpy as np
import os

if not os.path.exists('./checkpoint'):
  os.mkdir('./checkpoint')

if not os.path.exists('./weights'):
  os.mkdir('./weights')

if not os.path.exists('./log'):
  os.mkdir('./log')

def load_dataset(ngrams_path):
    if not os.path.exists(ngrams_path):
        print("Cannot find ngrams path !!!")
    print("Loading dataset...")
    list_ngrams = []
    with open(ngrams_path, 'rb') as f:
        while True:
          try:
              ngrams = np.load(f)
              list_ngrams.extend(ngrams)
          except OSError:
              # Break the loop when there are no more n-grams to load
              break
        
    print("Num samples of dataset: ", list_ngrams.shape[0])
    print("Loaded dataset!!!")

    return list_ngrams


def training(ngrams_path, resume=False, checkpoint_path="./checkpoint/seq2seq_luong_checkpoint.pth"):
    if not os.path.exists(ngrams_path):
      print("Cannot find ngrams path !!!")
    print("Loading dataset...")
    list_ngrams = []
    index = 1
    line_read = 1
    with open(ngrams_path, 'rb') as f:
        while True:
          try:
            print("Current line: " + str(line_read))
            if(index <= 2):
              list_ngrams.extend(np.load(f))
              index +=1
            elif index <= 5:
              np.load(f)
              if index == 5:
                index=1
              else:
                 index+=1
            line_read+=1
            if(line_read>22000):
               break
          except OSError:
              break
    result_list = np.array([])
    while(len(list_ngrams)>20000000):
      result_list = np.append(result_list, np.array(list_ngrams[-20000000:]))
      list_ngrams = list_ngrams[0:-20000000]
      print("Data loading check...")
    result_list = np.append(result_list, np.array(list_ngrams))
    print("Num samples of dataset: ", result_list.shape[0])
    print("Loaded dataset!!!")
    trainer = Trainer(alphabets, list_ngram=result_list)
    if os.path.isfile(checkpoint_path):
      trainer.load_checkpoint(checkpoint_path)
    trainer.train()
    


if __name__ == '__main__':
    training(ngrams_path="./dataset/list_ngrams.npy")


