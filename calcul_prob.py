import pdb
from decimal import Decimal

def cal_p_droit(exp_words, token_words):
    length = len(token_words)
    uni_list = []
    key_dic_right = {}
    for d in exp_words:
        ###### Calcultate P_droite #######
        sum = 0

        # calculate the entire number for the cooccurancy words
        for key in d:
            k_value = d[key]  # 12, 11
            k_val = int(k_value)
            sum += k_val

        # calculate the cooccurance word probability of droite: key_dic_right[key]
        for key in d:
            if key not in uni_list:
                k_name = key
                uni_list += [k_name]
                k_value = d[key]
                k_val = int(k_value)
                p_tj_ti = k_val / sum
                p_droite = p_tj_ti / length
                #p_droite = Decimal(p_droite).quantize(Decimal('0.000'))
                key_dic_right[k_name] = p_droite

            else:
                re_name = key
                re_value = d[key]
                re_val = int(re_value)
                re_p_tj_ti = re_val / sum
                re_p_droite = re_p_tj_ti / length
                #re_p_droite = Decimal(re_p_droite).quantize(Decimal('0.000'))
                key_dic_right[re_name] = key_dic_right[re_name] + re_p_droite

    return(key_dic_right)

def cal_p_left(exp_words, token_words):
    length = len(token_words)
    key_dic_left = {}
    for d in exp_words:
        i = 0
        for key in d.keys():
            for q in token_words:
                if key == q:
                    i += 1
            pml_tj_in_q = i / length
            key_dic_left[key]=pml_tj_in_q
    return key_dic_left

