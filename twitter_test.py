import os
from os.path import join, dirname

import re

from dotenv import load_dotenv
import twitter

# Load environment variables
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

consumer_key = os.environ.get('TWITTER_KEY')
consumer_secret = os.environ.get('TWITTER_SECRET')
access_token_key = os.environ.get('TWITTER_TOKEN')
access_token_secret = os.environ.get('TWITTER_TOKEN_SECRET')


api = twitter.Api(consumer_key=consumer_key,
                  consumer_secret=consumer_secret,
                  #access_token_key=access_token_key,
                  # access_token_secret=access_token_secret,
                  application_only_auth=True)

# print(api.GetUser(screen_name='Mejaisenpai'))                
# re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split()