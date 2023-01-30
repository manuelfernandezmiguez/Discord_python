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
async def partido(ctx):
    await ctx.respond(f"{one_record} éche o primeiro partido recollido")

testing_servers=[218047836539846657]

@bot.slash_command(description="sauda a alguen")
async def greet(ctx, user: discord.Member):
    await ctx.respond(f"Ola {user.mention}")

@bot.slash_command(description="comando de probas")
async def test(ctx):
    role = ctx.guild.get_role(463478871031939075)
    canle = ctx.channel
    guild = ctx.guild
    avatar = ctx.user.avatar
    colour = ctx.user.colour
    creado =ctx.user.created_at
    spotify= ctx.Spotify.album
    mensaxe = (f"esta é a canle: {canle}, este é o rol: {role}, este e o guild: {guild}, este é o avatar: {avatar}, é o color: {colour}, é a data de creacion: {creado}")
    mensaxe2 = (f" spotify? {spotify}")
    await ctx.respond(mensaxe2)


@bot.command()

async def embebido(ctx):
    embed = discord.Embed(
        title="My Amazing Embed",
        description="Embeds are super easy, barely an inconvenience.",
        color=discord.Colour.blurple(), # Pycord provides a class with default colors you can choose from
    )
    embed.add_field(name="A Normal Field", value="A really nice field with some information. **The description as well as the fields support markdown!**")

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

dice = discord.SlashCommandGroup("dice", "random dice related commands")


@dice.command()
async def tirar(ctx,caras: int,numero: int):
    await moduloEmbed.tirar(ctx, caras,numero)

    
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


#EXEMPLOS atopados na paxina de guía#


class MyView(discord.ui.View):
    @discord.ui.select( # the decorator that lets you specify the properties of the select menu
        placeholder = "Choose a Flavor!", # the placeholder text that will be displayed if nothing is selected
        min_values = 1, # the minimum number of values that must be selected by the users
        max_values = 1, # the maximum number of values that can be selected by the users
        options = [ # the list of options from which users can choose, a required field
            discord.SelectOption(
                label="Vanilla",
                description="Pick this if you like vanilla!"
            ),
            discord.SelectOption(
                label="Chocolate",
                description="Pick this if you like chocolate!"
            ),
            discord.SelectOption(
                label="Strawberry",
                description="Pick this if you like strawberry!"
            )
        ]
    )
    async def select_callback(self, select, interaction): # the function called when the user is done selecting options
        await interaction.response.send_message(f"Awesome! I like {select.values[0]} too!")


@bot.command()
async def flavor(ctx):
    await ctx.send("Choose a flavor!", view=MyView())


class MyView2(discord.ui.View): # Create a class called MyView that subclasses discord.ui.View
    @discord.ui.button(label="Click me!", style=discord.ButtonStyle.primary, emoji="😎") # Create a button with the label "😎 Click me!" with color Blurple
    async def button_callback(self, button, interaction):
        await interaction.response.send_message("You clicked the button!") # Send a message when the button is clicked

@bot.slash_command() # Create a slash command
async def button(ctx):
    await ctx.respond("This is a button!", view=MyView2()) # Send a message with our View class that contains the button


@bot.command(description="Sends the bot's latency.") # this decorator makes a slash command
async def ping(ctx): # a slash command will be created with the name "ping"
    await ctx.respond(f"Pong! Latency is {bot.latency}")

bot.run(os.getenv('TOKEN')) # run the bot with the token
