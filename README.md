# football-tweet-dataset-generator
### The repository code is compatible with Python 3.8 and Ubuntu.
## Before you clone:
 1. Visit and register in https://developer.twitter.com/.
 2. For an application, various access related tokens and keys are generated. Copy them to a file.

## Instructions
1. Clone the repository at the desired directory.
2. Copy the contents of config.py.sample and create a new config.py file. Copy and paste your Twitter API credentials into it and update the hashtags you want to scrap. For more info, follow the instructions mentioned in config.py.sample.
3. Create a virtual environment for the project using below command:<br>
    `virtualenv <virtualenv name of your choice>`
4. Install the dependencies using :<br>
    `pip install -r requirements.txt`
5. Ensure that the dependancies are installed by checking them in the site-packages by below command:<br>
    `ls <your virtualenv name>/lib/python3.8/site-packages/ | grep "vaderSentiment\|pandas\|tweepy"`
6. Move/Copy the "tweet-scrapper" file to /etc/cron.d. If you face "permission denied" error, reset the permissions of /etc/cron.d by using below command:<br>
    `sudo chmod 644 /etc/cron.d`

## To test the working of tweet scraping manually:
1. Ensure that dependencies are installed after creating the virtual environment. Follow Instructions *3* and *4* if required. Also ensure config.py file is created and Instruction *2* is completed.
2. Activate the virtual environment using below command:<br>
    `source <your virtualenv name>/bin/activate`
3. Run the Python Script using :<br>
    `python3 main.py`
    
# Further Reading:
To understand how vaderSentiment and tweepy works, read their documentation and source codes.<br>
vaderSentiment : https://github.com/cjhutto/vaderSentiment<br>
tweepy : https://docs.tweepy.org/en/stable/index.html
