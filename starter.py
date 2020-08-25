import requests
import sys
import json
import RiotConsts as Consts

def main():
	# Get Summoner Name
	name = input("Enter Summoner Name: ")

	# Request for summoner info
	r = requests.get(f'{Consts.URL["base"]}/summoner/v{Consts.API_VERSIONS["summoner"]}/summoners/by-name/{name}?api_key={Consts.KEY}')

	if r.status_code != 200:
		print("There was a problem with your request")
		sys.exit()

	summoner_info = r.json()
	summoner_id = summoner_info['id']
	account_id = summoner_info['accountId']

	# Get basic ranked info
	r = requests.get(f'{Consts.URL["base"]}/league/v{Consts.API_VERSIONS["league"]}/entries/by-summoner/{summoner_id}?api_key={Consts.KEY}')

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

	print(summoner_info['name'])
	print(f'{tier} {rank}: {lp} LP')
	print(f'Win Rate: {wr}%')

	# Get matchlist by account id
	r = requests.get(f'{Consts.URL["base"]}/match/v{Consts.API_VERSIONS["match"]}/matchlists/by-account/{Consts.ACCOUNT_ID}?api_key={Consts.KEY}')

	matchlist = r.json()
	gameIds = getGameIds(matchlist)
	print(gameIds)

# Returns all the gameIds of the give matches
def getGameIds(matchlist):
	matches = matchlist['matches']
	gameIds = []

	for match in matches:
		gameIds.append(match['gameId'])
	
	return gameIds

main()