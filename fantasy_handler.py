import requests
import emoji
from dotenv import load_dotenv
import os



class FantasyHandler():
    def __init__(self):
        load_dotenv()
        self.headers = {
            'Connection': os.getenv('FANTASY_HEADER_CONNECTION_VAL'),
            'Accept': os.getenv('FANTASY_HEADER_ACCEPT_VAL'),
            'User-Agent': os.getenv('FANTASY_HEADER_USER_AGENT_VAL'),
        }

        self.cookies = {
            'swid': os.getenv('FANTASY_COOKIE_SWID_VAL'),
            'espn_s2': os.getenv('FANTASY_COOKIE_ESPN_S2_VAL')
        }

        self.fantasy_url = os.getenv('FANTASY_URL')

    def remove_emojis(self, name):
        for char in name:
            if emoji.is_emoji(char):
                name = name.replace(char, "")
            name = name.strip()
        return name

    async def get_standings(self):
        response = requests.get(self.fantasy_url, headers=self.headers, cookies=self.cookies)
        if not response or not response.status_code == 200:
            return 'Unable to retrieve fantasy standings'
        data = response.json()
        teams = data['teams']
        rankings = []
        for team in teams:
            if team['name'] and team['record']['overall']:
                name = team['name']
                record = team['record']['overall']
                rankings.append({name: record})
            else:
                return 'Unable to retrieve fantasy standings'
        rankings = sorted(rankings, key = lambda x: list(x.values())[0]['percentage'], reverse=True)
        return self.format_fantasy_standings(rankings)
    
    async def get_stats(self, requested_team):
        response = requests.get(self.fantasy_url, headers=self.headers, cookies=self.cookies)
        data = response.json()
        teams = data['teams']
    
        found_team = None
        for team in teams:
            if team['name']:
                name = team['name'].strip()
                if name == requested_team:
                    found_team = team
                emoji.replace_emoji

        if not found_team:
            return 'Uh oh! Looks like that team name isn\'t a part of the league. Make sure the name you entered is exactly the same as the name on ESPN (including emojis)'
        elif not found_team['record']['overall']:
            return 'There was a problem retrieving fantasy football stats for that team'

        overall_record = found_team['record']['overall']
        wins = overall_record['wins']
        losses = overall_record['losses']
        points_for = overall_record['pointsFor']
        points_against = overall_record['pointsAgainst']

        stats = [
            {'Record': f'{wins}-{losses}'},
            {'Points For': points_for},
            {'Points Against': points_against}
        ]
        return self.format_fantasy_stats(requested_team, stats)
    

    def format_fantasy_standings(self, standings):
        response = 'Here are the current fantasy football standings\n'

        for s in standings:
            for team, record_info in s.items():
                wins = record_info['wins']
                losses = record_info['losses']
                record = f'{wins}-{losses}'
                response += f'**{team}** {record}\n'
        
        return response
    
    def format_fantasy_stats(self, team, stats):
        response = f'Here are the stats for {team}\n'
        for item in stats:
            for stat, value in item.items():
                response += f'**{stat}**: {value}\n'

        return response


