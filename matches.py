import requests, json
from pprint import pprint
import math

yage_steam_id = '76561197961903009'
reco_steam_id = '76561197992402350'


civ_ratings = {
 'Aztecs':      {'infantry': 8, 'archers': 5, 'calvary': 0, 'monks': 10, 'siege':7},
 'Berbers':     {'infantry': 6, 'archers': 7, 'calvary': 8, 'monks': 6, 'siege':7},
 'Britons':     {'infantry': 6, 'archers': 8, 'calvary': 3, 'monks': 5, 'siege':5},
 'Bulgarians':  {'infantry': 7, 'archers': 4, 'calvary': 8, 'monks': 4, 'siege':8},
 'Burgundians': {'infantry': 1, 'archers': 1, 'calvary': 1, 'monks': 1, 'siege':1},
 'Burmese':     {'infantry': 8, 'archers': 2, 'calvary': 8, 'monks': 9, 'siege':7},
 'Byzantines':  {'infantry': 7, 'archers': 8, 'calvary': 7, 'monks': 8, 'siege':3},
 'Celts':       {'infantry': 8, 'archers': 3, 'calvary': 6, 'monks': 2, 'siege':10},
 'Chinese':     {'infantry': 7, 'archers': 10, 'calvary':6, 'monks': 7, 'siege':6},
'Cumans':      {'infantry': 7, 'archers': 5, 'calvary': 10, 'monks': 4, 'siege':8},
 'Ethiopians':  {'infantry': 6, 'archers': 9, 'calvary': 4, 'monks': 5, 'siege':10},
 'Franks':      {'infantry': 6, 'archers': 2, 'calvary': 9, 'monks': 3, 'siege':7},
 'Goths':       {'infantry': 10,'archers': 5, 'calvary': 6, 'monks': 3, 'siege':6},
 'Huns':        {'infantry': 4, 'archers': 9, 'calvary': 9, 'monks': 4, 'siege':4},
 'Incas':       {'infantry': 8, 'archers': 8, 'calvary': 0, 'monks': 7, 'siege':6},
 'Indians':     {'infantry': 6, 'archers': 7, 'calvary': 8, 'monks': 4, 'siege':6},
 'Italians':    {'infantry': 5, 'archers': 8, 'calvary': 5, 'monks': 8, 'siege':4},
 'Japanese':    {'infantry': 9, 'archers': 7, 'calvary': 6, 'monks': 7, 'siege':6},
 'Khmer':       {'infantry': 3, 'archers': 6, 'calvary': 6, 'monks': 6, 'siege':8},
 'Koreans':     {'infantry': 5, 'archers': 7, 'calvary': 3, 'monks': 4, 'siege':9},
 'Lithuanians': {'infantry': 8, 'archers': 6, 'calvary': 8, 'monks': 9, 'siege':3},
'Magyars':     {'infantry': 7, 'archers': 8, 'calvary': 10, 'monks': 3, 'siege':4},
 'Malay':       {'infantry': 9, 'archers': 7, 'calvary': 3, 'monks': 8, 'siege':7},
 'Malians':     {'infantry': 8, 'archers': 7, 'calvary': 8, 'monks': 7, 'siege':7},
 'Mayans':      {'infantry': 6, 'archers': 10, 'calvary':1, 'monks': 3, 'siege':7},
 'Mongols':     {'infantry': 6, 'archers': 8, 'calvary': 8, 'monks': 2, 'siege':9},
'Persians':    {'infantry': 3, 'archers': 6, 'calvary': 10, 'monks': 2, 'siege':7},
 'Portuguese':  {'infantry': 7, 'archers': 8, 'calvary': 6, 'monks': 7, 'siege':7},
 'Saracens':    {'infantry': 5, 'archers': 8, 'calvary': 7, 'monks': 9, 'siege':7},
 'Sicilians':   {'infantry': 1, 'archers': 1, 'calvary': 1, 'monks': 1, 'siege':1},
 'Slavs':       {'infantry': 9, 'archers': 3, 'calvary': 8, 'monks': 9, 'siege':9},
 'Spanish':     {'infantry': 7, 'archers': 5, 'calvary': 9, 'monks': 9, 'siege':6},
 'Tatars':      {'infantry': 2, 'archers': 7, 'calvary': 8, 'monks': 3, 'siege':7},
 'Teutons':     {'infantry': 7, 'archers': 4, 'calvary': 7, 'monks': 9, 'siege':8},
 'Turks':       {'infantry': 3, 'archers': 7, 'calvary': 8, 'monks': 6, 'siege':7},
 'Vietnamese':  {'infantry': 5, 'archers': 8, 'calvary': 5, 'monks': 6, 'siege':6},
 'Vikings':     {'infantry': 8, 'archers': 6, 'calvary': 4, 'monks': 3, 'siege':7}
} 

def echo_played_civs(steam_id, count=1000):
  civs_url = 'https://aoe2.net/api/strings?game=aoe2de&language=en'

  civs = []

  response = requests.get(civs_url)
  if response.status_code != 200:
    raise Exception(response.text)

  strings = response.json()

  for civ in strings['civ']:
    civs.append(civ['string'])

  print(civs)

  matches = []


  remainder = count
  start = 0
  offset = 0

  while remainder > 0:
    if remainder >= 1000:
      batch_count = 1000
      offset += 1000
      remainder = remainder - 1000
    else:
      batch_count = remainder
      offset += remainder
      remainder = remainder - remainder

    matches_url = 'https://aoe2.net/api/player/matches?game=aoe2de&steam_id={}&count={}&start={}'.format(steam_id, batch_count, start)
    print('fetching', batch_count, 'matches out of', count, 'total', 'starting at match', start)
    response = requests.get(matches_url)
    if response.status_code != 200:
      raise Exception(response.text)
    matches = matches + response.json()
    start = offset

  civs_played = {}
  consecutive_civs_played = {}
  last_civ_played = -1
  same_civ_matches = 1

  for match in matches:
    for player in match['players']:
      if player['steam_id'] == steam_id:
        civ = player['civ']
        if civ is None:
          continue
        if civ in civs_played:
          civs_played[civ] += 1
        else:
          try:
            civs_played[civ] = 1
          except Exception as e:
            print(civs, civ)
        if last_civ_played == civ:
          same_civ_matches += 1
        else:
          if same_civ_matches > 1:
            if last_civ_played in consecutive_civs_played:
              consecutive_civs_played[last_civ_played].append(same_civ_matches)
            else:
              consecutive_civs_played[last_civ_played] = [same_civ_matches]
          same_civ_matches = 1
        last_civ_played = civ




  played_civ_list = [(civ, civs_played[civ]) for civ in civs_played]
  played_civ_list.sort(key=lambda x: x[1], reverse=True)

  for civ in played_civ_list:
      try:
        print(civs[civ[0]], civ[1], end='')
      except:
        print("not found in list", civ[0], civ[1])

      if civ[0] in consecutive_civs_played:
        print("",consecutive_civs_played[civ[0]])
      else:
        print()

  print('total matches', len(matches))


if __name__ == "__main__":
  echo_played_civs(reco_steam_id)
  echo_played_civs(yage_steam_id)
