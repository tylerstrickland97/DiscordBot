from cod_api import API
from cod_api import platforms
from dotenv import load_dotenv
import os

"""Class that handles commands related to retrieving Call of Duty statistics"""
class CODHandler():
    def __init__(self):
        """Constructor"""
        load_dotenv()
        self.api = API()
        self.cod_login = os.getenv('COD_LOGIN')
    
    def change_time_format(self, minutes):
        """Changes time from minutes to a string of days, hours, and minutes. Used to make the time played stat look nicer"""
        days = minutes // 1440
        minutes = minutes % 1440
        hours = minutes // 60
        minutes = minutes % 60
        return f'{days} days, {hours} hours, {minutes} minutes'
    
    def get_important_stats(self, results):
        """Retrieves the stats friends care about for all of the call of duty games, if they're present in the retrieved API data."""
        stats = {}
        important_keys = ['kdRatio', 'ekiadRatio', 'accuracy', 'scorePerMinute', 'wlRatio', 'timePlayed']
        stats_keys = ['K/D Ratio', 'EKIA/D Ratio', 'Accuracy', 'SPM', 'W/L Ratio', 'Time Played']

        for key, stat in zip(important_keys, stats_keys):
            if key in results:
                stats[stat] = results[key]
    
        if stats['Time Played']:
            stats['Time Played'] = self.change_time_format(stats['Time Played'])
        return stats
    
    async def get_player_stats(self, game, username):
        """Uses the COD api to retrieve stats for the player with the given username on the given game"""
        await self.api.loginAsync(self.cod_login)
        func = None
    
        if '#' in username:
            platform = platforms.Activision 
        else:
            platform = platforms.XBOX

        if game == 'MW2':
            # MW2 is not supported right now, so if this is the game just send a response saying the stats aren't available at the moment
            # results = await api.ModernWarfare2.combatHistoryAsync(platform, username)
            response = 'Sorry, but I am unable to retrieve stats for MW2 at this time'
            return response
        elif game == 'Vanguard':
            func = self.api.Vanguard.combatHistoryAsync
        elif game == 'ColdWar':
            func = self.api.ColdWar.combatHistoryAsync
        elif game == 'MW2019':
            func= self.api.ModernWarfare.combatHistoryAsync
        elif game == 'Warzone':
            func = self.api.Warzone.combatHistoryAsync
        else:
            return
    
        try:

            results = await func(platform, username)
            stats = self.get_important_stats(results['data']['summary']['all'])
            return self.format_cod_stats(stats, username, game)
        except:
            return f'Sorry, but I wasn\'t able to find stats for **{username}** on **{game}**. Check to make sure there are not any typos in the provided username and that the username is not different on {game}'
    def format_cod_stats(self, stats, player, game):
        """Formats the retrieved stats into a string"""
        response = f'Here\'s what I was able to find for **{player}** on **{game}**\n'

        for stat in stats:
            if not stat == 'Time Played':
                value = f'{stats[stat]:.2f}'
            else:
                value = f'{stats[stat]}'
            response += f'**{stat}**: {value}\n'
    
        return response


    




