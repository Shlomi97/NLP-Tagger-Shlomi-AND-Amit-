from collections import OrderedDict
import features_functions
import pandas as pd
import sys
import viterbi
import time
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Pool
# Well we will write the description of this file

# The following class counts #of different feature in dictionary form
# The class has many dictionary depend on the number of the different feataures
class feature_statistics_class():
    def __init__(self):

        self.words_tags_count_dict = OrderedDict()  # this is set of feature100
        # we create a list of all possible list which we have
        self.three_last_tags_dict = OrderedDict()  # this is feature f103
        self.two_last_tags_dict = OrderedDict()  # this is feature f104
        self.tags_dict = OrderedDict()  # this is features f105
        self.lastword_current_tag = OrderedDict()
        self.possilble_tags = []
        self.prefix_tag_pairs=OrderedDict()
        self.sufix_tag_pairs=OrderedDict()
    # the following function creates dictionary of word-tag-pair
    def get_word_tag_pair_count(self, file_path):
        with open(file_path) as f:

            for line in f:  # Here we have a separete sentence
                words_hist = []  # in some features we have to look at two tags back we create a list
                tags_hist = []
                # which will have a size at most 3 this is a datastructure of queue first in first out
                # just note that curword is going to the last element in the list for example:
                # tag_list=[boy,girl, box] curword=taglist[2]=box
                splited_words = line.split(' ')
                splited_words[-1] = 'END_END'
                splited_words = ['*_*', '*_*'] + splited_words
                for word_idx in range(len(splited_words)):

                    cur_word, cur_tag = splited_words[word_idx].split(
                        '_')  # in this line we get the pair of the word and its tag
                    words_hist.append(cur_word)  # we add the current element
                    tags_hist.append(cur_tag)  # we add the current word
                    if len(words_hist) > 3:  # the len of words_hist can not be higher than four
                        words_hist.pop(0)
                    if len(tags_hist) > 3:
                        tags_hist.pop(0)

                    if cur_tag not in self.possilble_tags:  # here we create a list of all existing tags in the training set
                        self.possilble_tags.append(cur_tag)

                    # For each feature we check exist and we update the count using ready binary feature functions
                    # this is feature100 word tag feature
                    if (cur_word, cur_tag) not in self.words_tags_count_dict:
                        self.words_tags_count_dict[(cur_word, cur_tag)] = 1
                    else:
                        self.words_tags_count_dict[(cur_word, cur_tag)] += 1
                    low = cur_word
                    suffixes_list = ['s','ies','es','er','est','ly','ward','wise','ed','en','d',"'s","'",'ing','eer',
                                     'ion', 'ity', 'ment', 'ness', 'or', 'sion', 'ship', 'th','able','al','and','ary','ful','ic','ous','ious','less','y','ent']
                    for a in suffixes_list:
                        if low.endswith(a) and cur_word != 'END':
                            if(a,cur_tag) not in self.sufix_tag_pairs :
                                self.sufix_tag_pairs[(a,cur_tag)]=1
                            else:
                                self.sufix_tag_pairs[(a, cur_tag)] += 1
                    prefixes_list = ['un', 'im', 'ante', 'mis', 'in', 'il', 'non', 'anti', 'dis', 'auto', 'de', 'down',
                                     'ir', 'mega',
                                     'mid', 'over', 'out', 'post', 'pre', 'pro', 're', 'semi', 'sub', 'up', 'per', 'de','Un', 'Im', 'Ante', 'Mis', 'In', 'Il', 'Non', 'Anti', 'Dis', 'Auto', 'De', 'Down',
                     'Ir', 'Mega',
                     'Mid', 'Over', 'Out', 'Post', 'Pre', 'Pro', 'Re', 'Semi', 'Sub', 'Up', 'Per', 'De']
                    for a in prefixes_list:
                        if low.startswith(a):
                            if(a,cur_tag) not in self.prefix_tag_pairs:
                                self.prefix_tag_pairs[(a,cur_tag)]=1
                            else:
                                self.prefix_tag_pairs[(a, cur_tag)] += 1
                    if len(words_hist)<3:
                        continue
                    # this is feature 104  look on the two last tags
                    if tuple(tags_hist[1:3]) not in self.two_last_tags_dict:

                        self.two_last_tags_dict[tuple(tags_hist[1:3])] = 1
                    else:
                        self.two_last_tags_dict[tuple(tags_hist[1:3])] += 1

                    # this is feature 103 #we look at the three last tags
                    if tuple(tags_hist) not in self.three_last_tags_dict:

                        self.three_last_tags_dict[tuple(tags_hist)] = 1
                    else:
                        self.three_last_tags_dict[tuple(tags_hist)] += 1

                    # this is feature 105 # we look only on the current tag
                    if cur_tag not in self.tags_dict:  # this is feature 105

                        self.tags_dict[cur_tag] = 1
                    else:
                        self.tags_dict[cur_tag] += 1

                    # this is feature 106 # we look only on the previous word and the current tag
                    if (words_hist[1], cur_tag) not in self.lastword_current_tag:
                        self.lastword_current_tag[(words_hist[1], cur_tag)] = 1
                    else:
                        self.lastword_current_tag[(words_hist[1], cur_tag)] += 1


class feature2id_class():
    def __init__(self, feature_statistics, threshold):
        self.feature_statistics = feature_statistics  # statistics class, for each featue gives empirical counts
        self.threshold = threshold  # feature count threshold - empirical count must be higher than this

        self.n_total_features = 0  # Total number of features accumulated

        # Init all features dictionaries
        self.words_tags_dict = OrderedDict()  # this is a set of features
        self.three_last_tags_dict = OrderedDict()  # this is feature f103
        self.two_last_tags_dict = OrderedDict()  # this is feature f104
        self.tags_dict = OrderedDict()  # this is features f105
        self.lastword_current_tag = OrderedDict()
        self.prefix_tag=OrderedDict()
        self.suffix_tag=OrderedDict()
        # this is list of all feature functions objections which we are going to use
        self.not_tag_features_list = [features_functions.adjective_prefixes,
                                      features_functions.adjective_suffixes_feature, features_functions.CD_feature,
                                      features_functions.Capital_letter, features_functions.noun_prefixes,
                                      features_functions.Plural_Capital,
                                      features_functions.Connector_feature,features_functions.DT_feature,features_functions.Prep_feature,
                                      features_functions.Preposition_feature,features_functions.wdt_feature,features_functions.wp_feature,
                                      features_functions.wps_feature,features_functions.wrb_feature,features_functions.Preps_feature,
                                      features_functions.pos_suffixes_feature,features_functions.md_feature]

    def get_word_tag_pairs(self, file_path):
        with open(file_path) as f:
            for line in f:
                words_hist = []  # in some features we have to look at two tags back we create a list
                tags_hist = []
                splited_words = line.split(' ')
                splited_words[-1]='END_END'
                splited_words=['*_*','*_*']+splited_words

                for word_idx in range(len(splited_words)):
                    cur_word, cur_tag = splited_words[word_idx].split('_')

                    words_hist.append(cur_word)  # we add the current element
                    tags_hist.append(cur_tag)  # we add the current word
                    if len(words_hist) > 3:  # the len of words_hist can not be higher than four
                        words_hist.pop(0)
                    if len(tags_hist) > 3:
                        tags_hist.pop(0)

                    if ((cur_word, cur_tag) not in self.words_tags_dict) \
                            and (self.feature_statistics.words_tags_count_dict[(cur_word, cur_tag)] >= self.threshold):
                        self.words_tags_dict[(cur_word, cur_tag)] = self.n_total_features
                        self.n_total_features += 1

                    if len(tags_hist)<3:
                        continue

                    low = cur_word
                    prefixes_list = ['un', 'im', 'ante', 'mis', 'in', 'il', 'non', 'anti', 'dis', 'auto', 'de', 'down',
                                     'ir', 'mega',
                                     'mid', 'over', 'out', 'post', 'pre', 'pro', 're', 'semi', 'sub', 'up', 'per', 'de','Un', 'Im', 'Ante', 'Mis', 'In', 'Il', 'Non', 'Anti', 'Dis', 'Auto', 'De', 'Down',
                     'Ir', 'Mega',
                     'Mid', 'Over', 'Out', 'Post', 'Pre', 'Pro', 'Re', 'Semi', 'Sub', 'Up', 'Per', 'De']
                    for a in prefixes_list:
                        if low.startswith(a) and ((a,cur_tag) not in self.prefix_tag) and (self.feature_statistics.prefix_tag_pairs[(a,cur_tag)]>=self.threshold):
                            self.prefix_tag[(a,cur_tag)]=self.n_total_features
                            self.n_total_features += 1

                    suffixes_list = ['s','ies','es','er','est','ly','ward','wise','ed','en','d',"'s","'",'ing','eer',
                                     'ion', 'ity', 'ment', 'ness', 'or', 'sion', 'ship', 'th','able','al','and','ary','ful','ic','ous','ious','less','y','ent',]
                    for a in suffixes_list:
                        if low.endswith(a) and (a,cur_tag) not in self.suffix_tag and low != 'END' and (self.feature_statistics.sufix_tag_pairs[(a,cur_tag)]>=self.threshold):
                             self.suffix_tag[(a,cur_tag)]=self.n_total_features
                             self.n_total_features += 1
                    # we enter the contextual features
                    # here we have three followed tags
                    if (tuple(tags_hist) not in self.three_last_tags_dict) \
                            and (self.feature_statistics.three_last_tags_dict[tuple(tags_hist)] >= self.threshold):
                        self.three_last_tags_dict[tuple(tags_hist)] = self.n_total_features
                        self.n_total_features += 1

                    # her we have two followed tags
                    if (tuple(tags_hist[1:3]) not in self.two_last_tags_dict) \
                            and (self.feature_statistics.two_last_tags_dict[tuple(tags_hist[1:3])] >= self.threshold):
                        self.two_last_tags_dict[tuple(tags_hist[1:3])] = self.n_total_features
                        self.n_total_features += 1
                    # one tag
                    if (cur_tag not in self.tags_dict) \
                            and (self.feature_statistics.tags_dict[cur_tag] >= self.threshold):
                        self.tags_dict[cur_tag] = self.n_total_features
                        self.n_total_features += 1
                    # last word current tag
                    if ((words_hist[1], cur_tag) not in self.lastword_current_tag) \
                            and (
                            self.feature_statistics.lastword_current_tag[(words_hist[1], cur_tag)] >= self.threshold):
                        self.lastword_current_tag[(words_hist[1], cur_tag)] = self.n_total_features
                        self.n_total_features += 1

        # Now we create a dictionary for the rest not paired features
        # We create a dictionary of index also for not featured tag
        self.another_features = {}
        # Like for not word-tag pair we create a dictionary which will keep the feature(func object as key)
        # and the value is going to be the index
        for i in range(len(self.not_tag_features_list)):
            feature = self.not_tag_features_list[i]
            self.another_features[feature] = i + self.n_total_features

        self.n_total_features += len(self.not_tag_features_list)


# The following function get as input history tuple of the previous two stage history
# it gets the word_dict features  and another features dictionary -which are features which
# we have created .
def represent_input_with_features(history, feature2id):
    ppword = history[0]
    pword = history[1]
    word = history[2]
    pptag = history[3]
    ptag = history[4]
    ctag = history[5]
    features = []  # this fill which which features we fill with ones

    if (word, ctag) in feature2id.words_tags_dict:  # we do it for all chosen word-tags features
        features.append(feature2id.words_tags_dict[(word, ctag)])

    if (pptag, ptag, ctag) in feature2id.three_last_tags_dict:  # we check appearance in the three following tags
        features.append(feature2id.three_last_tags_dict[(pptag, ptag, ctag)])

    if (ptag, ctag) in feature2id.two_last_tags_dict:
        features.append(feature2id.two_last_tags_dict[(ptag, ctag)])

    if (ctag) in feature2id.tags_dict:
        features.append(feature2id.tags_dict[ctag])

    if (pword, ctag) in feature2id.lastword_current_tag:
        features.append(feature2id.lastword_current_tag[(pword, ctag)])

    low=word
    suffixes_list = ['s', 'ies', 'es', 'er', 'est', 'ly', 'ward', 'wise', 'ed', 'en', 'd', "'s", "'", 'ing', 'eer',
                     'ion', 'ity', 'ment', 'ness', 'or', 'sion', 'ship', 'th', 'able', 'al', 'and', 'ary', 'ful', 'ic',
                     'ous', 'ious', 'less', 'y', 'ent']
    for a in suffixes_list:
        if low.endswith(a):
            if (a, ctag) in feature2id.suffix_tag:
                features.append(feature2id.suffix_tag[(a, ctag)])
    prefixes_list = ['un', 'im', 'ante', 'mis', 'in', 'il', 'non', 'anti', 'dis', 'auto', 'de', 'down',
                     'ir', 'mega',
                     'mid', 'over', 'out', 'post', 'pre', 'pro', 're', 'semi', 'sub', 'up', 'per', 'de','Un', 'Im', 'Ante', 'Mis', 'In', 'Il', 'Non', 'Anti', 'Dis', 'Auto', 'De', 'Down',
                     'Ir', 'Mega',
                     'Mid', 'Over', 'Out', 'Post', 'Pre', 'Pro', 'Re', 'Semi', 'Sub', 'Up', 'Per', 'De']
    for a in prefixes_list:
        if low.startswith(a):
            if (a, ctag) in feature2id.prefix_tag:
                features.append(feature2id.prefix_tag[(a, ctag)])

    for f in feature2id.another_features.keys():
        if f(history) != 0:
            index = feature2id.another_features[f]
            features.append(index)



    return features



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
if __name__ == "__main__":


    print(possilble_tag_list)
    print(len(possilble_tag_list))  # 44 possible tags

    print(feature2id_.n_total_features)
    print('dictionary of index word-pairs')
    print(feature2id_.words_tags_dict)
    print('dictionary of index word-pairs')
    print(feature2id_.another_features)
    histories = []
    indexes_list = []  # this is the
    possible_combination_indexes = []  # for each input we create list of list of indexes for all possible tags

    with open(file_path) as f:
        for line in f:  # Here we have a separate sentence

            words_hist = []  # in some features we have to look at two tags back we create a list
            tags_hist = []  # which will have a size at most 3 this is a data structure of queue first in first out
            # just note that curword is going to the last element in the list for example:
            # tag_list=[boy,girl, box] curword=taglist[2]=box

            splited_words = line.split(' ')
            splited_words[-1] = 'END_END'
            splited_words = ['*_*', '*_*'] + splited_words
            for word_idx in range(len(splited_words)):
                temp_tagging = []
                cur_word, cur_tag = splited_words[word_idx].split('_')
                # in this line we get the pair of the word and its tag
                words_hist.append(cur_word)  # we add the current element
                tags_hist.append(cur_tag)

                if len(words_hist) > 3:  # the len of words_hist can not be higher than four
                    words_hist.pop(0)

                if len(tags_hist) > 3:
                    tags_hist.pop(0)
                if len(words_hist) == 3:
                    history = tuple(words_hist + tags_hist)
                    histories.append(history)
                    indexes_list.append(represent_input_with_features(history, feature2id_))

                    for tag in possilble_tag_list:  # we run over all possible tag assumations
                        temp_history = tuple(words_hist + tags_hist[0:2] + [tag])
                        temp_tagging.append(represent_input_with_features(temp_history, feature2id_))
                    possible_combination_indexes.append(temp_tagging)

    data = {'A-Histories': histories,
            'B-indexes': indexes_list,
            'C-All possible indexes': possible_combination_indexes
            }

    training = pd.DataFrame(data=data)
    training.to_csv('training.csv', index=True)
    training.to_json('trainig'+file_path[5]+'.json')



