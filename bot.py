import discord, os, random
from discord.ext import commands
from bot_logic import gen_pass
import requests

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
    print(f'Hai fatto l\'accesso come {bot.user}')


@bot.command()
async def cia(ctx):
    await ctx.send(f'Ciao! Sono un bot {bot.user}!')

@bot.command()
async def heh(ctx, frase, count = 5):
    mesaggio = "# " + frase * count
    if len(mesaggio) > 2000:
        await ctx.send("Hai richiesto troppi caratteri, massimo 2000.")
    else:
        await ctx.send(mesaggio)
        
@bot.command()
async def genpass(ctx, count = 16):
    await ctx.send(gen_pass(count))
    
@bot.command()
async def memes(ctx):
    imgs = os.listdir('images')
    with open('images/' + random.choice(imgs), 'rb') as img:
        discordimg = discord.File(img)
    await ctx.send("Ecco un meme", file = discordimg)
    
def get_duck_image_url():    
    url = 'https://random-d.uk/api/random'
    res = requests.get(url)
    data = res.json()
    return data['url']

@bot.command('getPoints')
async def getPoints(ctx):
    contenuto = ""
    with open('textPoints.txt', 'r') as f:
        contenuto = f.read()
    for riga in f.split("\n"):
        if str(ctx.author.id) in riga:
            split = riga.split("=")
            
            punteggio = int(split[1].strip())
            
            await ctx.send('Hai **' + str(punteggio) + '** punti!')
                
@bot.command('modificaPoints')
async def modificaPoints(ctx, nuovo_punteggio):
    if not nuovo_punteggio:
        await ctx.send('Devi specificare un valore!')
        return
    
    try:
        nuovo_punteggio = int(nuovo_punteggio)
    except ValueError:
        await ctx.send('Il valore specificato deve essere un numero!')
        return

    trovato = False
    with open('textPoints.txt', 'r') as f:
        righe = f.readlines()

    with open('textPoints.txt', 'w') as f:
        for riga in righe:
            if str(ctx.author.id) in riga:
                split = riga.split("=")
                id = str(split[0].strip())
                nuovaRiga = f"{id} = {nuovo_punteggio}\n"
                f.write(nuovaRiga)
                trovato = True
            else:
                f.write(riga)
    
    if trovato:
        await ctx.send(f'Punteggio aggiornato a {nuovo_punteggio}')
    else:
        await ctx.send('ID utente non trovato nel file!')
 
@bot.command('aggiungiUtente')
async def aggiungiUtente(ctx):
    image_url = get_duck_image_url()
    await ctx.send(image_url)
     
      
@bot.command('duck')
async def duck(ctx):
    image_url = get_duck_image_url()
    await ctx.send(image_url)
    
@bot.command()
async def stop(ctx):
    await ctx.send('Il bot sta per andare offline...')
    await bot.close()
        
