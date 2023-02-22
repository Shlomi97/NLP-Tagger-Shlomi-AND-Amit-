import tagger
import pickle
import numpy as np


def probability(history,v,feature2id,tag_list):
    cur_index=tagger.represent_input_with_features(history,feature2id)
    if cur_index==[]:# we deal with a rare case when the vector of feature(cur_index) will will all zeros
        return 1
    return np.exp(sum(v[cur_index]))


def viterbi(histories,weights_path,tag_list,feature2id):
    with open(weights_path,'rb') as we:
        tag_dict={}
        for i,tag in enumerate(tag_list):
            tag_dict[tag]=i
        w=pickle.load(we)
        leng=len(tag_list)
        w=w[0]
        pre_pie=np.zeros((leng,leng))
        pre_pie[0][0]=1
        predictions=[]
        calcs=np.zeros((leng,leng,leng))
        pies=np.zeros((leng,leng,leng))
        for k,history in enumerate(histories):
            predictions.append([])
            cur_pie=np.zeros((leng,leng))
            for i,u in enumerate(tag_list):
                predictions[k].append([])
                top_list = pre_pie[:, i]
                top_list = sorted(range(len(top_list)), key=lambda i: top_list[i], reverse=True)[:5]
                for j,v in enumerate(tag_list):
                    for c in top_list:
                        cal=probability(history+(tag_list[c],u,v),w,feature2id,tag_list)
                        calcs[c][i][j]=cal
                        pies[c][i][j]=pre_pie[c][i]*cal

                for c in range(len(tag_list)):
                    """
                    s=np.sum(calcs[c][i])
                    if s>0:
                        pies[c][i]=pies[c][i]/s
                    """
                    pos=[pies[t][i][c] for t in range(len(tag_list))]
                    loc=np.array(pos).argmax()
                    cur_pie[i][c]=pos[loc]
                    predictions[k][i].append(tag_list[loc])
            pre_pie=cur_pie

        i,j=np.unravel_index(pre_pie.argmax(),pre_pie.shape)
        preds=[]
        indlist=np.zeros(len(histories))
        indlist[-1]=j
        indlist[-2]=i
        preds.append(tag_list[j])
        preds.append(tag_list[i])
        for i in range(3,len(histories)+1):
            index1=predictions[-i+2][int(indlist[-i+1])][int(indlist[-i+2])]
            indlist[-i]=tag_dict[index1]
            preds.append(index1)
        preds.reverse()
        return preds




