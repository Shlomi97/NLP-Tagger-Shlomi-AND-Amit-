import pandas as pd
import numpy as np
from scipy.optimize import fmin_l_bfgs_b
import pickle
import time
import sys

# well first of all we have to discuss how do we we enter teh

# we use the Taylor approximation to calculate e^x
# x is the number


# the following function gets the representation of of data series input
# training input is a single input
def calculate_f_v_product(training_input, v):
    indexes = training_input['B-indexes']
    return sum(v[indexes])  # we return in a nice way v*f(x,y) we use the fact that we sparse vector


# important comment comment in the likelihood function we use as input dataframe of all feature results
# A-histories-all histories, B-indexes- results of indexes for current history
# C-all possible tags.We did it in order to reduce the running time of the training.


# the following function calculates the total empirical counts
# it gets total history, v- dimenison of the weight vectors
# the result is a vector
# the input
def calculate_emprical_counts(all_histories, v_dimension):
    emprical_counts = np.zeros(v_dimension)
    for input_ in all_histories:
        temp = np.zeros(v_dimension)
        index = input_['B-indexes']
        if index == []:
            continue

        temp[index] = 1

        emprical_counts += temp
    return emprical_counts


# The following function get the representation for possible tags
# for given feature ,recall training_input is a single row for just one history
# normalized function return log sum( expontials) and sum (expontials)
def normalization_term_for_input(training_input, v):
    indexes_for_all_tags = training_input['C-All possible indexes']
    normalization_terms_array = np.zeros(len(indexes_for_all_tags))
    for i, inde in enumerate(indexes_for_all_tags):  # we loop over all possible tags for single
        if inde == []:
            normalization_terms_array[i] = 1
        normalization_terms_array[i] = np.exp(np.sum(v[inde]))
    normalization_term = np.sum(normalization_terms_array)
    return np.log(normalization_term), normalization_term, normalization_terms_array


# we calculate the p(y'|xi,v) expression
# the input again is data seires of the current input weights
""""
def probability(normalization_term,v,cur_index):
    indexes_for_all_tags = training_input['C-All possible indexes']
    normalization_term = 0
    for inde in indexes_for_all_tags:
        if inde==[]:
            continue
        normalization_term += np.power(np.exp(1), sum(v[inde]))  # this is  expression e^(v *f(x,y')
    if cur_index==[]:# we deal with a rare case when the vector of feature(cur_index) will will all zeros
        return 1/normalization_term
    return np.power(np.exp(1), sum(v[cur_index]))/normalization_term
"""


# We calculate the expected counf for a single input
# the function returns the a vector
def expected_count_calculate(training_input, v, v_dimension, normalization_term, normalization_terms_array):
    expected_count = np.zeros(v_dimension)
    indexes_for_all_tags = training_input['C-All possible indexes']
    for i, index in enumerate(indexes_for_all_tags):
        if index == []:  # again we deal wiht the case that we empty index( we will have innder product of zeors
            continue
        temp = np.zeros(v_dimension)
        temp[index] = normalization_terms_array[i]
        # temp[index]=temp[index]*np.power(2.71,sum(v[index]))
        expected_count += temp
    if normalization_term == 0:
        return 0
    return expected_count / normalization_term


# The following function calculates the likelihood and the gradient
# The main paramter is the train dataframe which has all histories
def calc_objective_per_iter(w_i, lamda, trainind_data, emprical_counts, w_i_dimension):
    # well first of all we will calculate the empirical counts we can take it out
    # v*f(x,y) f(x,y) is feature representation we have list of indexes
    # so what we just need to do is to
    # we define empty array
    # zero array[indexes]=v[indexes]
    # empirical count we calculate at the begining

    empirical_counts = emprical_counts
    linear_term = np.inner(w_i, emprical_counts)
    regularization = 0.5 * (
                w_i ** 2)  # np.inner(w_i,w_i) it is ||w||^2 this is following the definition of inner product
    normalization_term = 0
    expected_counts = np.zeros(w_i_dimension)

    for input_ in trainind_data:
        log_normed, normed, normed_array = normalization_term_for_input(input_,
                                                                        w_i)  # normalized function return log sum( expontials) and sum (expontials)
        normalization_term += log_normed
        expected_counts += expected_count_calculate(input_, w_i, w_i_dimension, normed, normed_array)

    regularization_grad = lamda * w_i  # this lamda v

    # The function returns the Max Entropy likelihood (objective) and the objective gradien

    likelihood = linear_term - normalization_term - regularization
    grad = empirical_counts - expected_counts - regularization_grad

    return (-1) * likelihood, (-1) * grad


if __name__ == "__main__":
    fullCmdArguments = sys.argv

    # - further arguments
    argumentList = fullCmdArguments[1:]
    if argumentList[0] == '1' or argumentList[0] == 'part1':
        file_path = 'train1.wtag'
        n_total_features = 24923
    else:
        file_path = 'train2.wtag'
        n_total_features = 6343
    start=time.time()

    traindata = pd.read_json('trainig' + file_path[5] + '.json')
    traindata = traindata.T.to_dict().values()  # we convert the dataframe to list of dicts
    traindata = list(traindata)


    emperical_counts = calculate_emprical_counts(traindata, n_total_features)
    print(emperical_counts)
    print('well done')
    lambda_ = 0.1

    # define 'args', that holds the arguments arg_1, arg_2, ... for 'calc_objective_per_iter'
    args = (lambda_, traindata, emperical_counts, n_total_features)
    w_0 = np.zeros(n_total_features, dtype=np.float32)
    # print(calc_objective_per_iter(w_0,lambda_,traindata,emperical_counts,n_total_features))
    print('lets go______________________________________________________________')

    optimal_params = fmin_l_bfgs_b(func=calc_objective_per_iter, x0=w_0, args=args, maxiter=1000, iprint=1, factr=1e10,
                                   maxls=2)
    weights = optimal_params[0]
    print(weights)

    # Now you can save weights using pickle.dump() - 'weights_path' specifies where the weight file will be saved.
    # IMPORTANT - we expect to recieve weights in 'pickle' format, don't use any other format!!
    weights_path = 'trained_weights_data_'+file_path[5]+'.pkl'  # i identifies which dataset this is trained on
    with open(weights_path, 'wb') as f:
        pickle.dump(optimal_params, f)
    print('time:',time.time()-start)