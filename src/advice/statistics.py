import json
import requests
import os

import champions_data
from io import BytesIO
from gtts import gTTS
import pygame

name = 'idzeti'
token = 'RGAPI-81f68b38-e1fc-4822-977c-b689a3f826e3'


def get_statistics(name, token):
    headers = {
        "Origin": "https://developer.riotgames.com",
        "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Riot-Token": token,
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
    }

    url = 'https://ru.api.riotgames.com/lol/summoner/v4/summoners/by-name/' + name
    user_resp = requests.get(url=url, headers=headers)
    user = user_resp.json()

    url = 'https://ru.api.riotgames.com/lol/match/v4/matchlists/by-account/' + str(user['accountId'])
    matches_resp = requests.get(url=url, headers=headers)
    matches = matches_resp.json()

    url = 'https://ru.api.riotgames.com/lol/match/v4/matches/' + str(matches['matches'][0]['gameId'])
    match_resp = requests.get(url=url, headers=headers)
    match = match_resp.json()

    participantIdentities = match['participantIdentities']
    participants = match['participants']

    stats_data = ''

    teams = {}
    my_team = ''

    for i in range(10):
        url = 'https://ru.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/' + str(
            participantIdentities[i]['player']['summonerId'])

        team = participants[i]['teamId']
        cur_name = participantIdentities[i]['player']['summonerName']
        if cur_name.lower() == name:
            my_team = team

        champions_master_resp = requests.get(url=url, headers=headers)
        champions_master = champions_master_resp.json()
        champions_master_total = 0
        champions_master_current = 0

        for champion_master in champions_master:
            champions_master_total += champion_master['championPoints']
            if champion_master['championId'] == participants[i]['championId']:
                champions_master_current = champion_master['championPointsSinceLastLevel']

        champion_name = ''
        for champion in champions_data.champions:
            if int(champion['key']) == participants[i]['championId']:
                champion_name = champion['name']

        if team not in teams.keys():
            teams[team] = {}
            teams[team]['name'] = champion_name
            teams[team]['m_points'] = champions_master_total
        else:
            if teams[team]['m_points']<champions_master_total:
                teams[team]['name'] = champion_name
                teams[team]['m_points'] = champions_master_total


        # stats_data_simple = champion_name + ' ' + \
        #               'total mastery point: ' + str(champions_master_total) + ' ' + \
        #               'mastery point for current champions: ' + str(champions_master_current) + ' points\n'
        # stats_data += stats_data_simple
        #
        # tts = gTTS(text=stats_data_simple, lang='en')
        # tts.save(str(i)+".wav")

        #print(i, champion_name, champions_master_total, champions_master_current)

    for k in teams.keys():
        if k!=my_team:
            enemy_team = k
    phrase = "My son!!!! Be careful of player "+ teams[enemy_team]['name']+", he is the most experienced!"
    phrase += "And don't worry, player "+teams[my_team]['name']+" will help, he is the most powerful!"
    tts = gTTS(phrase, 'en')
    tts.save("advice.mp3")

    pygame.mixer.init()
    pygame.mixer.music.load("advice.mp3")
    pygame.mixer.music.set_volume(1.0)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy() == True:
        pass
    # player.play()
    #
    if os.path.exists("advice.mp3"):
        os.remove("advice.mp3")
    else:
        print("The file does not exist")
    return phrase
    # print(json.dumps(match, sort_keys=True, indent=2, separators=(',', ': ')))

print(get_statistics(name,token))