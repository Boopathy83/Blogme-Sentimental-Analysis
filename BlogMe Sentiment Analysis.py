# -*- coding: utf-8 -*-
"""
Created on Wed Oct  4 15:04:59 2023

@author: User-02
"""

import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

#Reading the xlsx file

data = pd.read_excel('articles.xlsx')
#Summary of the data
data.describe()

#Summary of the columns
data.info()

#Counting the no of articles per source
data.groupby(['source_id'])['article_id'].count()

#number(sum) of reaction by publisher
data.groupby(['source_id'])['engagement_reaction_count'].sum()

#dropping a column , we dont have to use square brackets to represent a column in drop()
data = data.drop('engagement_comment_plugin_count',axis = 1)

#creating a keyword flag
keyword = 'crash'

#let's create a for loop to isolate the title rows

def keywordflag(keyword):
    length = len(data)
    keyword_flag=[]
    for x in range(0,length):
        heading = data['title'][x]
        try:  # To handle values like null or nan
            if keyword in heading:
                flag = 1
            else:
                flag = 0
        except:
                flag  = 0
        keyword_flag.append(flag)
    return keyword_flag
keywordflag = keywordflag('murder')

# To cross check the result
data['title'][15] # murder keyword found

data['keywordflag'] = pd.Series(keywordflag)

# We will be using 'vader' to the sentimental analysis
# It is used to analyse the sentiments for social media text,reviews etc...

# SentimentIntensityAnalyzer
sent_int = SentimentIntensityAnalyzer()

text = data['title'][19]
sentiment = sent_int.polarity_scores(text)

# Adding a for loop to extract sentiment per title

title_neg_sentiment = []
title_pos_sentiment = []
title_neu_sentiment = []

length = len(data)
for x in range(0,length):
    try:
        text = data['title'][x]
        sent_int = SentimentIntensityAnalyzer()
        sentiment = sent_int.polarity_scores(text)
        neg = sentiment['neg']
        neu = sentiment['neu']
        pos = sentiment['pos']
    except:
        neg = 0
        pos = 0
        neu = 0
    title_neg_sentiment.append(neg)
    title_neu_sentiment.append(neu)
    title_pos_sentiment.append(pos)
    
title_neg_sentiment = pd.Series(title_neg_sentiment)   
title_neu_sentiment = pd.Series(title_neu_sentiment)  
title_pos_sentiment = pd.Series(title_pos_sentiment)  
    
data['title_neg_sentiment'] = title_neg_sentiment
data['title_neu_sentiment'] = title_neu_sentiment
data['title_pos_sentiment'] = title_pos_sentiment

data.to_excel('blogme_clean.xlsx', sheet_name='blogmedata', index = False)






























        