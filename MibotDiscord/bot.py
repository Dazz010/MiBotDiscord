import discord
from discord import app_commands
from discord.ext import commands
import json

def load_items():
    with open('items.json', 'r') as f:
        return json.load(f)

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=discord.Intents.default())

    async def setup_hook(self):
        await self.tree.sync()

bot = MyBot()

# ✅ Función async para autocompletado
async def autocomplete_items(interaction: discord.Interaction, current: str):
    items = load_items()
    return [
        app_commands.Choice(name=item["name"], value=item["name"])
        for item in items if current.lower() in item["name"].lower()
    ][:25]

@bot.tree.command(name="testcolor", description="Probar color morado")
async def testcolor(interaction: discord.Interaction):
    embed = discord.Embed(
        title="Embed de prueba",
        description="Este debería verse morado.",
        color=discord.Color.from_rgb(138, 43, 226)  
    )
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="item", description="Mostrar información de un ítem")
@app_commands.describe(nombre="Nombre del ítem")
@app_commands.autocomplete(nombre=autocomplete_items)
async def item(interaction: discord.Interaction, nombre: str):
    items = load_items()
    for item in items:
        if item["name"].lower() == nombre.lower():
            embed = discord.Embed(
                title=item["name"],
                description=f"ID: `{item['id']}`\nValor: `{item['value']}`\nDemanda: `{item['demand']}`\nCategoría: `{item['category']}`",
                color=discord.Color.from_rgb(138, 43, 226)
            )
            embed.set_thumbnail(url=item["image"])
            await interaction.response.send_message(embed=embed)
            return
    await interaction.response.send_message("❌ Ítem no encontrado.")

bot.run(os.getenv("DISCORD_TOKEN"))