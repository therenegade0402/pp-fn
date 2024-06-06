import discord
from discord.ext import commands
import subprocess
import time
import random
import pyautogui
import asyncio

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True

bot = commands.Bot(command_prefix='.', intents=intents)

# ID du salon autorisé et du rôle à modifier
AUTHORIZED_CHANNEL_ID = 123456789012345678
ROLE_ID = 987654321098765432

# Chemin du dossier contenant les applications
APP_FOLDER = "macro"

async def execute_sequence(ctx, mode):
    role = discord.utils.get(ctx.guild.roles, id=ROLE_ID)
    if role is None:
        await ctx.send("Rôle introuvable.")
        return

    await ctx.send("Création en cours...")

    # Retirer la permission d'écrire au rôle
    overwrite = ctx.channel.overwrites_for(role)
    overwrite.send_messages = False
    await ctx.channel.set_permissions(role, overwrite=overwrite)

    # Lancer la première application
    subprocess.run([f"{APP_FOLDER}/{mode}-1.exe"])

    # Attendre la fermeture de l'application et générer un nombre aléatoire
    number = random.randint(1000, 9999)

    # Taper le code sur le clavier
    pyautogui.typewrite(str(number))
    pyautogui.press('enter')

    # Lancer la deuxième application
    subprocess.run([f"{APP_FOLDER}/{mode}-2.exe"])

    # Envoyer le message avec le mode et la clé
    await ctx.send(f"mode : {mode}\nclé : {number}")

    # Attendre 2 minutes
    await asyncio.sleep(120)

    # Envoyer "lancements en cours" et lancer la troisième application
    await ctx.send("Lancements en cours...")
    subprocess.run([f"{APP_FOLDER}/ready.exe"])

    # Envoyer "système opérationnel" et redonner la permission d'écrire au rôle
    await ctx.send("Système opérationnel.")
    overwrite.send_messages = True
    await ctx.channel.set_permissions(role, overwrite=overwrite)

@bot.command()
async def ppsolo(ctx):
    if ctx.channel.id != AUTHORIZED_CHANNEL_ID:
        await ctx.send("Cette commande ne peut être utilisée que dans un salon spécifique.")
        return
    await execute_sequence(ctx, "solo")

@bot.command()
async def ppduo(ctx):
    if ctx.channel.id != AUTHORIZED_CHANNEL_ID:
        await ctx.send("Cette commande ne peut être utilisée que dans un salon spécifique.")
        return
    await execute_sequence(ctx, "duo")

@bot.command()
async def pptrio(ctx):
    if ctx.channel.id != AUTHORIZED_CHANNEL_ID:
        await ctx.send("Cette commande ne peut être utilisée que dans un salon spécifique.")
        return
    await execute_sequence(ctx, "trio")

@bot.command()
async def ppsection(ctx):
    if ctx.channel.id != AUTHORIZED_CHANNEL_ID:
        await ctx.send("Cette commande ne peut être utilisée que dans un salon spécifique.")
        return
    await execute_sequence(ctx, "section")

# Remplacez 'YOUR_BOT_TOKEN' par votre token de bot Discord
bot.run('YOUR_BOT_TOKEN')
