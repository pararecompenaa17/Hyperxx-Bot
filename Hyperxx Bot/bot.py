import discord
from discord.ext import commands

# =========================
# CONFIGURAÇÕES
# =========================

import os
TOKEN = os.getenv("DISCORD_TOKEN")

GAMEPASS_ROBUX = 700
GAMEPASS_PRECO = 34.90

GRUPO_ROBUX = 700
GRUPO_PRECO = 24.50

VERDE = 0x00FF66


# =========================
# BOT
# =========================

intents = discord.Intents.default()

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)


# =========================
# CÁLCULOS
# =========================

def calcular_gamepass(robux):
    return (robux / GAMEPASS_ROBUX) * GAMEPASS_PRECO


def calcular_grupo(robux):
    return (robux / GRUPO_ROBUX) * GRUPO_PRECO


# =========================
# MODAL
# =========================

class RobuxModal(discord.ui.Modal):

    def __init__(self, tipo):
        self.tipo = tipo

        if tipo == "gamepass":
            titulo = "🎮 Calcular Gamepass"
        else:
            titulo = "👥 Calcular Grupo"

        super().__init__(title=titulo)

        self.robux = discord.ui.TextInput(
            label="Quantidade de Robux",
            placeholder="Ex: 700",
            required=True,
            min_length=1,
            max_length=10
        )

        self.add_item(self.robux)

    async def on_submit(self, interaction: discord.Interaction):

        try:
            quantidade = int(self.robux.value)

            if quantidade <= 0:
                raise ValueError

        except ValueError:
            await interaction.response.send_message(
                "❌ Digite uma quantidade válida de Robux.",
                ephemeral=True
            )
            return

        if self.tipo == "gamepass":
            preco = calcular_gamepass(quantidade)

            titulo = "🎮 Hyperxx • Gamepass"

        else:
            preco = calcular_grupo(quantidade)

            titulo = "👥 Hyperxx • Grupo"

        embed = discord.Embed(
            title=titulo,
            color=VERDE
        )

        embed.add_field(
            name="💰 Robux",
            value=f"**{quantidade:,} Robux**".replace(",", "."),
            inline=False
        )

        embed.add_field(
            name="💵 Valor",
            value=f"**R$ {preco:.2f}**".replace(".", ","),
            inline=False
        )

        embed.set_footer(
            text="Hyperxx • Calculadora de Robux"
        )

        await interaction.response.send_message(
            embed=embed,
            ephemeral=True
        )


# =========================
# BOTÕES
# =========================

class HyperxxView(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Gamepass",
        emoji="🎮",
        style=discord.ButtonStyle.success,
        custom_id="hyperxx_gamepass"
    )
    async def gamepass(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        await interaction.response.send_modal(
            RobuxModal("gamepass")
        )

    @discord.ui.button(
        label="Grupo",
        emoji="👥",
        style=discord.ButtonStyle.success,
        custom_id="hyperxx_grupo"
    )
    async def grupo(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        await interaction.response.send_modal(
            RobuxModal("grupo")
        )


# =========================
# /CALCULADORA
# =========================

@bot.tree.command(
    name="calculadora",
    description="Abra a calculadora de Robux da Hyperxx"
)
async def calculadora(interaction: discord.Interaction):

    embed = discord.Embed(
        title="💚 HYPERXX",
        description=(
            "**Calculadora de Robux**\n\n"
            "Escolha uma opção abaixo:\n\n"
            "🎮 **Gamepass**\n"
            "700 Robux → **R$ 34,90**\n\n"
            "👥 **Grupo**\n"
            "700 Robux → **R$ 24,50**"
        ),
        color=VERDE
    )

    embed.set_footer(
        text="Hyperxx • Robux Calculator"
    )

    await interaction.response.send_message(
        embed=embed,
        view=HyperxxView()
    )


# =========================
# INICIAR BOT
# =========================

@bot.event
async def on_ready():

    await bot.tree.sync()

    print(f"🟢 Hyperxx conectado como {bot.user}")


bot.run(TOKEN)