import os

import pygame
import requests
from gtts import gTTS

from stats import champions_data


def get_statistics(name, token):
    region = 'ru'
    regions = ['na1', 'br1', 'eun1', 'euw1', 'jp1', 'kr', 'la1', 'la2', 'oc1', 'tr1', 'pbe1']
    # headers = {
    #     "Origin": "https://developer.riotgames.com",
    #     "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
    #     "X-Riot-Token": "RGAPI-548630ff-7321-40fc-a0f9-5f532b52bdbb",
    #     "Accept-Language": "ru",
    #     "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/605.1.15 (KHTML, like Gecko) " + \
    #                   "Version/12.0.3 Safari/605.1.15 "
    # }
    headers = {
        "Origin": "https://developer.riotgames.com",
        "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Riot-Token": token,
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) " + \
                      "Chrome/71.0.3578.98 Safari/537.36 "
    }

    url = 'https://' + region + '.api.riotgames.com/lol/summoner/v4/summoners/by-name/' + name
    user_resp = requests.get(url=url, headers=headers)
    reg = 0
    while user_resp.status_code == 404:
        if reg == len(regions):
            phrase = "My son!!! I can not find you among my summoners. You might have inout the wrong name"
            tts = gTTS(phrase, 'en')
            tts.save("advice.mp3")

            pygame.mixer.init()
            pygame.mixer.music.load("advice.mp3")
            pygame.mixer.music.set_volume(1.0)
            pygame.mixer.music.play()
            return
        region = regions[reg]
        url = 'https://' + region + '.api.riotgames.com/lol/summoner/v4/summoners/by-name/' + name
        user_resp = requests.get(url=url, headers=headers)
        reg += 1
    user = user_resp.json()

    url = 'https://' + region + '.api.riotgames.com/lol/match/v4/matchlists/by-account/' + str(user['accountId'])
    matches_resp = requests.get(url=url, headers=headers)
    matches = matches_resp.json()

    url = 'https://' + region + '.api.riotgames.com/lol/match/v4/matches/' + str(matches['matches'][0]['gameId'])
    match_resp = requests.get(url=url, headers=headers)
    match = match_resp.json()

    participant_identities = match['participantIdentities']
    participants = match['participants']

    stats_data = ''

    teams = {}
    my_team = ''

    for i in range(10):
        champions_master_total = 0
        champions_master_current = 0
        team = participants[i]['teamId']
        cur_name = participant_identities[i]['player']['summonerName']
        if cur_name.lower() == name:
            my_team = team
        if 'summonerId' in participant_identities[i]['player'].keys():
            url = 'https://' + region + '.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/' + \
                  str(participant_identities[i]['player']['summonerId'])

            champions_master_resp = requests.get(url=url, headers=headers)
            champions_master = champions_master_resp.json()

            for champion_master in champions_master:
                champions_master_total += champion_master['championPoints']
                if champion_master['championId'] == participants[i]['championId']:
                    champions_master_current = champion_master['championPointsSinceLastLevel']

        champion_name = ''

        for champion in champions_data.champions:
            if int(champion['key']) == participants[i]['championId']:
                champion_name = champion['name']
        print(champion_name)
        if team not in teams.keys():
            teams[team] = {}
            teams[team]['max'] = {}
            teams[team]['max']['name'] = champion_name
            teams[team]['max']['m_points'] = champions_master_total
            teams[team]['min'] = {}
            teams[team]['min']['name'] = champion_name
            teams[team]['min']['m_points'] = champions_master_total
        else:
            if cur_name != name:
                if teams[team]['max']['m_points'] < champions_master_total:
                    teams[team]['max']['name'] = champion_name
                    teams[team]['max']['m_points'] = champions_master_total

                if teams[team]['min']['m_points'] > champions_master_total:
                    teams[team]['min']['name'] = champion_name
                    teams[team]['min']['m_points'] = champions_master_total

        # stats_data_simple = champion_name + ' ' + \
        #               'total mastery point: ' + str(champions_master_total) + ' ' + \
        #               'mastery point for current champions: ' + str(champions_master_current) + ' points\n'
        # stats_data += stats_data_simple
        #
        # tts = gTTS(text=stats_data_simple, lang='en')
        # tts.save(str(i)+".wav")

        # print(i, champion_name, champions_master_total, champions_master_current)

    enemy_team = None
    for k in teams.keys():
        if k != my_team:
            enemy_team = k
    if teams[enemy_team]['max']['m_points'] == 0:
        phrase = "My son!!! Now you have played with bots, sometimes simple start leads to the great actions!!!"
    else:
        phrase = "My son!!!! Be careful of player " + teams[enemy_team]['max']['name'] + "next time, he is the master!"
    phrase += "Next time avoid playing with player " + teams[my_team]['min']['name'] + "! He is the least experienced."
    tts = gTTS(phrase, 'en')
    tts.save("advice.mp3")

    pygame.mixer.init()
    pygame.mixer.music.load("advice.mp3")
    pygame.mixer.music.set_volume(1.0)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pass
    # player.play()
    #
    if os.path.exists("advice.mp3"):
        os.remove("advice.mp3")
    else:
        print("The file does not exist")
    return phrase
    # print(json.dumps(match, sort_keys=True, indent=2, separators=(',', ': ')))


name = 'twelvedavinci'
token = 'RGAPI-548630ff-7321-40fc-a0f9-5f532b52bdbb'
print(get_statistics(name, token))
