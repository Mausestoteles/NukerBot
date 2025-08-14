import os
import asyncio
import logging
from typing import List

import discord
from discord import app_commands

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
log = logging.getLogger("LKB")

TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    raise SystemExit("Bitte DISCORD_TOKEN als Umgebungsvariable setzen.")

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# ---------- Helpers ----------
def _is_deletable_channel(ch: discord.abc.GuildChannel) -> bool:
    return isinstance(ch, (discord.TextChannel, discord.VoiceChannel, discord.StageChannel, discord.ForumChannel))

def _is_category(ch: discord.abc.GuildChannel) -> bool:
    return isinstance(ch, discord.CategoryChannel)

def _is_admin_or_owner(member: discord.Member) -> bool:
    return member.guild_permissions.administrator or (member.guild and member.guild.owner_id == member.id)

# ---------- /ping ----------
@tree.command(name="ping", description="Healthcheck")
@app_commands.guild_only()
async def ping_cmd(interaction: discord.Interaction):
    await interaction.response.send_message("Pong! ✅", ephemeral=True)

# ---------- /lkb (Hauptgruppe) ----------
lkb = app_commands.Group(name="lkb", description="Lustiger Kleiner Bot Befehle")
channel_group = app_commands.Group(name="channel", description="Kanal-Operationen", parent=lkb)
members_group = app_commands.Group(name="members", description="Mitglieder-Operationen", parent=lkb)
roles_group = app_commands.Group(name="roles", description="Rollen-Operationen", parent=lkb)

# ---------- /lkb channel delete ----------
@channel_group.command(name="delete", description="Löscht Kanäle per Namen – mit * alles löschen.")
@app_commands.describe(name="Exakter Kanalname oder * für alle Kanäle")
@app_commands.guild_only()
async def delete_channels(interaction: discord.Interaction, name: str):
    member = interaction.user if isinstance(interaction.user, discord.Member) else None
    if not member or not member.guild_permissions.manage_channels:
        return await interaction.response.send_message("❌ Du brauchst **Kanäle verwalten**.", ephemeral=True)
    guild = interaction.guild
    if guild is None:
        return await interaction.response.send_message("❌ Nur in einem Server nutzbar.", ephemeral=True)
    await interaction.response.defer(ephemeral=True, thinking=True)
    try:
        if name.strip() == "*":
            normal_channels = [c for c in guild.channels if _is_deletable_channel(c)]
            categories = [c for c in guild.channels if _is_category(c)]
            deleted = errors = 0
            for ch in normal_channels:
                try:
                    await ch.delete(reason=f"/lkb channel delete by {interaction.user} (* all)")
                    deleted += 1; await asyncio.sleep(0.2)
                except Exception as e:
                    log.warning("Konnte Kanal nicht löschen: %s (%s)", ch, e); errors += 1
            for cat in categories:
                try:
                    await cat.delete(reason=f"/lkb channel delete by {interaction.user} (* all)")
                    deleted += 1; await asyncio.sleep(0.2)
                except Exception as e:
                    log.warning("Konnte Kategorie nicht löschen: %s (%s)", cat, e); errors += 1
            return await interaction.followup.send(f"🗑️ Fertig. Gelöscht: **{deleted}**. Fehler: **{errors}**.", ephemeral=True)
        else:
            target = name.strip().lower()
            to_delete_normal = [c for c in guild.channels if _is_deletable_channel(c) and c.name.lower() == target]
            to_delete_categories = [c for c in guild.channels if _is_category(c) and c.name.lower() == target]
            if not to_delete_normal and not to_delete_categories:
                return await interaction.followup.send(f"ℹ️ Nichts gefunden mit **{name}**.", ephemeral=True)
            deleted = errors = 0
            for ch in to_delete_normal:
                try:
                    await ch.delete(reason=f"/lkb channel delete by {interaction.user} (name={name})")
                    deleted += 1; await asyncio.sleep(0.2)
                except Exception as e:
                    log.warning("Konnte Kanal nicht löschen: %s (%s)", ch, e); errors += 1
            for cat in to_delete_categories:
                try:
                    await cat.delete(reason=f"/lkb channel delete by {interaction.user} (name={name})")
                    deleted += 1; await asyncio.sleep(0.2)
                except Exception as e:
                    log.warning("Konnte Kategorie nicht löschen: %s (%s)", cat, e); errors += 1
            return await interaction.followup.send(f"🗑️ Gelöscht: **{deleted}** mit **{name}**. Fehler: **{errors}**.", ephemeral=True)
    except discord.Forbidden:
        return await interaction.followup.send("❌ Mir fehlen Rechte (Manage Channels / Rollen-Hierarchie).", ephemeral=True)
    except discord.HTTPException as e:
        return await interaction.followup.send(f"❌ Discord-Fehler: {e}", ephemeral=True)
    except Exception as e:
        log.exception("Unerwarteter Fehler")
        return await interaction.followup.send(f"❌ Unerwarteter Fehler: {e}", ephemeral=True)

# ---------- /lkb channel rename_all ----------
@channel_group.command(name="rename_all", description="Benennt alle Kanäle nach einem Muster um.")
@app_commands.describe(
    base="Basename, z. B. 'channel' (Ergebnis: channel-01, channel-02, ...)",
    start="Startindex (Standard: 1)",
    include_categories="Auch Kategorien umbenennen (Standard: Nein)"
)
@app_commands.guild_only()
async def rename_all_channels(
    interaction: discord.Interaction,
    base: str,
    start: app_commands.Range[int, 0] = 1,
    include_categories: bool = False
):
    member = interaction.user if isinstance(interaction.user, discord.Member) else None
    if not member or not member.guild_permissions.manage_channels:
        return await interaction.response.send_message("❌ Du brauchst **Kanäle verwalten**.", ephemeral=True)
    guild = interaction.guild
    if guild is None:
        return await interaction.response.send_message("❌ Nur im Server nutzbar.", ephemeral=True)
    await interaction.response.defer(ephemeral=True, thinking=True)
    index = start
    renamed = errors = 0
    channels: List[discord.abc.GuildChannel] = [c for c in guild.channels if _is_deletable_channel(c)]
    for ch in channels:
        try:
            new_name = f"{base}-{index:02d}"
            index += 1
            if ch.name != new_name:
                await ch.edit(name=new_name, reason=f"/lkb channel rename_all by {interaction.user}")
                renamed += 1
            await asyncio.sleep(0.2)
        except Exception as e:
            log.warning("Konnte Kanal nicht umbenennen: %s (%s)", ch, e); errors += 1
    if include_categories:
        categories: List[discord.CategoryChannel] = [c for c in guild.channels if _is_category(c)]
        for cat in categories:
            try:
                new_name = f"{base}-cat-{index:02d}"
                index += 1
                if cat.name != new_name:
                    await cat.edit(name=new_name, reason=f"/lkb channel rename_all by {interaction.user}")
                    renamed += 1
                await asyncio.sleep(0.2)
            except Exception as e:
                log.warning("Konnte Kategorie nicht umbenennen: %s (%s)", cat, e); errors += 1
    return await interaction.followup.send(f"✏️ Umbenannt: **{renamed}**. Fehler: **{errors}**.", ephemeral=True)

# ---------- /lkb members kick_all ----------
@members_group.command(name="kick_all", description="Kickt alle Mitglieder.")
@app_commands.describe(
    reason="Grund (Audit Log)",
    include_admins="Auch Admins/Owner kicken (nicht empfohlen)",
    include_bots="Auch Bots kicken",
    confirm="Sicherheitsbestätigung: tippe GENAU 'YES'"
)
@app_commands.guild_only()
async def kick_all_members(
    interaction: discord.Interaction,
    reason: str = "Mass kick via LKB",
    include_admins: bool = False,
    include_bots: bool = False,
    confirm: str = ""
):
    member = interaction.user if isinstance(interaction.user, discord.Member) else None
    if not member or not member.guild_permissions.administrator:
        return await interaction.response.send_message("❌ Du brauchst **Administrator**.", ephemeral=True)
    if confirm != "YES":
        return await interaction.response.send_message("⚠️ Abbruch. Setze **confirm** auf **YES**.", ephemeral=True)
    guild = interaction.guild
    if guild is None:
        return await interaction.response.send_message("❌ Nur im Server nutzbar.", ephemeral=True)
    await interaction.response.defer(ephemeral=True, thinking=True)
    kicked = errors = 0
    async for m in guild.fetch_members(limit=None):
        try:
            if m.id == guild.owner_id:
                continue
            if not include_admins and _is_admin_or_owner(m):
                continue
            if not include_bots and m.bot:
                continue
            if m == guild.me:
                continue
            await guild.kick(m, reason=reason)
            kicked += 1
            await asyncio.sleep(0.2)
        except Exception as e:
            log.warning("Konnte %s nicht kicken: %s", getattr(m, "name", "Mitglied"), e); errors += 1
    return await interaction.followup.send(f"👢 Gekickt: **{kicked}**. Fehler: **{errors}**.", ephemeral=True)

# ---------- /lkb roles delete_all ----------
@roles_group.command(name="delete_all", description="Löscht alle Rollen. Lasset sie brennen")
@app_commands.describe(
    include_managed="Auch gemanagte/Integrations-Rollen versuchen",
    confirm="Sicherheitsbestätigung: tippe GENAU 'YES'"
)
@app_commands.guild_only()
async def delete_all_roles(
    interaction: discord.Interaction,
    include_managed: bool = False,
    confirm: str = ""
):
    member = interaction.user if isinstance(interaction.user, discord.Member) else None
    if not member or not (member.guild_permissions.manage_guild or member.guild_permissions.administrator):
        return await interaction.response.send_message("❌ Du brauchst **Server verwalten** (oder Admin).", ephemeral=True)
    if confirm != "YES":
        return await interaction.response.send_message("⚠️ Abbruch. Setze **confirm** auf **YES**.", ephemeral=True)
    guild = interaction.guild
    if guild is None:
        return await interaction.response.send_message("❌ Nur im Server nutzbar.", ephemeral=True)
    await interaction.response.defer(ephemeral=True, thinking=True)
    deleted = errors = skipped = 0
    for role in guild.roles:
        try:
            if role.is_default():  # @everyone
                skipped += 1; continue
            if role >= guild.me.top_role:
                skipped += 1; continue
            if role.managed and not include_managed:
                skipped += 1; continue
            await role.delete(reason=f"/lkb roles delete_all by {interaction.user}")
            deleted += 1
            await asyncio.sleep(0.15)
        except Exception as e:
            log.warning("Konnte Rolle nicht löschen: %s (%s)", role, e); errors += 1
    return await interaction.followup.send(
        f"🧹 Rollen gelöscht: **{deleted}**, übersprungen: **{skipped}**, Fehler: **{errors}**.",
        ephemeral=True
    )

# ---------- /lkb server info ----------
@lkb.command(name="server", description="Server-Infos anzeigen")
@app_commands.guild_only()
async def server_info(interaction: discord.Interaction):
    guild = interaction.guild
    if guild is None:
        return await interaction.response.send_message("❌ Nur im Server nutzbar.", ephemeral=True)

    # Basis-Zahlen
    total_members = guild.member_count
    roles_count = len(guild.roles)
    text_channels = sum(isinstance(c, discord.TextChannel) for c in guild.channels)
    voice_channels = sum(isinstance(c, discord.VoiceChannel) for c in guild.channels)
    forum_channels = sum(isinstance(c, discord.ForumChannel) for c in guild.channels)
    categories = sum(isinstance(c, discord.CategoryChannel) for c in guild.channels)
    created = discord.utils.format_dt(guild.created_at, style="F")
    owner_mention = f"<@{guild.owner_id}>" if guild.owner_id else "Unbekannt"

    desc = (
        f"**Server:** {guild.name}\n"
        f"**ID:** {guild.id}\n"
        f"**Owner:** {owner_mention}\n"
        f"**Erstellt:** {created}\n"
        f"**Mitglieder:** {total_members}\n"
        f"**Rollen:** {roles_count}\n"
        f"**Kanäle:** Text {text_channels} · Voice {voice_channels} · Forum {forum_channels} · Kategorien {categories}\n"
    )

    await interaction.response.send_message(desc, ephemeral=True)

# ---------- /lkb resync ----------
@lkb.command(name="resync", description="Slash-Commands neu synchronisieren (Admin).")
@app_commands.guild_only()
async def resync_cmd(interaction: discord.Interaction):
    member = interaction.user if isinstance(interaction.user, discord.Member) else None
    if not member or not member.guild_permissions.administrator:
        return await interaction.response.send_message("❌ Nur für Administratoren.", ephemeral=True)
    await interaction.response.defer(ephemeral=True, thinking=True)
    try:
        global_count = len(await tree.sync())
        for g in client.guilds:
            await tree.sync(guild=g)
        return await interaction.followup.send(f"🔁 Resync ok. Global: {global_count} cmds. Gilden: {len(client.guilds)}.", ephemeral=True)
    except Exception as e:
        log.exception("Resync-Fehler")
        return await interaction.followup.send(f"❌ Resync-Fehler: {e}", ephemeral=True)

# Gruppe registrieren (nach allen Subcommands!)
tree.add_command(lkb)

# ---------- Sync global + pro Gilde ----------
@client.event
async def on_ready():
    try:
        synced = await tree.sync()  # global
        log.info("Global %d Slash-Commands synchronisiert.", len(synced))
        for g in client.guilds:      # pro Gilde (schnell sichtbar)
            await tree.sync(guild=g)
        log.info("Slash-Commands pro Gilde synchronisiert (%d Gilden).", len(client.guilds))
        log.info("Eingeloggt als %s (ID: %s)", client.user, client.user.id)
    except Exception:
        log.exception("Fehler beim Sync der Slash-Commands")

@client.event
async def on_guild_join(guild: discord.Guild):
    try:
        await tree.sync(guild=guild)
        log.info("Slash-Commands für neue Gilde synchronisiert: %s (%s)", guild.name, guild.id)
    except Exception:
        log.exception("Fehler beim Sync in neuer Gilde")

# ---------- Start ----------
def main():
    client.run(TOKEN)

if __name__ == "__main__":
    main()
# /* ======================================== */
# // Signature
# //
#    01001001 01110000 01000001 01110101 01010110 01000011 01000101
#    01100111 01011010 01000101 01010011 00111000 01001010 00110010
#    01001001 01101110 01010000 01100111 00111101 00111101
# /* ======================================== */
