import discord
from discord.ext import commands
import random

class Responses(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.responses = {
            "<@1284037026672279635>": [
                "what?",
                "what u want bruh?",
                "what bro",
                "why are you pinging me 😭",
                "dude what? im a bot bro why are u pinging me",
                "why is this nigga pinging me, like.. IM JUST A BOT, I DONT HAVE SENTIENCE 😭",
                "why did bro just ping me",
                "did this nigga just ping a bot",
                "bro why am i getting pinged",
                "who the fuck is pinging a bot",
                "nigga did u jus ping me",
                "stop pinging me pls",
                "bro pls dont ping me",
                ":c wat",
                "ooh someone pinged me, i feel wanted",
                "# WHO IN THE FUCK, JUST PINGED ME????",
                "# STOP PINGING ME",
                "bro your literally gonna break my code by pinging me this much.",
                "<@785042666475225109>, help im being pinged, what do i do bro, u didnt code me to deal with this :c",
                "<@785042666475225109> BRO WHAT DO I DO, I CANT DEFEND MYSELF IN THIS SITUATION, U DIDNT CODE ME ENOUGH BITCH",
                "asshole dont ping me bruh",
                "I feel violated with these pings",
                "By the way, my name came from https://open.spotify.com/track/2s6NgzAUgyaqrNTSmzXZgS?si=4def578035e94753",
                "pls stop pinging me"
            ],
            "im gonna finger": [
                "?????",
                "my nigga, what the fuck??",
                "ah HELL NAH",
                "me next?",
                "im gonna finger <@785042666475225109>",
                "bro can i be next",
                "who is fingering who???",
                "bro what yall kno about the fingergeddon"
            ],
            "bend over": [
                "dude what.",
                "nigga what???",
                "aint no way 😭",
                "bend over is wild",
                "im gonna bend u over <@785042666475225109>",
                "im gona bend all of yall over",
                "bro the next person who says bend over, im gonna fucking touch u",
                "bend over n touch your toes and i'll show u where the monster goes"
            ],
            "mommy": [
                "im sorry but did this nigga just say mommy",
                "mommy is genuinely insane bro",
                "😭MOMMY??",
                "BRO SAID MOMMY 💀",
                "im your daddy lil bro.",
                "i thought i was mommy :c, is bro cheating on me now",
                "my nigga jus said mommy 😭",
                "'cant let gang kno i call people on discord mommy' ahh message",
                "bro better delete that 'mommmy' before someone calls him out LMFAO",
                "bro said mommy, chat clip it",
                "screenshotted (im a bot, i cant screenshot shit)",
                "whos my good boy?"
            ],
            "cum": [
                "i am NOT cumming lil bro",
                "did someone jus say cum..",
                "im cumming",
                "😭bro said cum",
                "what is this cum you speak of gang",
                "im cumming on <@785042666475225109>",
                "cum for me <@1256856675520876696>💀",
                "bro if i see even one nigga say cum, i stfg im gonna blow a load",
                "my fav word is cum btw",
                "cum for me"
            ],
            "kms": [
                "Help is (not) available, Speak with someone today (never) at 1-800-273-8255 "
            ],
            "pull the trigger": [
                "whoa what???",
                "bro..",
                "whoa slow down..",
                "nigga what",
                "dont pull the trigger lil bro 😭",
                "bro if u pull that trigger im gonna pull up to <@785042666475225109>'s house",
                "bro why",
                "dont pull the trigger bro 😭",
                "its ok lil bro its just life"
            ],
            "dont care": [
                "no one cares if u care bruh ",
                "bro said dont care 😭 man im hurt",
                "cool nigga",
                "'dont care + didnt ask + ratio' head ahh",
                "you should care tho",
                "bro really dont care fr",
                "damn bro aint care 😭"
            ],
            "kys": [
                "dont say that, they'll prolly actually do it 😭",
                "kys is wild, me personally i wouldnt take that",
                "nigga what",
                "bro jus said kys so casually wtf",
                "bro u wild 😭",
                "KYS?? nigga u good??",
                "dont die bro its not that deep",
                "damn bro wishin death upon niggas now",
                "is bro an opp or wha, why we wishing death upon niggas now 😭"
            ],
            ",cs": [
                "bro what are u tryna clear snipe for",
                "why is bro tryna clear snipe?",
                "what is nigga hiding that needs a fucking cs",
                "im ngl, i dont even wanna kno what this nigga said that made him need to clear snipe",
                "whatchu tryna hide lil bro?",
                "whats this nigga tryna hide hm?",
                "btw <#1286292755693441076> exist"
            ],
            "hersy": [
                "how did bro misspell heresy",
                "can bro even spell😭",
                "nigga said hersy, im dead asf😭",
                "how do you even misspell your own bots name"
            ],
            "type shit": [
                "type shit",
                "type shi"
            ],
            "fe!n": [
                "fin fin fin fin fin fin fin fin fin",
                "JUST COME OUTSIDE, FOR THE NIGHT, TAKE YOUR TIME, GET YOUR LIGHT, JOHNNY DANG, YEA YEA, I BEEN OUT GEEKING, BITCH",
                "# FE!N FE!N FE!N FE!N FE!N FE!N FE!N FE!N FE!N FE!N",
            ],
            "<@785042666475225109>": [
                "why is bro pinging the owner",
                "he's prolly afk or busy",
                "<@785042666475225109> wakey wakey bitch ass nigga",
                "<@785042666475225109> ur being summoned master cheifu",
                "Please don't ping the owner"
            ],
            "<@818507782911164487>": [
                "<@818507782911164487> rise bitch nigga"
            ],
            "pocket pussy": [
                "my nigga, chill",
                "bro what are you talking about",
                "I want a pocket pussy",
                "pocket pussy?? bro what are u saying",
                "stfu bunny"
            ],
            "wanna play with my peepee": [
                "nah",
                "PEEPEE???😭",
                "bro 😭",
                "this nigga said PEEPEE LMFAOO 😭"
            ],
            "gonna put it in your mouth": [
                "im sorry what???",
                "bro, what?? put WHAT exactly in my mouth??",
                "you gay asl nigga",
                "please dont",
                "oh yes please stick it so far down my throat 😩",
                "oh just like that? bet please choke me 😫"
            ],
            "my dick":[
                "ah hell nah nigga u gay as fuck",
                "yea bro your gay as fuck wtf",
                "bro i dont want your dick nigga",
                "fuck up nigga u sound zesty asf",
                "ew",
                "nigga gay",
                "uhm, what?😭"
            ],
            "gun": [
                "https://guns.lol/playfair"
            ],
            "i hate jews": [
                "i hate jews too",
                "hail hitler my nigga",
                "gas em up 😭"
            ],
            "faggot": [
                "nigga you cant say that",
                "chill with the faggot word, its kinda wild",
                "faggot?? WHERE"
            ],
            "jew": [
                "hail hitler",
                "nein",
                "# ERIKAAAA"
            ],
            "balls": [
                "i have ball cancer",
                "imma put my balls in yo mouth gang"
            ],
            "uwu": [
                "My nigga, do you wanna get banned?",
                "# We don't say UwU here.",
                "Nigga, don't say that shit, u gonna get banned",
                "Ew this nigga said uwu 😭",
                "please commit suicide, why would u even say uwu ts so corny and cringe"
            ],
            ",akf": [
                "how do you misspell afk my nigga",
                "bro, its a 3 letter word how do u fuck that up",
                "bro misspelt afk no fucking way",
                "its afk btw",
                "whats akf?"
            ],
            ",satus": [
                "nigga you spelt it wrong",
                "its ,status btw",
                "how do u misspell your own command",
                "wtf is ,satus huh?"
            ],
            ",staus": [
                "is your spelling this bad nigga, u just misspelt your own bots command",
                "yea bro btw its fucking ,status not ,staus u fucking retard",
                "how are u this bad at spelling your own bot command"
            ],
            "<@757355424621133914>": [
                "faggot, <@757355424621133914> you're being summoned dickwad"
            ],
            "yippe": [
                "https://tenor.com/view/yippee-happy-yippee-creature-yippee-meme-yippee-gif-gif-1489386840712152603"
            ],
            "i literally made you": [
                "'i brought u into this world and i will take you out of it' head ass 😭"
            ],
            "stfu": [
                "who is you talkin to like that son",
                "who are you tellin to stfu??",
                "nigga i hope you aint tellin me to stfu",
                "nigga YOU stfu",
                "nah bro, how about you stfu",
                "nah bro tellin a bot to stfu 😭",
                "nigga beefing with a ROBOT 😭"
            ],
            "where the fuck my blunt, where the fuck my cup, where the fuck my reefer": [
                "# HUH HUH HUH HUH HUH HUH, IM SMOKING ON KUSH, HUH HUH HUH HUH HUH HUH, IM SMOKING ON KUSH"
            ]
        }

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return  # Ignore messages from the bot itself

        # Get a random response based on the message content
        for trigger, responses in self.responses.items():
            if trigger in message.content.lower():
                response = random.choice(responses)
                await message.channel.send(response)
                break  # Stop checking after the first match

# Setup function to add the cog to the bot
async def setup(bot):
    await bot.add_cog(Responses(bot))
