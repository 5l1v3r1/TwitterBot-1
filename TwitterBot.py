import tweepy
import time
from bs4 import BeautifulSoup
ACCESS_TOKEN = ''
ACCESS_TOKEN_SECRET = ''
CONSUMER_KEY = ''
CONSUMER_SECRET = ''
#Set up keys for API access
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

#read the last tweet so the bot knows not to repeat old tweets
def Get_LastTweet(file):
    file_read = open(file, 'r')
    LastTweet = int(file_read.read().strip())
    file_read.close()
    return LastTweet
#Update the last tweet 
def Set_LastTweet(LastTweet, file):
    file_write = open(file, 'w')
    file_write.write(str(LastTweet))
    file_write.close()
    return
#Grabs all the recent mentions starting at the last known tweet and stores it in "mentions"
LastTweet = Get_LastTweet('LastTweet.txt')
mentions = api.mentions_timeline(LastTweet)

#This function is a webscrapper that grabs the NBA rankings off their website
def NBAStandings(conference):
    from bs4 import BeautifulSoup
    import requests

    link = 'https://www.nba.com/amp/league/standings'
    r = requests.get(link).text
    soup = BeautifulSoup(r, 'html.parser')

    data = []
    #Finds Team Rank, Team Name, and Wins and Losses and adds them to a Temp list which is added to final data
    for tr in soup.find_all('tr'):
        temp = []
        #find Team Ranks
        if 'bs4' in str(type(tr.find('span', {'class': 'rank'}))):
            TeamRank = tr.find('span', {'class': 'rank'})
            temp.append(TeamRank.text)
        #find Team name
        if 'bs4' in str(type(tr.a)):
            TeamName = tr.a.text
            temp.append(str(TeamName).strip())
        #Find Wins
        for td in tr.find_all('td'):
            if 'Wins' in td.text:
                wins = str(td.text).strip()
                temp.append(wins[-2:])
        #Find Losses
        for td in tr.find_all('td', {'class': 'notpinned'}):
            for span in td:
                if 'Losses' in str(span):
                    loss = str(td.text).strip()
                    temp.append(loss[-2:])
        # This was needed because for some of the teams Bs4 was fiding something called 'ns' and adding it with losses, need to find
        #a better way to deal with it
        if 'ns' in temp:
            rm = temp.index('ns')
            del temp[rm]
        data.append(temp)
    #Delete all empty lists from data and stores them in Final
    Final = [ e for e in data if e]
    #Returns top 5 eastern
    if conference == 'east':
        return Final[0:5]
    #Returns top 5 western
    elif conference == 'west':
        return Final[15:20]
#Goes through all the mentions to see if they meet certain criteria for the bot to respond to
#The bot knows when to respond based on mentions and '#'
for mention in mentions:
    Set_LastTweet(mention.id, 'LastTweet.txt')
    #Reply Hello
    if "#hello" in mention.text.lower():
        print('found #hello, replying now...')
        api.update_status('@' + mention.user.screen_name + ' Hello to you too!', mention.id)
    #1B4 Rocks
    if '#1b4' in mention.text.lower():
        api.update_status('@' + mention.user.screen_name + ' 1B4 rocks!!!', mention.id)
    #NBAEast
    if '#nbaeast' in mention.text.lower():
        teams = NBAStandings('east')
        with open('temp.txt', 'w') as f:
            f.write(f'NBA Eastern Conference Standings: \nRank {teams[0][0]} {teams[0][1]} Record: {teams[0][2]}-{teams[0][3]} \nRank {teams[1][0]} {teams[1][1]} Record: {teams[1][2]}-{teams[1][3]} \nRank {teams[2][0]} {teams[2][1]} Record: {teams[2][2]}-{teams[2][3]} \nRank {teams[3][0]} {teams[3][1]} Record: {teams[3][2]}-{teams[3][3]} \nRank {teams[4][0]} {teams[4][1]} Record: {teams[4][2]}-{teams[4][3]}')       
        with open('temp.txt','r') as f:
            api.update_status('@' + mention.user.screen_name + ' ' + f.read(), mention.id)
    #NBAWest
    if '#nbawest' in mention.text.lower():
        teams = NBAStandings('west')
        with open('temp.txt', 'w') as f:
            f.write(f'NBA Western Conference Standings: \nRank {teams[0][0]} {teams[0][1]} Record: {teams[0][2]}-{teams[0][3]} \nRank {teams[1][0]} {teams[1][1]} Record: {teams[1][2]}-{teams[1][3]} \nRank {teams[2][0]} {teams[2][1]} Record: {teams[2][2]}-{teams[2][3]} \nRank {teams[3][0]} {teams[3][1]} Record: {teams[3][2]}-{teams[3][3]} \nRank {teams[4][0]} {teams[4][1]} Record: {teams[4][2]}-{teams[4][3]}')       
        with open('temp.txt','r') as f:
            api.update_status('@' + mention.user.screen_name + ' ' + f.read(), mention.id)
