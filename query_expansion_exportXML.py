import sys
import glob
import time
import re
import json
from nltk.stem import PorterStemmer
import pdb
import nltk
from nltk import word_tokenize
import calcul_prob
from decimal import Decimal
from os.path import basename, dirname

if len(sys.argv) > 1:
    # Input File path
    topics_path = sys.argv[1]

output_prefix = "query_expansion_param_"
list_of_file = glob.glob(topics_path)
expansion_dict = '/Users/jeanneluo/UbuntuShare/e_query/globle/ap_cfd_dis5_min10_top20_stp.json'
ps = PorterStemmer()

f = open(expansion_dict, 'r')
expansion_words = json.load(f) #dict
expansion_dict = {}

# ignore the noise
for k, vs in expansion_words.items():
    if(vs):
        expansion_dict[k] = vs

start_time = time.time()

for file in list_of_file:
    lists_topics = []
    lists_num = []
    exp_lists_topics = []

    with open(file) as fp:
        num_val = 0
        for line in fp:
            # Get <num>
            result = re.match(r"<num>\s*Number:\s*(\d+)\s*\n", line)
            if bool(result):
                num_val = int(result.group(1), 10)
                lists_num += [{"num": num_val}]

            # Get <title>
            title_str = ""
            result = re.match(r"<title>\s*Topic:\s*(.*)\n", line)

            if bool(result):
                title_str = result.group(1)

                # Enlever les points(.)
                # Remplacer les gillemets(") et traits(-) et tous les autres avec une espace.
                # Donc les mots comme  U.S.-U.S.S.R. deviendront US USSR
                # To avoid cause error in Indri 5.12
                title_str = title_str.replace(".", "")
                # re.sub(r"[^A-Za-z]+", ' ', title_str) #Just keep english letters.
                # Replace all the non-alphas with space, but keep digits
                title_str = ''.join([(x if x.isalpha() or x.isdigit() else ' ') for x in title_str])
                lists_topics += [{"num": num_val, "title": title_str}]

    title_list = []
    title_exp = []
    for dict in lists_topics:
        title_list += [dict['title']]

    for title_line in title_list:
        tokens = word_tokenize(title_line)   
        length = len(tokens)
        tokens_norm = [ps.stem(t.lower()) for t in tokens if t.isalpha()]
        exp_words_info = []

        key_dic_final = {}
        lamb = 0.5

        for o_query_term in tokens_norm:
            #print(o_query_term)
            for keyword in expansion_dict:
                if(o_query_term == keyword):
                    #print(o_query_term)
                    #print(expansion_dict[keyword])
                    exp_words_info += [expansion_dict[keyword]]
                    #exp_words_info += [(keyword, expansion_dict[keyword])]

        dic_l = calcul_prob.cal_p_left(exp_words_info, tokens_norm)
        dic_r = calcul_prob.cal_p_droit(exp_words_info, tokens_norm)

        for exp_words in exp_words_info:
            for exp_word in exp_words:
                probability = lamb * dic_l[exp_word] + (1 - lamb) * dic_r[exp_word]
                key_dic_final[exp_word] = probability
        #print(key_dic_final)

        exp_str = ''
        for combine in key_dic_final:
            va = str(key_dic_final[combine])
            com_str = ''.join(va + ' ' + combine + ' ')
            exp_str += com_str

        if(exp_str):
            title = "".join('#weight(0.5 #combine (' + title_line + ') 0.5 #weight(' + exp_str + '))')
        else:
            title = "".join('#combine('+title_line+')')
        title_exp += [{"title": title}]

    l = len(lists_num)
    k = 0
    while k < l:
        exp_lists_topics += [{"num": lists_num[k]['num'], "title": title_exp[k]['title']}]
        k += 1


    # Write the Indri query format file
    with open(dirname(topics_path) + "/" + output_prefix + basename(file)[:-4] + ".xml", "w") as fw:
        param = ("<parameters>\n")
        for topic in exp_lists_topics:
            query = (
                    "\t<query>\n"
                    "\t\t<type>indri</type>\n"
                    "\t\t<number>{0}</number>\n"
                    "\t\t<text>\n"
                    "\t\t\t {1} \n"
                    "\t\t</text>\n"
                    "\t</query>\n"
                     )
            param += query.format(topic["num"], topic["title"])
        param += ("\t<memory>1G</memory>\n"
                     "\t<index>./test_output</index>\n"
                     "\t<trecFormat>true</trecFormat>\n"
                     "\t<count>1000</count>\n"
                     "</parameters>")
        fw.writelines(param)
        print(fw)
