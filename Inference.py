from tagger import  feature2id_class
from tagger import feature_statistics_class
import viterbi
from multiprocessing import Pool
import time
import pandas as pd
import numpy as np
import operator
import getopt, sys

def run_viterbi(line):
    histories = []
    words_hist = []  # in some features we have to look at two tags back we create a list
    true_tags = []
    # just note that curword is going to the last element in the list for example:
    # tag_list=[boy,girl, box] curword=taglist[2]=box

    splited_words = line.split(' ')
    splited_words.append('END_END')
    splited_words=['*_*','*_*']+splited_words
    for word_idx in range(len(splited_words)):
        cur_word, true_tag = splited_words[word_idx].split('_')
        #print(cur_word)
        # in this line we get the pair of the word and its tag
        words_hist.append(cur_word)  # we add the current element
        true_tags.append(true_tag)

        if len(words_hist) > 3:  # the len of words_hist can not be higher than four
            words_hist.pop(0)
        if len(words_hist)==3:
            history = tuple(words_hist)
            histories.append(history)
    pred_tags = viterbi.viterbi(histories, 'trained_weights_data_'+file_path[5]+'.pkl', possilble_tag_list, feature2id_)
    print(len(true_tags),len(pred_tags))
    results=[(true_tags[i+2],pred) for i,pred in enumerate(pred_tags)]
    print(results)
    return results




# read commandline arguments, first
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

    start = time.time()
    with open('test1.wtag') as f:
        with Pool(2) as p:
            possilble_tag_list = s.possilble_tags
            results = list(p.map(run_viterbi, f.read().split('\n')))
            print(time.time() - start)
            # print(results)
            count = 0
            y_true = []
            y_pred = []
            leng = 0
            for result in results:
                leng += len(result)
                for pair in result:
                    if pair[0] == pair[1]:
                        count += 1
                    y_true.append(pair[0])
                    y_pred.append(pair[1])
            print(count / leng)
            y_actu = pd.Series(y_true, name='Actual')
            y_pred = pd.Series(y_pred, name='Predicted')
            df_confusion = pd.crosstab(y_actu, y_pred)
            sums = {}
            print(df_confusion.index, df_confusion.columns)
            for tag in df_confusion.index.values:
                if tag not in df_confusion.columns.values:
                    continue
                sums[tag] = np.sum(df_confusion.loc[:, tag]) - df_confusion.loc[tag, tag]
            top = [a[0] for a in sorted(sums.items(), key=operator.itemgetter(1), reverse=True)[:10]]
            print(df_confusion.loc[top, top])



