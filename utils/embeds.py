import discord


def embed_error(mensaje: str) -> discord.Embed:
    return discord.Embed(description=f"❌ {mensaje}", color=discord.Color.red())
