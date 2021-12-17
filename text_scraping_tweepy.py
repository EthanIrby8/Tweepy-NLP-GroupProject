import os
import csv
from tqdm import tqdm
import tweepy
from tweepy import Cursor
import pandas as pd
import time
from datetime import datetime
import nltk


CONSUMER_KEY=''
CONSUMER_SECRET=''
ACCESS_KEY=''
ACCESS_SECRET=''


auth=tweepy.OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY,ACCESS_SECRET)


def get_tweets(feature_keywords, num_tweets=100, f_text="extended", retweets="retweeted_status"):

    start_date = "201501010900"  # 03-01-2020 at 9:00 am
    end_date = "201502010900"  # 04-01-2020 at 9:00 am
    api = tweepy.API(auth, wait_on_rate_limit=True)

    fetch_feature_tweets = api.search_full_archive(label="dev", query=feature_keywords, fromDate=start_date, toDate=end_date,
                                                   maxResults=num_tweets)

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

        print("...{} tweets downloaded so far".format(len(all_feat_tweets)))
        # end_scrape = time.time()
        # total_scrape_time = round((end_scrape - start_scrape) / 60, 2)
        # print('time taken for scrape is {} minutes'.format(total_scrape_time))

    # csv_timestamp = datetime.now().strftime("%m_%d_%Y")
    path = os.getcwd()
    filename = path + '/' + 'bpd2015data.csv'
    with open(filename, 'w') as bpd2015csv:
        writer = csv.writer(bpd2015csv)
        writer.writerow(["username", "tweet", "username_of_retweeter", "hashtag", "tweet created",
                         "number of followers", "# following"])
        writer.writerows(all_feat_tweets)


if __name__ == "__main__":
    f_keywords = "no bipolar disorder OR i am not bipolar OR never had a manic episode OR never been bipolar OR not bipolar"
    get_tweets(f_keywords)

# features_df = pd.read_csv(".csv", header=0)
# features_df.head()
# print(features_df.shape)
# print(features_df.tweet[0])

# LABEL DATABASE SCRIPT

def get_label_tweets(label_keywords, num_tweets=100, f_text="extended", retweets="retweeted_status"):

    start_date = "201611010900"  # first two scrapes have been done exactly a year apart march 2020 down to march 2019
    end_date = "201612010900"  # 04-01-2020 at 9:00 am
    api = tweepy.API(auth, wait_on_rate_limit=True)

    fetch_label_tweets = api.search_full_archive(label="dev", query=label_keywords, fromDate=start_date, toDate=end_date,
                                                 maxResults=num_tweets)

    bigram_phrases = ['no bipolar', 'no diagnosis', 'not diagnosed',
                      'not bipolar', 'dont bipolar', 'false diagnosis']

    trigram_phrases = ['do not have', 'have not received', 'never been diagnosed',
                       'not diagnosed with', 'did not diagnose', 'i am not', 'never been bipolar']

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

    # csv_timestamp = datetime.now().strftime("%m_%d_%Y")
    path = os.getcwd()
    fname = path + '/' + 'bpd2016labeldata.csv'  # % csv_timestamp
    with open(fname, 'a', encoding='utf-8') as secondcsv:
        writer = csv.writer(secondcsv)
        writer.writerow(["username", "tweet", "username_of_retweeter", "hashtag", "tweet created",
                         "number of followers", "# following", "label"])
        writer.writerows(all_label_tweets)

if __name__ == "__main__":
    l_keywords = "no bipolar diagnosis OR i am not bipolar OR never diagnosed with bipolar OR not diagnosed bipolar OR #nobipolar"
    get_label_tweets(l_keywords)

# label_df = pd.read_csv("bpd_label_data_ethan_10_25_2021.csv", header=0)
# print(label_df.head())
# print(label_df.shape)
# print(label_df.tweet[0])

