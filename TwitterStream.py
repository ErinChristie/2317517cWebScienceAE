from pymongo import MongoClient as Connection
import json
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import datetime
import unittest
import sys

# Establish connection to localhost
connection = Connection('localhost', 27017)
# Connect to MongoDB database 
db = connection.webscienceae
db.myCollection.ensure_index("id", unique=True, dropDups=True)
collection = db.RESTCollection

# Define keywords to use and ensure language is English
keywords = ['megxit', 'meghan', 'harry']
language = ['en']

# API keys and access tokens 
consumer_key = ""
consumer_secret = ""
access_key = ""
access_secret = ""

class StdOutListener(StreamListener):

    def on_data(self, data):
        # Parse Tweet to variable tweet 
        tweet = json.loads(data)
        try: 
            # Try to store data collected in database 
            tweet_id = tweet['id_str']  # Tweet id from Twitter 
            username = tweet['user']['screen_name']  # The username of who wrote the Tweet 
            followers = tweet['user']['followers_count']  # Number of followers the user has
            text = tweet['text']  # The Tweet's text
            hashtags = tweet['entities']['hashtags']  # Any hashtags used 
            created_at = tweet['created_at']  # The timestamp of when the Tweet was created
            language = tweet['lang']  # The language of the Tweet

            # Create a date object using the created_at timestamp so it can be used by MongoDB
            created = datetime.datetime.strptime(created_at, '%a %b %d %H:%M:%S +0000 %Y')
            
            # Initialise the REST API
            # Write to file the followers of each user
            # Write the followers of each user to the file "followers.txt"
            list_of_followers = []

            file = open("followers.txt","a+")
            current_cursor = tweepy.Cursor(api.followers_ids, screen_name=username, count=10)
            current_followers = current_cursor.iterator.next()
            list_of_followers.extend(current_followers)
            next_cursor_id = current_cursor.iterator.next_cursor

            while(next_cursor_id!=0):
                current_cursor = tweepy.Cursor(self.api.followers_ids, screen_name=username, count=10,cursor=next_cursor_id)
                current_followers=current_cursor.iterator.next()
                list_of_followers.extend(current_followers)
                next_cursor_id = current_cursor.iterator.next_cursor
               
            file.write(list_of_followers)
            file.close()  
            # Put all data collected for a single Tweet into a variable
            tweet_data = {'id':tweet_id, 'username':username, 'followers':followers, 'text':text, 'hashtags':hashtags, 'language':language, 'created':created}

            # Store the varibale tweet_data into the database 
            collection.save(tweet_data)

             # Get the full list of followers of a particular user
            list_of_followers=[]

            file = open("user_followers.txt","w")
            current_cursor = tweepy.Cursor(api.followers_ids, screen_name="DailyMirror", count=5000)
            current_followers = current_cursor.iterator.next()
            list_of_followers.extend(current_followers)
            next_cursor_id = current_cursor.iterator.next_cursor

            while(next_cursor_id!=0):
                current_cursor = tweepy.Cursor(self.api.followers_ids, screen_name="DailyMirror", count=5000,cursor=next_cursor_id)
                current_followers=current_cursor.iterator.next()
                list_of_followers.extend(current_followers)
                next_cursor_id = current_cursor.iterator.next_cursor
                #file.write(list_of_followers)

        except:
            print(tweet)

        file.write(list_of_followers)

    # Prints error status if an error occurs 
    def on_error(self, status):
        print (status)
        return True

# Pass in access and authentication information so can use the 
if __name__ == '__main__':
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)

    stream = Stream(auth, l)
    stream.filter(track=keywords, languages=language)