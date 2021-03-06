import requests
import sys
import json
import RiotConsts as Consts
import Key

def main():
	championCodes = generateChampionCodes(Consts.CHAMPION_LIST_URL)

	# Get Summoner Name
	name = input("Enter Summoner Name: ")

	# Request for summoner info
	r = requests.get(f'{Consts.URL["base"]}/summoner/v{Consts.API_VERSIONS["summoner"]}/summoners/by-name/{name}?api_key={Key.KEY}')

	if r.status_code != 200:
		print("There was a problem with your request")
		sys.exit()

	summoner_info = r.json()
	summoner_id = summoner_info['id']
	account_id = summoner_info['accountId']

	# Get basic ranked info
	r = requests.get(f'{Consts.URL["base"]}/league/v{Consts.API_VERSIONS["league"]}/entries/by-summoner/{summoner_id}?api_key={Key.KEY}')

	if r.status_code != 200:
		print("There was a problem with your request")
		sys.exit()

	ranked_info = r.json()
	ranked_solo_info = ranked_info[0]

	if ranked_solo_info['queueType'] == 'RANKED_FLEX_SR':
		ranked_solo_info = r.json()[1]

	tier = ranked_solo_info['tier']
	rank = ranked_solo_info['rank']
	lp = ranked_solo_info['leaguePoints']
	wins = int(ranked_solo_info['wins'])
	losses = int(ranked_solo_info['losses'])
	wr = round((wins / (wins + losses)) * 100)

	print("--------------------------")
	print(summoner_info['name'])
	print(f'{tier} {rank}: {lp} LP')
	print(f'Win Rate: {wr}%')
	print("--------------------------")

	# Get matchlist by account id
	r = requests.get(f'{Consts.URL["base"]}/match/v{Consts.API_VERSIONS["match"]}/matchlists/by-account/{Consts.ACCOUNT_ID}?api_key={Key.KEY}')

	if r.status_code != 200:
		print("There was a problem with your request")
		sys.exit()

	matchlist = r.json()
	gameIds = getGameIds(matchlist)
	game = gameIds[0]

	# Getting game info from the latest match
	r = requests.get(f'{Consts.URL["base"]}/match/v{Consts.API_VERSIONS["match"]}/matches/{game}?api_key={Key.KEY}')

	if r.status_code != 200:
		print("There was a problem with your request")
		sys.exit()

	match = r.json()

	# with open('match.json', 'w') as f:
	# 	json.dump(match, f)
	
	# f.close()

	# game duration in minutes
	gameDuration = int(match['gameDuration']) / 60

	target = getPlayerStats(match, name)
	printMatchStats(target, gameDuration, championCodes)

# Returns all the gameIds of the give matches
def getGameIds(matchlist):
	matches = matchlist['matches']
	gameIds = []

	for match in matches:
		gameIds.append(match['gameId'])
	
	return gameIds

# Returns game stats of the given player
def getPlayerStats(match, name):
	participantIdentities = match['participantIdentities']
	participantNo = 0
	
	# Getting participant number
	for participant in participantIdentities:
		playerInfo = participant['player']
		
		if playerInfo['summonerName'].lower() == name.lower():
			participantNo = participant['participantId']
			break
	
	if participantNo == 0:
		print("Could not find player")


	
	return match['participants'][participantNo - 1]

def printMatchStats(target, gameDuration, championCodes):
	print("Previous Match Stats:")

	stats = target['stats']
	minionsKilled = int(stats['totalMinionsKilled'])
	neutralMinionsKilled = int(stats['neutralMinionsKilled'])
	totalMinionsKilled = minionsKilled + neutralMinionsKilled
	csPerMin = round(totalMinionsKilled / gameDuration, 1)
	damageDealt = int(stats['totalDamageDealtToChampions'])
	goldEarned = int(stats['goldEarned'])
	visionScore = int(stats['visionScore'])
	controlWardsBought = int(stats['visionWardsBoughtInGame'])
	championPlayed = ""

	for champion in championCodes:
		if target['championId'] == int(champion):
			championPlayed = championCodes[champion]
			break

	print(f"Champion: {championPlayed}")
	print(f"CS/Min: {csPerMin}")
	print(f"Damage Dealth: {damageDealt}")
	print(f"Gold Earned: {goldEarned}")
	print(f"Vision Score: {visionScore}")
	print(f"Control Wards Bought: {controlWardsBought}")
	print("--------------------------")

def generateChampionCodes(url):
	with open('champion.json') as jsonFile:
		championData = json.load(jsonFile)
	
	championIds = {}
	championInfo = championData['data']

	for champion in championInfo:
		championIds[championInfo[champion]['key']] = champion
	
	return championIds

main() 