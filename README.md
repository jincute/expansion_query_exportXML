# expansion_query_exportXML

### precondition：
1. expansion_dict file: ap_cfd_dis5_min10_top20_stp.json (expansion dict)
2. query topics file: topics.1-50.txt

### run commands:
#python query_expansion_exportXML.py <path>/topics.1-50.txt
  
### output:
query_expansion_param_topics.1-50.xml

#### remind:
in query_expansion_param_topics.1-50.xml, please set the <index> ... </index> to the path where your index file locates

Normalisation formula:
$P(t_j|Q) = \lambda P_{ML}(t_j|Q) + (1-\lambda)\sum P(t_j|t_i)P_{ML}(t_i|Q)$
