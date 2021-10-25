import os
import csv
from tqdm import tqdm
import tweepy
from tweepy import Cursor
import pandas as pd
import time
from datetime import datetime
import nltk


CONSUMER_KEY='p5PNFXTHR9CWXESFsxCKoFPfO'
CONSUMER_SECRET='Nqb0SB0Zhrq8xR5yJNgKVYVzfJaSTzXyVyPyIiCp5jsueSX29Z'
ACCESS_KEY='371269481-bVVsnOibIbRTxqosakp9LsRifwclf1jmYOvmX3pW'
ACCESS_SECRET='eMUGfaUuoCtCtrVhG1pELHZ6YMHergjyUNtD2cUk7i1Mm'


auth=tweepy.OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY,ACCESS_SECRET)

'''
def get_tweets(feature_keywords, num_tweets=100, f_text="extended", retweets="retweeted_status"):

    start_date = "202003010900"  # 03-01-2020 at 9:00 am
    end_date = "202004010900"  # 04-01-2020 at 9:00 am
    api = tweepy.API(auth, wait_on_rate_limit=True)

    fetch_feature_tweets = api.search_full_archive(label="dev", query=feature_keywords, fromDate=start_date, toDate=end_date,
                                                   maxResults=num_tweets)

    # print("...{} tweets downloaded so far".format(len(feat_tweets)))

    all_feat_tweets = []
    for ind, tweet in enumerate(tqdm(fetch_feature_tweets)):
        # start_scrape = time.time()
        status = api.get_status(tweet.id, tweet_mode=f_text)
        if hasattr(status, retweets):
            full_text = status.retweeted_status.full_text.encode("utf-8").lower()
            feat_tweets = [tweet.user.screen_name, full_text, tweet.retweeted_status.user.screen_name,
                           tweet.entities['hashtags'], tweet.created_at, tweet.user.followers_count,
                           tweet.user.friends_count]
            all_feat_tweets.append(feat_tweets)
        else:
            full_text = status.full_text.encode("utf-8").lower()
            feat_tweets = [tweet.user.screen_name, full_text, "no retweet username", tweet.entities['hashtags'],
                           tweet.created_at, tweet.user.followers_count, tweet.user.friends_count]
            all_feat_tweets.append(feat_tweets)

        # end_scrape = time.time()
        # total_scrape_time = round((end_scrape - start_scrape) / 60, 2)
        # print('time taken for scrape is {} minutes'.format(total_scrape_time))

    csv_timestamp = datetime.now().strftime("%m_%d_%Y")
    path = os.getcwd()
    filename = path + '/' + '%s_bpd_feature_data_ethan.csv' % csv_timestamp
    with open(filename, 'w') as firstcsv:
        writer = csv.writer(firstcsv)
        writer.writerow(["username", "tweet", "username_of_retweeter", "hashtag", "tweet created",
                         "number of followers", "# following"])
        writer.writerows(all_feat_tweets)


if __name__ == "__main__":
    f_keywords = "bipolar 1 disorder OR bp1 OR bipolar mania OR bipolar hypomania OR bipolar manic depression OR #bipolar1 OR #bipolar1disorder"
    get_tweets(f_keywords)

features_df = pd.read_csv("10_25_2021_16_50_50_bpd_feature_data_ethan.csv", header=0)
features_df.head()
print(features_df.shape)
print(features_df.tweet[0])
'''
# LABEL DATABASE SCRIPT

def get_label_tweets(label_keywords, num_tweets=100, f_text="extended", retweets="retweeted_status"):

    start_date = "202003010900"  # 03-01-2020 at 9:00 am
    end_date = "202004010900"  # 04-01-2020 at 9:00 am
    api = tweepy.API(auth, wait_on_rate_limit=True)

    fetch_label_tweets = api.search_full_archive(label="dev", query=label_keywords, fromDate=start_date, toDate=end_date,
                                                 maxResults=num_tweets)

    bigram_phrases = ['diagnosed bipolar', 'bipolar diagnosis', 'bipolar diagnosed',
                      'bp diagnosis', 'got diagnosed', 'am diagnosed', 'have bipolar', 'after diagnosed',
                      'diagnosed with', '#bipolar diagnosis', '#bp diagnosis', '#being bipolar',
                      'getting diagnosed']

    trigram_phrases = ['diagnosed with bipolar', 'received bipolar diagnosis', 'with bipolar diagnosed',
                       'bipolar 1 diagnosis',
                       'bp 1 diagnosis', 'i got diagnosed', 'i am diagnosed', 'i have bipolar', 'after he diagnosed',
                       'diagnosed with disorder']

    all_label_tweets = []
    for i, tweet in enumerate(tqdm(fetch_label_tweets)):
        # start_scrape = time.time()
        status = api.get_status(tweet.id, tweet_mode=f_text)
        if hasattr(status, retweets):

            full_text = status.retweeted_status.full_text.lower()
            retweet_username = tweet.retweeted_status.user.screen_name

            nltk_tokens = nltk.word_tokenize(full_text)
            bi_grams = nltk.ngrams(nltk_tokens, 2)
            bigram_labels = [bigram for bigram in bi_grams]
            concat_bigrams = [s1 + " " + s2 for s1, s2 in bigram_labels]

            tri_grams = nltk.ngrams(nltk_tokens, 3)
            trigram_labels = [trigram for trigram in tri_grams]
            concat_trigrams = [s1 + " " + s2 + " " + s3 for s1, s2, s3 in trigram_labels]

            label_bigrams = [lbl for lbl in concat_bigrams if lbl in bigram_phrases]
            label_trigrams = [lbl for lbl in concat_trigrams if lbl in trigram_phrases]
            new_labels = label_bigrams + label_trigrams

            label_tweets = [tweet.user.screen_name, full_text, retweet_username, tweet.entities['hashtags'],
                            tweet.created_at, tweet.user.followers_count, tweet.user.friends_count, new_labels]

            all_label_tweets.append(label_tweets)
        else:
            full_text = status.full_text.lower()
            nltk_tokens = nltk.word_tokenize(full_text)
            bi_grams = nltk.ngrams(nltk_tokens, 2)
            bigram_labels = [bigram for bigram in bi_grams]
            concat_bigrams = [s1 + " " + s2 for s1, s2 in bigram_labels]

            tri_grams = nltk.ngrams(nltk_tokens, 3)
            trigram_labels = [trigram for trigram in tri_grams]
            concat_trigrams = [s1 + " " + s2 + " " + s3 for s1, s2, s3 in trigram_labels]

            label_bigrams = [lbl for lbl in concat_bigrams if lbl in bigram_phrases]
            label_trigrams = [lbl for lbl in concat_trigrams if lbl in trigram_phrases]
            new_labels = label_bigrams + label_trigrams

            label_tweets = [tweet.user.screen_name, full_text, "no retweet username", tweet.entities['hashtags'],
                           tweet.created_at, tweet.user.followers_count, tweet.user.friends_count, new_labels]
            all_label_tweets.append(label_tweets)

        print("...{} tweets downloaded so far".format(len(all_label_tweets)))

        # end_scrape = time.time()
        # total_scrape_time = round((end_scrape - start_scrape) / 60, 2)
        # print('time taken for scrape is {} minutes'.format(total_scrape_time))

    csv_timestamp = datetime.now().strftime("%m_%d_%Y")
    path = os.getcwd()
    fname = path + '/' + 'bpd_label_data_ethan_%s.csv' % csv_timestamp
    with open(fname, 'w', encoding='utf-8') as secondcsv:
        writer = csv.writer(secondcsv)
        writer.writerow(["username", "tweet", "username_of_retweeter", "hashtag", "tweet created",
                         "number of followers", "# following", "label"])
        writer.writerows(all_label_tweets)


if __name__ == "__main__":
    l_keywords = "bipolar 1 diagnosis OR diagnosed with bipolar OR diagnosed with bipolar 1 disorder OR diagnosed bipolar OR #diagnosedbipolar"
    get_label_tweets(l_keywords)

label_df = pd.read_csv("bpd_label_data_ethan_10_25_2021.csv", header=0)
print(label_df.label)
print(label_df.shape)
print(label_df.tweet[0])

