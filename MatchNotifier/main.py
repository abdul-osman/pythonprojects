# Imports needed
import re
from datetime import date
from datetime import timedelta, datetime
import requests
from bs4 import BeautifulSoup
from twilio.rest import Client


# Get today and tomorrow dates,
# Later will use this to check if team is playing tomorrow
today = date.today()
today_formatted = today.strftime("%A %w %B %Y")
tomorrow = today + timedelta(1)
tomorrow_formatted = tomorrow.strftime("%A %w %B %Y")

# Get user's team name

user_team = input("Which team do you support? ").lower()

# Make a html request, and use BeautifulSoup and lxml to parse
result = requests.get(f'https://www.live-footballontv.com/{user_team}-on-tv.html')
content = result.text
soup = BeautifulSoup(content, 'lxml')

# Get next fixture
fixture = soup.find('div', class_='fixture').get_text(strip=True, separator=' ')


# Get the date the team is playing
next_game_date = soup.find('div', class_='fixture-date').get_text()
next_game_date_formatted = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', next_game_date)

if today_formatted == next_game_date_formatted:
  # Get game time
  game_time = soup.find('div', class_='fixture__time').get_text()

  # Get game competition
  game_competition = soup.find('div', class_='fixture__competition').get_text()

  # Get channel name
  game_channel = soup.find('div', class_='fixture__channel').get_text()

  account_sid = ''
  auth_token = ''
  client = Client(account_sid, auth_token)

  
  message = client.messages.create(
    from_='+447588673087',
    body=f'{user_team} is playing today at {game_time}, {game_channel}, {game_competition}',
    to='+447535473535'
  )
  
  print(message.sid)
else: 
  print(f'{user_team} is playing on {next_game_date_formatted}')



















