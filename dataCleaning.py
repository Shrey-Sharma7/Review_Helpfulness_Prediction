import pandas as pd
import numpy as np


def dataCleaning(file):
    df = pd.read_csv(file)

    mydf = df.loc[:, ['review_rating',
                      'review_text', 'review_helpful_vote']]

    # Convert ratings & votes to int
    mydf.loc[:, 'review_rating'] = mydf.review_rating.str.extract(
        "(.*) out of 5 stars").astype(float).astype(int).values
    mydf.loc[:, 'review_helpful_vote'] = mydf.review_helpful_vote.str.extract(
        "(.*) (?:people|person) found this helpful", expand=False).str.replace('One', '1').str.replace(',', '').fillna(0).astype(float).astype(int).values
    mydf = mydf.fillna('#')

    # Drop reviews with 0 rating and less than 10 words to balance the proportions
    mydf.drop(mydf[(mydf['review_helpful_vote'] == 0) & (
        mydf['review_text'].apply(lambda x:len(x.split())) < 10)].index, inplace=True)

    return mydf
