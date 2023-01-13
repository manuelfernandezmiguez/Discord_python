import discord
import os # default module
import wavelink
from dotenv import load_dotenv
import pymongo
from discord import FFmpegPCMAudio
from math import sqrt
import pprint
import moduloEmbed

client = pymongo.MongoClient("mongodb://localhost:27017")
db = client["brawl-starts_liga"]
mycollection = db["partidos"]
mycollection2 = db["equipos"]
one_record = mycollection.find_one()

load_dotenv() # load all the variables from the env file
bot = discord.Bot()


@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")

@bot.slash_command(name = "hello", description = "Say hello to the bot")
async def hello(ctx):
    await ctx.respond("Son chumano, non me silencies!")

@bot.slash_command(name = "partido", description = "Devolve o primeiro partido(exemplo)")
async def hello(ctx):
    await ctx.respond(f"{one_record} éche o primeiro partido recollido")

testing_servers=[218047836539846657]

@bot.user_command(name="Account Creation Date", guild_ids='testing_servers')  # create a user command for the supplied guilds
async def account_creation_date(ctx, member: discord.Member):  # user commands return the member
    await ctx.respond(f"{member.name}'s account was created on {member.created_at}")


@bot.command()
async def hello2(ctx):
    embed = discord.Embed(
        title="Comandos dispoñibles do ChumanoBot",
        description="Un embed no que se explican todos os comandos.",
        color=discord.Colour.dark_gold, # Pycord provides a class with default colors you can choose from
    )
    embed.add_field(name="record", value="Graba as voces dos diferentes usuarios conectados na mesma canle de voz ** Formato: .wav **")

    embed.add_field(name="Inline Field 1", value="Inline Field 1", inline=True)
    embed.add_field(name="Inline Field 2", value="Inline Field 2", inline=True)
    embed.add_field(name="Inline Field 3", value="Inline Field 3", inline=True)
 
    embed.set_footer(text="Footer! No markdown here.") # footers can have icons too
    embed.set_author(name="Pycord Team", icon_url="https://example.com/link-to-my-image.png")
    embed.set_thumbnail(url="https://example.com/link-to-my-thumbnail.png")
    embed.set_image(url="https://example.com/link-to-my-banner.png")

    
 
    await ctx.respond("Hello! Here's a cool embed.", embed=embed) # Send the embed with some text

connections = {}

@bot.command()
async def record(ctx):  # If you're using commands.Bot, this will also work.
    voice = ctx.author.voice

    if not voice:
        await ctx.respond("You aren't in a voice channel!")

    vc = await voice.channel.connect()  # Connect to the voice channel the author is in.
    connections.update({ctx.guild.id: vc})  # Updating the cache with the guild and channel.

    vc.start_recording(
        discord.sinks.WaveSink(),  # The sink type to use.
        once_done,  # What to do once done.
        ctx.channel  # The channel to disconnect from.
    )
    await ctx.respond("Started recording!")
async def once_done(sink: discord.sinks, channel: discord.TextChannel, *args):  # Our voice client already passes these in.
    recorded_users = [  # A list of recorded users
        f"<@{user_id}>"
        for user_id, audio in sink.audio_data.items()
    ]
    await sink.vc.disconnect()  # Disconnect from the voice channel.
    files = [discord.File(audio.file, f"{user_id}.{sink.encoding}") for user_id, audio in sink.audio_data.items()]  # List down the files.
    await channel.send(f"finished recording audio for: {', '.join(recorded_users)}.", files=files)  # Send a message with the accumulated files.
@bot.command()
async def stop_recording(ctx):
    if ctx.guild.id in connections:  # Check if the guild is in the cache.
        vc = connections[ctx.guild.id]
        vc.stop_recording()  # Stop recording, and call the callback (once_done).
        del connections[ctx.guild.id]  # Remove the guild from the cache.
        await ctx.delete()  # And delete.
    else:
        await ctx.respond("I am currently not recording here.")  # Respond with this if we aren't recording.



    
mongo = discord.SlashCommandGroup("mongo", "mongo related commands")




@mongo.command()
async def clasificacion(ctx):
    await moduloEmbed.clasificacion(ctx)
@mongo.command()
async def insertar_partido(ctx, x: str,y: str,z: str):
    await ctx.respond(insertar(x,y,z))

@mongo.command()
async def recuperar_partido_equipo(ctx, equipo: str):
    await ctx.respond(buscar_equipos_por_nome(equipo))



bot.add_application_command(mongo)
printer = pprint.PrettyPrinter()
def insertar(nome1,nome2,ganhador):
    myDocument = {
        "equipo1":nome1,
        "equipo2":nome2,
        "gañador": ganhador
    }
    id = mycollection.insert_one(myDocument).inserted_id
    actualizar_victoria(ganhador)
    mensaxe="Insertouse correctamente con iste id: "+ str(id)+ " Felicidades a " + ganhador
    return mensaxe

def buscar_equipos_por_nome(nome: str):
    columns = {"_id":0, "equipo1":1,"equipo2":1,"gañador":1}
    equipos=list(mycollection.find({"equipo1":nome},columns))
    equipos2=list(mycollection.find({"equipo2":nome},columns))
    equipoXeneral=equipos+equipos2
    devolto="esta é a lista dos partidos xogados polo equipo: "+ nome +"\n"
    devolto+="equipo1"+"\t"+"equipo2"+"\t"+"gañador"+"\n"
    i=0
    valT=" "
    for equipo in equipoXeneral:
        valT= " "
        for key, val in equipo.items():
            valT+=str(val)+"\t"
        devolto+= valT + "\n"
        i+=1
    return devolto
    



def actualizar_victoria(nome: str):

    retorno=mycollection2.update_one({
        'nome': nome
        },{
        '$inc': {
            'puntos': 3
                }
    }, upsert=False).raw_result
    return retorno

class MyModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(label="Short Input"))
        self.add_item(discord.ui.InputText(label="Long Input", style=discord.InputTextStyle.long))

    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Modal Results")
        embed.add_field(name="Short Input", value=self.children[0].value)
        embed.add_field(name="Long Input", value=self.children[1].value)
        await interaction.response.send_message(embeds=[embed])

@bot.slash_command()
async def modal_slash(ctx: discord.ApplicationContext):
    """Shows an example of a modal dialog being invoked from a slash command."""
    modal = MyModal(title="Modal via Slash Command")
    await ctx.send_modal(modal)


@bot.slash_command(name="play")
async def play(ctx):
    vc = ctx.author.voice # define our voice client

    if vc: # check if the bot is not in a voice channel
        channel = ctx.author.voice.channel
        voice = await channel.connect()
        source = FFmpegPCMAudio('manuProba.wav')
        player = voice.play(source)
        # connect to the voice channel
    else:
        await ctx.send("non estas conectado a unha canle de voz")

@bot.slash_command(name="desconectar")
async def leave(ctx):
    if (ctx.voice_client): # check if the bot is not in a voice channel
        await ctx.guild.voice_client.disconnect()
        await ctx.send("xa me desconectei")
    else:
        await ctx.send("non estou nunha canle de voz")



bot.run(os.getenv('TOKEN')) # run the bot with the token
