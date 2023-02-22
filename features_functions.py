#This file will be used for all function which will help us to count whether the features holds or not
#Each feature function is going to get as input history
#the history is previous-word, current-word, next word " " " for tag


#In may cases when the word begins with capital letter it has NNP
def DT_feature(history):
    curword=history[2]
    curtag=history[5]
    dt=['the','The','a','Another','those','this','any','another','each','an','these','An','Either','every','This','Some','These','Those','Each','Every','THE','Any']
    if curword in dt and curtag=='DT':
        return 1
    else:
        return 0

def Connector_feature(history):
    curword=history[2]
    curtag=history[5]
    connectors_list=['and','or','&','but','nor','et','And','Neither','plus','Or','minus','nor','Nor','AND']
    if curword in connectors_list and curtag=='CC':
        return 1
    else:
        return 0

def Preposition_feature(history):
    curword=history[2]
    curtag=history[5]
    #note that another feature which can be complete is RB
    preposition_list = ['with','in','Among','of','into','by','then','from','for','between','on','after','at','under','as','whether','until','because','over','if','Like','like']
    if curword in preposition_list and curtag == 'IN':#we think if it is a good idea to put so there

        return 1
    else:
        return 0

def Prep_feature(hist):
    curword = hist[2]
    curtag = hist[5]
    curword=curword.lower()
    prp_list=['yourself','me','you','it','em','myself','ourselves','them','one','he','they','we','themselves','she','i','himself','herself','itself','him','us']
    if curword in prp_list and curtag == 'PRP':#we think if it is a good idea to put so there
        return 1
    else:
        return 0

def Preps_feature(hist):
    curword = hist[2]
    curtag = hist[5]
    curword=curword.lower()
    prp_list=['our','your','his','her','their','my','its']
    if curword in prp_list and curtag == 'PRP$':#we think if it is a good idea to put so there
        return 1
    else:
        return 0
def md_feature(hist):
    curword = hist[2]
    curtag = hist[5]
    curword = curword.lower()
    prp_list = ['could','wo','may','should','ca',"'ll",'mighta','shall','ought','would','will','might','must']
    if curword in prp_list and curtag == 'MD':  # we think if it is a good idea to put so there
        return 1
    else:
        return 0

def wp_feature(hist):
    curword = hist[2]
    curtag = hist[5]
    curword=curword.lower()
    prp_list=['who','what','whom']
    if curword in prp_list and curtag == 'WP':#we think if it is a good idea to put so there
        return 1
    else:
        return 0


def wps_feature(hist):
    curword = hist[2]
    curtag = hist[5]
    curword = curword.lower()
    prp_list = ['whose', 'whosoever']
    if curword in prp_list and curtag == 'WP$':  # we think if it is a good idea to put so there
        return 1
    else:
        return 0

def wrb_feature(hist):
    curword = hist[2]
    curtag = hist[5]
    curword = curword.lower()
    prp_list = ['where','when','how','why','whereby']
    if curword in prp_list and curtag == 'WRB':  # we think if it is a good idea to put so there
        return 1
    else:
        return 0

def wdt_feature(hist):
    curword = hist[2]
    curtag = hist[5]
    curword = curword.lower()
    prp_list = ['which','what','that','whatever','whichever']
    if curword in prp_list and curtag == 'WDT':  # we think if it is a good idea to put so there
        return 1
    else:
        return 0

def Capital_letter(hist):
    curword = hist[2]
    curtag = hist[5]
    first_letter=curword[0]
    if first_letter.isupper==True and hist[1] !='*' and curtag=='NNP':
        return  1#we condition on that that the word is not the first word in the sentence
    else:
        return 0

#here we implement the f101 features  which return 1 if the word ends the specific kind of feature

def Plural_Capital(hist):
    curword = hist[2]
    curtag = hist[5]
    first_letter = curword[0]
    if first_letter.isupper == True and hist[1] != '*' and curtag == 'NNPS':
        return 1  # we condition on that that the word is not the first word in the sentence
    else:
        return 0


#this feature returns whether the word end
def adjective_suffixes_feature(hist):
    curword = hist[2]
    curtag = hist[5]
    curword=curword.lower()
    adjective_suffixes=['able','al','and','ary','ful','ic','ous','ious','less','y','ent','ed','en']
    for a in adjective_suffixes:
        if curword.endswith(a) and curtag == 'JJ':
            return 1
    return 0


def noun_suffixes_feature(hist):
    curword = hist[2]
    curtag = hist[5]
    noun_suffixes = ['eer', 'er', 'ion', 'ity', 'ment', 'ness', 'or', 'sion', 'ship', 'th']
    for a in noun_suffixes:
        if curword.endswith(a) and curtag == 'NN':
            return 1
    return 0


def vbg_suffixes_feature(hist):# 23553   meanwhile 23552
    curword = hist[2]
    curtag = hist[5]
    curword = curword.lower()
    vbg_suffixes = ['ing']
    for a in vbg_suffixes:
        if curword.endswith(a) and curtag == 'VBG':
            return 1
    return 0

def pos_suffixes_feature(hist):
    curword=hist[2]
    curtag=hist[5]
    curword = curword.lower()
    vbg_suffixes = ["'s","'"]
    for a in vbg_suffixes:
        if curword.endswith(a) and curtag == 'POS':
            return 1
    return 0

def vbz_suffixes_feature(hist):
    curword=hist[2]
    curtag=hist[5]
    curword = curword.lower()
    vbg_suffixes = ['s','es','ies']
    for a in vbg_suffixes:
        if curword.endswith(a) and curtag == 'VBZ' and not curword.endswith("'s"):
            return 1
    return 0

def vbd_suffixes(hist):   #23553
    curword = hist[2]
    curtag = hist[5]
    curword = curword.lower()
    vcd_suffixes = ['ed','d']
    for a in vcd_suffixes:
        if curword.endswith(a) and curtag == 'VBD':
            return 1
    return 0

def vbn_suffixes(hist):
    curword = hist[2]
    curtag = hist[5]
    curword = curword.lower() #23554
    vcd_suffixes = ['ed','en']
    for a in vcd_suffixes:
        if curword.endswith(a) and curtag == 'VBN':
            return 1
    return 0


def Rb_suffixes(hist):
    curword = hist[2]   #23555
    curtag = hist[5]
    curword = curword.lower()
    rb_suffixes = ['ly','ward','wise']
    for a in rb_suffixes:
        if curword.endswith(a) and curtag == 'RB':
            return 1
    return 0

def Rbs_suffixes(hist):
    curword = hist[2]   #23555
    curtag = hist[5]
    curword = curword.lower()
    rb_suffixes = ['est']
    for a in rb_suffixes:
        if curword.endswith(a) and curtag == 'RBS':
            return 1
    return 0

def Rbr_suffixes(hist):
    curword = hist[2]  #23556
    curtag = hist[5]
    curword = curword.lower()
    rbr_suffixes = ['er']
    for a in rbr_suffixes:
        if curword.endswith(a) and curtag == 'RBR':
            return 1
    return 0


def plural_noun(hist):
    curword = hist[2]
    curtag = hist[5] #23557
    vcd_suffixes = ['s','ies','es']
    curword = curword.lower()
    for a in vcd_suffixes:
        if curword.endswith(a) and curtag == 'NNS':
            return 1
    return 0

#now we go to the f102 features which are the

def adjective_prefixes(hist):
    curword = hist[2]  #23558
    curtag = hist[5]
    curword=curword.lower()
    prefixes_list=['un','im','ante','mis','in','il','non','anti','dis','auto','de','down','ir','mega','mid','over','out','post','pre','pro','re','semi','sub','up']
    for a in prefixes_list:
        if curword.startswith(a) and curtag == 'JJ':
            return 1
    return 0

def noun_prefixes(hist):
    curword = hist[2]  #23558
    curtag = hist[5]
    curword = curword.lower()
    prefixes_list = ['per','non','pro','sub','dis','anti','auto','de','down','il','un','im','in','ir','mid','mis','over','out','post','pre','re','semi','tele','up']
    for a in prefixes_list:
        if curword.startswith(a) and curtag == 'NN':
            return 1
    return 0

def plural_noun_prefixs(hist):
    curword = hist[2]  # 23558
    curtag = hist[5]
    curword = curword.lower()
    prefixes_list = ['per', 'non', 'pro', 'sub','dis','anti','auto','de','down','il','un','im','in','ir','mid','mis','over','out','post','pre','pro','re','semi','tele','up']
    for a in prefixes_list:
        if curword.startswith(a) and curtag == 'NNS':
            return 1
    return 0

def verb_prefixes(hist):
    curword = hist[2]  #23559
    curtag = hist[5]
    curword = curword.lower()
    prefixes_list = ['un','dis','de','out','up','mis','anti','auto','down','il','un','im','in','ir','non','over','re','semi','tele','up']
    for a in prefixes_list:
        if curword.startswith(a) and curtag == 'VB':
            return 1
    return 0

def present_verb_prefixes(hist):
    curword = hist[2]  #23559
    curtag = hist[5]
    curword = curword.lower()
    prefixes_list = ['un','dis','de','out','up','mis','anti','auto','down','il','im','in','ir','non','over','re','semi','tele','up']
    for a in prefixes_list:
        if curword.startswith(a) and curtag == 'VBZ':
            return 1
    return 0

def present_plural_verb_prefixes(hist):
    curword = hist[2]  #23559
    curtag = hist[5]
    curword = curword.lower()
    prefixes_list = ['un','dis','de','out','up','mis','anti','auto','down','il','im','in','ir','non','over','re','semi','tele','up']
    for a in prefixes_list:
        if curword.startswith(a) and curtag == 'VBP':
            return 1
    return 0

def past_verb_prefixes(hist):
    curword = hist[2]  #23559
    curtag = hist[5]
    curword = curword.lower()
    prefixes_list = ['un','dis','de','out','up','mis','anti','auto','down','il','im','in','ir','non','over','re','semi','tele','up']
    for a in prefixes_list:
        if curword.startswith(a) and curtag == 'VBD':
            return 1
    return 0

def past_passive_verb_prefixes(hist):
    curword = hist[2]  #23559
    curtag = hist[5]
    curword = curword.lower()
    prefixes_list = ['un','dis','de','out','up','mis','anti','auto','down','il','im','in','ir','non','over','re','semi','tele','up']
    for a in prefixes_list:
        if curword.startswith(a) and curtag == 'VBN':
            return 1
    return 0
#This feature function is going to be complicated due to the reason that  #23560
#We need to check whether the current string is cd , it can be  float, data and anaother kinds of number
def CD_feature(hist):
     #we deal with case we transfrom 4,000 to 4.000 we do not care about the numbers size
    curword=hist[2]
    curtag=hist[5]

    curword=curword.replace(',','').replace('-','').replace(':','').replace('s','').replace('mid','').replace('\/','')#we do so we can deal with case like 1990s or
    curword=curword.lower()#We also make it lower to small letters
    #We use try and accept do check whether the sting is a cardinal number
    special_numbers=['one','two','three','four','five','six','seven','nine','ten','tweleve','fourty','thousand','million','billion','trillion','p53']
   # special_numbers=['billion','Two','two','three','four','five','million' ,'trillion','Forty','one' ,'One','six','Six' ,'mid-1990s','1980s' ,'p53' ,'seven' ,'eight','Eight','nine','Twelve','1970s',
                     #'08:35:00']

    try:  #we also need check about number as like 4,000
        num=float(curword)
        if  curtag=='CD':

            return 1

    except ValueError:

        if   curtag=='CD' and curword in special_numbers :#in this conditon we deal with another kind
            #of number which are  written in word
            return 1



    return 0






