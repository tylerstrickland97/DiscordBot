from cod_handler import CODHandler
from fantasy_handler import FantasyHandler


class CommandHandler():

    async def handle_cod_commands(self, sender, message_contents):
        bad_response = f'Sorry {sender}, but I cannot properly respond to that command. Use the command "!helpme" to receive a list of commands that I can respond to\n'
        if len(message_contents) < 3:
            return bad_response
        
        game = message_contents[1]
        if game not in self._cods:
            return bad_response
        
        player = " ".join(message_contents[2:])
        stats = await self.cod_handler.get_player_stats(game, player)
        if not stats:
            return bad_response
        return stats

    async def handle_fantasy_commands(self, sender, message_contents):
        bad_response = f'Sorry {sender}, but I cannot properly respond to that command. Use the command "!helpme" to receive a list of commands that I can respond to\n'
        if len(message_contents) < 2:
            return bad_response
        
        if message_contents[1] == 'standings':
            standings = await self.fantasy_handler.get_standings()
            if not standings:
                return bad_response
            else:
                return standings
            
        elif message_contents[1] == 'stats':
            team = ' '.join(message_contents[2:])
            stats = await self.fantasy_handler.get_stats(team)
            if not stats:
                return bad_response
            else:
                return stats
        else:
            return bad_response

    async def handle_help_command(self, sender, message_contents):
        response = f'Hi {sender}, here are all of the possible commands you can give me\n\n'

        for cod in self._cods:
            response += f'**!stats {cod} "activision_id/xbox_gamertag"** -- to view the combat record for a player on {cod}\n'
        
        response += '**!fantasy standings** -- to view the current standings in our fantasy league\n'
        response += '**!fantasy stats "team_name"** -- to see select stats for a specific fantasy team\n'
        response += '**!helpme** -- to see this message again\n' 
        
        return response

    async def handle_commands(self, context):
        message_contents = context.message.content.split(' ')
        sender_mention = context.author.mention
        command = message_contents[0]
        if command == '!stats':
            stats = await self.handle_cod_commands(sender_mention, message_contents)
            return stats
        elif command == '!fantasy':
            response = await self.handle_fantasy_commands(sender_mention, message_contents)
            return response
        elif command == '!helpme':
            response = await self.handle_help_command(sender_mention, message_contents)
            return response

    def __init__(self):
        self.cod_handler = CODHandler()
        self.fantasy_handler = FantasyHandler()
        self._cods = ["MW2", "Vanguard", "ColdWar", "MW2019", "Warzone"]
        pass