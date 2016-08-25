# try NLP processing of some columns
# e.g. use NLP to find word associations w/ high or low cost, e.g. surgery

from sklearn.feature_extraction import DictVectorizer

def vectorize_group(p_group):
    "vectorize group"
#   ma = []
#   for k,v in p_group['median'].iteritems():
#       ma.append({'provider':k, 'cost':v})
    ma = [{'provider':k, 'cost':v} \
           for k,v in p_group['median'].iteritems()]
    print('ma', ma)
    vec = DictVectorizer()
    ar = vec.fit_transform(ma).toarray()
    print('\nar', ar)   # note it's unit matrix w/ Y cost values
# to do:
# -for non-aggregate data, input into LogisticRegression or SVC ?
# -Dict, Hash, CountVectorizer on provider words?
#  split provider words into tokens, assign values to tokens
#    e.g. just take tokens, add cost for each => surgery * 8 expensive costs
#         or maybe split cost evenly between tokens => surgery still expensive
# -add State or Zipcode (Zip is actually categorical, not numerical order)


