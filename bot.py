import os
import discord
# ---------- Configuração ----------
TOKEN = os.getenv("DISCORD_TOKEN")
TRAP_CHANNEL_ID = 1570190395923505263   # ID do canal armadilha
LOG_CHANNEL_ID = 1570259380107083846    # ID do canal de logs

intents = discord.Intents.default()  # não precisa de message_content
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f"Ratao ligano {client.user}")


@client.event
async def on_message(message: discord.Message):
    # Só age no canal armadilha, dentro de servidor
    if message.guild is None or message.channel.id != TRAP_CHANNEL_ID:
        return

    # Ignora só outros bots
    if message.author.bot:
        return

    user = message.author
    perms = user.guild_permissions
    is_staff = perms.administrator or perms.manage_messages or perms.ban_members

    try:
        if is_staff:
            # Adm/staff: bane e NÃO apaga as mensagens
            await message.guild.ban(
                user,
                reason="Conta hackeada (caiu no esgoto do ratao) - staff",
                delete_message_seconds=0,
            )
            status = "adm tomo ban burro "
        else:
            # Membro comum: softban (expulsa e apaga mensagens da última hora)
            await message.guild.ban(
                user,
                reason="Conta hackeada (caiu no esgoto do ratao)",
                delete_message_seconds=3600,
            )
            await message.guild.unban(user, reason="Softban do esgoto")
            status = "tomo kick burro"
    except discord.Forbidden:
        status = "FALHOU: cargo da pessoa é igual ou acima do bot"
    except discord.HTTPException as e:
        status = f"FALHOU: {e}"

    if LOG_CHANNEL_ID:
        log_channel = client.get_channel(LOG_CHANNEL_ID)
        if log_channel:
            await log_channel.send(
                f"🪤 **{user}** (`{user.id}`) Bobao foi hackeado → {status}"
            )


client.run(TOKEN)
