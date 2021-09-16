from discord.ext import commands
from random import choice, randint, shuffle
import re
from enum import Enum

import shared
import phasmorpg

class PhasmoTrait():
    def __init__(self, t_name, t_desc, t_dependencies):
        self.trait_name = t_name
        self.trait_desc = t_desc
        self.trait_dependencies = t_dependencies

    def conflict(self, lost_items):
        pass


class PhasmoItems(Enum):
    DOTS_PROJECTOR = 1
    EMF_READER = 2
    FLASHLIGHT = 3
    GHOST_WRITING_BOOK = 4
    SPIRIT_BOX = 5
    UV_LIGHT = 6
    VIDEO_CAMERA = 7
    CANDLE = 8
    CRUCIFIX = 9
    GLOWSTICK = 10
    HEAD_MOUNTED_CAMERA = 11
    LIGHTER = 12
    MOTION_SENSOR = 13
    PARABOLIC_MICROPHONE = 14
    PHOTO_CAMERA = 15
    SALT = 16
    SANITY_PILLS = 17
    SMUDGE_STICKS = 18
    SOUND_SENSOR = 19
    STRONG_FLASHLIGHT = 20
    THERMOMETER = 21
    TRIPOD = 22

class RockPaperScissors(Enum):
    """Small class to handle rps game and emoji names"""
    ROCK = 1
    NEWSPAPER = 2
    SCISSORS = 3

class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def pgame(self, ctx, num_traits:str, num_players:str="4"):
        """Khord gives custom RPG traits for Phasmo"""
        shared.log_command(ctx,f'pgame {num_traits} {num_players}')

        regex_passed_traits = regex_passed_players = None
        regex_passed_traits = re.search("^[1-9]{1}$", num_traits)
        regex_passed_players = re.search("^[1-4]{1}$", num_players)
        if not regex_passed_traits or not regex_passed_players:
            await ctx.send(f"Invalid input. Usage: ;pgame number_of_traits(1-9) [number_of_players](1-4)\n")
        else:
            num_traits = int(num_traits)
            num_players = int(num_players)


            items_copy = phasmorpg.items.copy()
            for i in range(0,num_players):

                message = f"```[PLAYER {i+1}]\n + Traits:\n"

                traits = self.get_traits(num_traits)

                for trait in traits:
                    message += f"\t{trait[0]} --- {trait[1]}\n"

                if ["Forgetful","Lose two random items from the mission"] in traits:
                    message += " + Items Lost:\n"
                    items_lost = self.get_items(items_copy)
                    message += f"\t{items_lost[0]}\n\t{items_lost[1]}\n"

                message += f" + (OPTIONAL) Personality: {self.get_personality()}\n"
                await ctx.send(f"{message}```")

    @commands.command()
    async def scissors(self, ctx):
        """Challenge Khord with scissors"""
        shared.log_command(ctx,'scissors')

        result = self.rps_game(RockPaperScissors.SCISSORS)
        await ctx.send(result)

    @commands.command()
    async def paper(self, ctx):
        """Challenge Khord with paper"""
        shared.log_command(ctx,'paper')

        result = self.rps_game(RockPaperScissors.NEWSPAPER)
        await ctx.send(result)

    @commands.command()
    async def rock(self, ctx):
        """Challenge Khord with rock"""
        shared.log_command(ctx,'rock')

        result = self.rps_game(RockPaperScissors.ROCK)
        await ctx.send(result)


    def get_traits(self, count):
        """Randomizes a copy of traits list, then pops desired amount for pgame"""
        traits = []
        c_copy = phasmorpg.traits.copy()
        shuffle(c_copy)
        for count in range(1, count+1):
            temp_index = randint(0,len(c_copy)-1)
            temp_trait = c_copy.pop(temp_index)
            traits.append(temp_trait)

        return traits

    def get_personality(self):
        """Randomizes a personality for pgame"""
        return choice(phasmorpg.personalities)

    def get_items(self, items_copy):
        """Randomizes 2 items for pgame"""
        items_gotten = []
        for item in range(0, 2):
            temp_index = randint(0,len(phasmorpg.items)-1)
            temp_item = items_copy.pop(temp_index)
            items_gotten.append(temp_item)
        return items_gotten

    def rps_game(self, player_choice):
        player_victory = False
        npc_choice = RockPaperScissors(randint(1,3))

        # Determine if player won
        if ((player_choice == RockPaperScissors.ROCK and npc_choice == RockPaperScissors.SCISSORS) or
            (player_choice == RockPaperScissors.SCISSORS and npc_choice == RockPaperScissors.NEWSPAPER) or
            (player_choice == RockPaperScissors.NEWSPAPER and npc_choice == RockPaperScissors.ROCK)):
            player_victory = True

        # Add player and bot choices to output statement
        outcome_statement = f":{(player_choice.name).lower()}: ***vs*** :{(npc_choice.name).lower()}:\n"

        # Add victory/draw/loss result to output statement
        if player_victory:
            outcome_statement = outcome_statement + "Purely luck, mortal. :white_check_mark:"
        elif not player_victory and player_choice == npc_choice:
            outcome_statement += "Hmm. Interesting. :monkey:"
        else:
            outcome_statement += "As expected from a feeble mind. You lose. :x:"

        return (outcome_statement)