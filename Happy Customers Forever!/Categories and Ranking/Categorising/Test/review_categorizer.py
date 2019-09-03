from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import KeywordsOptions, Features, EmotionOptions
import spacy
import pandas as pd
import json
from concurrent.futures import ThreadPoolExecutor
from spacy.lemmatizer import Lemmatizer
from spacy.lang.en import LEMMA_INDEX, LEMMA_EXC, LEMMA_RULES


def which_bucket(sentence, nlp):
    # SENTENCE BY SENTENCE
    buckets = {"Account and Cheque": "annual fee pre-close forgery fake fraud minimum balance interest rate cheque bounce", "Hidden Charges": "deduct extra hidden charges debit", "Investment and Loan": "policy investment loans stocks funds", "Customer Service": "support response person delay slow documents time",
                   "Online and Mobile Services": "online netbanking internet banking mobile", "Branch Issues": "branch ambiance location staff facility time cleanliness dirty"}
    max_sim = 0
    for bucket in buckets:
        sim = nlp(sentence).similarity(nlp(buckets[bucket]))
        if sim > 0.6 and sim > max_sim:
            max_sim = sim
            category = bucket
    if max_sim:
        return category
    else:
        return None


def lemmatize(sent, nlp):
    lemmatized = []
    lemmatizer = Lemmatizer(LEMMA_INDEX, LEMMA_EXC, LEMMA_RULES)
    doc = nlp(str(sent))
    for token in doc:
        i = lemmatizer(str(token), token.pos_)
        # print(i)
        lemmatized.append(i[0])
    return ' '.join(lemmatized)


def review_categorizer(filename):
    nlp = spacy.load("en_core_web_lg")

    bucket = {'Account and Cheque': [], 'Hidden Charges': [], 'Investment and Loan': [],
              'Customer Service': [], 'Online and Mobile Service': [], 'Branch Issues': []}
    df1 = df2 = df3 = df4 = df5 = df6 = pd.DataFrame(
         columns=["Bank name", "Customer name", "Issue Type", "Review", "Review_Lemma", "Keyword", "Recency", "Place", "Sentiment", "joy", "sadness", "fear", "disgust", "anger"])
    connection = {'Account and Cheque': df1, 'Hidden Charges': df2, 'Investment and Loan': df3,
                  'Customer Service': df4, 'Online and Mobile Service': df5, 'Branch Issues': df6}

    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2018-11-16',
        iam_apikey='LOqcUDy1uNJZZLdvbrXwY5pKfRebfECrI0NtHKy2o-Hq',
        url='https://gateway-lon.watsonplatform.net/natural-language-understanding/api')

    df = pd.read_csv(filename, delimiter="|", encoding="ISO-8859-1")

    def extract(filename, row):
        bank_name = row["Bank"]
        reviews = row["Review"]
        itype = row["Issue Type"]
        uname = row["Name"]
        place = row["Place"]
        #bank_name = row["Hotel Name"]
        recency = row["Date"]
        for sent in nlp(str(reviews)).sents:
            sent_lemma = lemmatize(sent, nlp)
            try:
                response = natural_language_understanding.analyze(
                    text=str(sent_lemma),
                    features=Features(keywords=KeywordsOptions(sentiment=True, limit=10))).get_result()
            except Exception as e:
                #print(e,sent_lemma)
                print("some error with ibm nlu?")
                continue
            for i in response["keywords"]:
                keyword = i["text"]
                sentiment = i["sentiment"]["score"]
                if sentiment >= 0:  # Skip sentences which have positive sentiment
                    continue
                category = which_bucket(keyword, nlp)
                # and (not connection[category]["Review"].str.contains(sent).any()):
                if category:
                    try:
                        response_emo = natural_language_understanding.analyze(
                        text=str(sent_lemma),
                        features=Features(emotion=EmotionOptions(targets=[keyword]))).get_result()
                        joy = response_emo["emotion"]["targets"][0]["emotion"]["joy"]
                        sadness = response_emo["emotion"]["targets"][0]["emotion"]["sadness"]
                        anger = response_emo["emotion"]["targets"][0]["emotion"]["anger"]
                        disgust = response_emo["emotion"]["targets"][0]["emotion"]["disgust"]
                        fear = response_emo["emotion"]["targets"][0]["emotion"]["fear"]
                    except:
                        print("some nlu error")
                    try:
                        print("done")
                        connection[category] = connection[category].append({"Bank name": bank_name, "Customer name": uname, "Issue type":itype,  "Review": str(sent), "Review_Lemma": sent_lemma, "Keyword": keyword, "Sentiment": sentiment,
                                                                             "Recency": recency, "Place":place, "joy": joy, "sadness": sadness, "anger": anger, "disgust": disgust, "fear": fear}, ignore_index=True)
                    except:
                        # print("Error")
                        print("not written to the dataframes")
                        pass

    # Multi-Threading to make it faster
    with ThreadPoolExecutor(max_workers=4) as executor:
        for index, row in df.iterrows():
            executor.submit(extract(filename, row))

    for con in connection:
        connection[con].drop_duplicates(subset="Review_Lemma",
                                        keep='first', inplace=True)
        connection[con].to_csv(str(con)+".csv", sep='|')



review_categorizer("bank_example.csv")
