import pandas as pd
import numpy as np
import nltk
import contractions
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer
import re


def dataPreprocessing(df):

    # mydf = df.loc[:, ['review_rating',
    #                   'review_text', 'review_helpful_vote']]
    mydf = df
    # Contractions
    mydf['no_contract'] = mydf['review_text'].apply(
        lambda x: [contractions.fix(word) for word in x.split()])
    mydf['review'] = [' '.join(map(str, l)) for l in mydf['no_contract']]
    mydf['review'] = [' '.join(map(str, l)) for l in mydf['no_contract']]

    # Stopwords Removal
    mydf['review'] = mydf['review'].apply(
        lambda x: re.sub('[^A-Za-z]', ' ', x))
    mydf['review'] = mydf['review'].apply(lambda x: x.lower())
    mydf = mydf.drop(['no_contract'], axis=1)
    mydf['tokens'] = mydf['review'].apply(word_tokenize)
    stop_words = set(stopwords.words('english'))
    mydf['stopwords_removed'] = mydf['tokens'].apply(
        lambda x: [word for word in x if word not in stop_words])

    # Lemmatization
    mydf['lemmatized'] = mydf['stopwords_removed'].apply(
        lambda x: [WordNetLemmatizer().lemmatize(word) for word in x])
    mydf = mydf.drop(['review_text', 'tokens',
                     'stopwords_removed'], axis=1)

    # Return the pandas dataframe
    return mydf
