#!/home/code/football-tweet-dataset-generator/twitter/bin/python3
"""
Encoding : UTF-8
Author : Niranjana Hegde B S
Python Libraries Used : Tweepy, CSV, Pandas, VaderSentiment
"""

from config import ACCESSTOKEN , ACCESSTOKENSECRET, APIKEY, APISECRETKEY, CSV_FILE_NAME, COLS, HASHTAGS, COUNT
from tweepy import OAuthHandler, API, Cursor
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
from csv import writer, DictReader
import os


#Conect to Twitter API
auth = OAuthHandler(APIKEY, APISECRETKEY)   
auth.set_access_token(ACCESSTOKEN, ACCESSTOKENSECRET)
api = API(auth, wait_on_rate_limit=True)

def check_if_csv_exists(path_to_file):
    """
    Input : Path to CSV file
    Returns : Boolean based on the file existance 
    """
    return True if os.path.exists(path_to_file) else False


def check_if_text_exists(text,path):
    """
    Purpose : To avoid duplicate texts in the dataset
    Input : Path to CSV file and the tweet text
    Returns : Boolean based on the tweet text existance in CSV 
    """
    if check_if_csv_exists(path):
        with open(CSV_FILE_NAME) as csv_file:
            csv_reader = DictReader(csv_file)
            for row in csv_reader:
                if row["Text"] == text:
                    return True
        return False
    else:
        return False

def append_list_as_row(file_name, list_of_elem):
    """
    Purpose : Enter the new scraped Tweet details into CSV as a row
    Input : Path to CSV file, list containing the new row entry.
    Returns : None 
    """
    with open(file_name, 'a+', newline='') as write_obj:
        csv_writer = writer(write_obj)
        csv_writer.writerow(list_of_elem)

def get_recent_id():
    """
    Purpose : To get the recent tweet ID to avoid older tweets from showing up.
    Input : None
    Returns : ID of the recent tweet 
    """
    with open(CSV_FILE_NAME) as csv_file:
        id_reader = DictReader(csv_file)
        lists = [row["ID"] for row in id_reader]
    return max(lists)

def tweepy_cursor(file_status):
    """
    Purpose : API calls to Twitter.
    Input : Boolean value specifying if CSV file exists or not.
    Returns : List of tweets.
    """
    last_id = get_recent_id() if file_status else None
    return [tweet for tweet in Cursor(api.search, q = HASHTAGS, lang = "en",since_id = last_id,  tweet_mode = 'extended').items(COUNT)]

def scrape_and_save():
    """
    Purpose : To make API calls, analyze the tweet and save them to CSV
    Input : None
    Returns : None 
    """
    #Initialise the SentimentAnalyzer from vaderSentiment
    analyzer = SentimentIntensityAnalyzer()
    
    path_to_file = f"{os.getcwd()}/{CSV_FILE_NAME}" 
    flag = check_if_csv_exists(path_to_file)
    tweets = tweepy_cursor(flag)
    
    for tweet in tweets:
        tweet_id = tweet.id
        try:
            text = tweet.retweeted_status.full_text
        except AttributeError:  # Not a Retweet
            text = tweet.full_text
        
        if check_if_text_exists(text,path_to_file):
            continue
        
        polarity = analyzer.polarity_scores(text)

        """
        Picking the right sentiment. Although there is a chance that one of the 
        value between pos,neg and neu is greater than other two,
        if the difference between them is really less, then it would be unjustifiable 
        to class it into one. In such scenario, the tweet text is labelled as 
        neutral.
        """
        if polarity['pos'] >= polarity['neg'] + polarity['neu']:
            sentiment = 'pos'
        elif polarity['neg'] >= polarity['pos'] + polarity['neu']:
            sentiment = 'neg'
        else:
            sentiment = 'neu'
        
        created_at = tweet.created_at
        entry_rows = [tweet_id, text,created_at,sentiment]
        
        flag = check_if_csv_exists(path_to_file)
        if flag :
            append_list_as_row(path_to_file,entry_rows)
        else:
            #Create the CSV.
            first_entry = {"ID":tweet_id,"Text":text,"Created At":created_at,"Sentiment":sentiment}
            CSV = pd.DataFrame(columns = COLS).append(first_entry,ignore_index=True)
            CSV.to_csv(path_to_file,index=False)

scrape_and_save()