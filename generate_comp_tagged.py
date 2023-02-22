from tagger import  feature2id_class
from tagger import feature_statistics_class
import viterbi
from multiprocessing import Pool
import sys
import time
import pandas as pd
import numpy as np
import operator


def run_viterbi1(line):
    histories = []
    words_hist = []  # in some features we have to look at two tags back we create a list
    # just note that curword is going to the last element in the list for example:
    # tag_list=[boy,girl, box] curword=taglist[2]=box

    splited_words = line.split(' ')
    if len(splited_words)<2:
        return '\n'
    splited_words.append('END')
    splited_words=['*','*']+splited_words
    print(splited_words)
    for word_idx in range(len(splited_words)):
        cur_word = splited_words[word_idx]
        #print(cur_word)
        # in this line we get the pair of the word and its tag
        words_hist.append(cur_word)  # we add the current element

        if len(words_hist) > 3:  # the len of words_hist can not be higher than four
            words_hist.pop(0)
        if len(words_hist)==3:
            history = tuple(words_hist)
            histories.append(history)
    pred_tags = viterbi.viterbi(histories, 'trained_weights_data_'+file_path[5]+'.pkl', possilble_tag_list, feature2id_)
    words=splited_words[2:]
    newline=[words[i]+'_'+pred_tags[i] for i in range(len(words)-1)]
    return ' '.join(newline)




fullCmdArguments = sys.argv

# - further arguments
argumentList = fullCmdArguments[1:]
if argumentList[0]=='1' or argumentList[0]=='part1':
    file_path='train1.wtag'
    threshold=2
else:
    file_path = 'train2.wtag'
    threshold=1
s = feature_statistics_class()
s.get_word_tag_pair_count(file_path)
# the class after the cleaning this is the second class
possilble_tag_list = s.possilble_tags
feature2id_ = feature2id_class(s, threshold)
feature2id_.get_word_tag_pairs(file_path)
if __name__ == '__main__':

    with open('comp'+file_path[5]+'.words', 'r') as f:
        with Pool(2) as p:
            possilble_tag_list = s.possilble_tags
            results = list(p.map(run_viterbi1, f.read().split('\n')))
            with open('comp_m'+file_path[5]+'_209146299.wtag', 'w') as file:
                for line in results:
                    file.write(line + '\n')