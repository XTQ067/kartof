
from userbot.main import PLUGIN_MESAJLAR
from userbot.modules.admin import get_user_from_event
from userbot.cmdhelp import CmdHelp
from userbot.events import register
from userbot import BOTLOG, BOTLOG_CHATID, bot
from asyncio import sleep
from userbot.language import get_value
LANG = get_value("chat")

# ████████████████████████████████ #

""" Userid, chatid ve log emrleri olan UserBot modulu """


@register(outgoing=True, pattern="^.userid|^.id")
async def useridgetter(target):
    """ .userid komandası gösterilen istifadeçinin İD nömresini verir"""
    message = await target.get_reply_message()
    if message:
        if not message.forward:
            user_id = message.sender.id
            if message.sender.username:
                name = "@" + message.sender.username
            else:
                name = "**" + message.sender.first_name + "**"
        else:
            user_id = message.forward.sender.id
            if message.forward.sender.username:
                name = "@" + message.forward.sender.username
            else:
                name = "*" + message.forward.sender.first_name + "*"
        await target.edit("**{}** {} \n**{}** `{}`".format(
            LANG['USERNAME'], name, LANG['ID'], user_id))


@register(outgoing=True, pattern="^.link(?: |$)(.*)")
async def permalink(mention):
    """ .link emri gösterilen istifadeçinin profil bağlantısını metn şeklinde elçatan edir  """
    user, custom = await get_user_from_event(mention)
    if not user:
        return
    if custom:
        await mention.edit(f"[{custom}](tg://user?id={user.id})")
    else:
        tag = user.first_name.replace("\u2060",
                                      "") if user.first_name else user.username
        await mention.edit(f"[{tag}](tg://user?id={user.id})")


@register(outgoing=True, pattern="^.chatid$")
async def chatidgetter(chat):
    """ .chatid komandası gösterilen qrupun İD-sini verir """
    await chat.edit(f"{LANG['GROUP']} `" + str(chat.chat_id) + "`")


@register(outgoing=True, pattern=r"^.log(?: |$)([\s\S]*)")
async def log(log_text):
    """ .log komandası seçilen mesajı günlük grupuna gönderir """
    if BOTLOG:
        if log_text.reply_to_msg_id:
            reply_msg = await log_text.get_reply_message()
            await reply_msg.forward_to(BOTLOG_CHATID)
        elif log_text.pattern_match.group(1):
            user = f"#LOG / Grup ID: {log_text.chat_id}\n\n"
            textx = user + log_text.pattern_match.group(1)
            await bot.send_message(BOTLOG_CHATID, textx)
        else:
            await log_text.edit("`Bununla nə edə bilərəm  ?`")
            return
        await log_text.edit("`Günlükdə yaddaşa yazıldı`")
    else:
        await log_text.edit(LANG['NEED_LOG'])
    await sleep(2)
    await log_text.delete()


@register(outgoing=True, pattern="^.kickme$")
async def kickme(leave):
    chat = await leave.get_chat()
    me = leave.client.get_me()
    my_first_name = me.first_name
    my_full_name  = f"{me.first_name} {me.last_name}"
    myusername = f'@{me.username}'
    mymention  = f'[{my_first_name}](https://tg://user?id={me.id})'
    await leave.edit(PLUGIN_MESAJLAR['kickme'].format(
        id=chat.id,
        title=chat.title,
        myfirstname=my_first_name,
        myfullname=my_full_name,
        myusername=myusername,
        mymention=mymention,
        member_count="Bilinmiyor" if chat.participants_count is None else (chat.participants_count - 1)))
    await leave.client.kick_participant(leave.chat_id, 'me')


@register(outgoing=True, pattern="^.unmutechat$")
async def unmute_chat(unm_e):
    """ .unmutechat komandası susdurulmuş qrupun sesini açar """
    try:
        from userbot.modules.sql_helper.keep_read_sql import unkread
    except AttributeError:
        await unm_e.edit('`SQL off-mode rejimində işləyir!`')
        return
    unkread(str(unm_e.chat_id))
    await unm_e.edit(LANG['UNMUTED'])
    await sleep(2)
    await unm_e.delete()


@register(outgoing=True, pattern="^.mutechat$")
async def mute_chat(mute_e):
    """ .mutechat komandası qrupu sessizleşdirir """
    try:
        from userbot.modules.sql_helper.keep_read_sql import kread
    except AttributeError:
        await mute_e.edit("`SQL off-mode rejimində işləyir!`")
        return
    await mute_e.edit(str(mute_e.chat_id))
    kread(str(mute_e.chat_id))
    await mute_e.edit(LANG['MUTED'])
    await sleep(2)
    await mute_e.delete()
    if BOTLOG:
        await mute_e.client.send_message(
            BOTLOG_CHATID,
            str(mute_e.chat_id) + " sessizleşdirildi.")


@register(incoming=True, disable_errors=True)
async def keep_read(message):
    """ Mute mentiqi. """
    try:
        from userbot.modules.sql_helper.keep_read_sql import is_kread
    except AttributeError:
        return
    kread = is_kread()
    if kread:
        for i in kread:
            if i.groupid == str(message.chat_id):
                await message.client.send_read_acknowledge(message.chat_id)


# TGUSERBOT
regexNinja = False


@register(outgoing=True, pattern="^s/")
async def sedNinja(event):
    """Regex-ninja modulu üçün, s/ ilə başlayan avtomatik silmə komandası"""
    if regexNinja:
        await sleep(.5)
        await event.delete()


@register(outgoing=True, pattern="^.regexninja (on|off)$")
async def sedNinjaToggle(event):
    """ Regex ninja modulunu heyata keçirir veye deaktiv edir. """
    global regexNinja
    if event.pattern_match.group(1) == "on":
        regexNinja = True
        await event.edit("`Regexbot üçün ninja modulu aktivləşdirildi.`")
        await sleep(1)
        await event.delete()
    elif event.pattern_match.group(1) == "off":
        regexNinja = False
        await event.edit("`Regexbot için ninja modulu deaktiv edildi.`")
        await sleep(1)
        await event.delete()

Komek = CmdHelp("chat")
Komek.add_command("chatid", None, "Göstərilən qrupun ID nömrəsini verir")
Komek.add_command(
    "userid",
    None,
    "Cavab verdiyiniz istifadəçinin ID nömrəsini verir.")
Komek.add_command("log", None, "Cavablanan mesajı günlük grupuna göndərir.")
Komek.add_command(
    "kickme",
    None,
    "Əmri yazdığınız qrupdan çıxmağınızı həyata keçirər.")
Komek.add_command("mutechat", None, "Qrupu səssizləşdirər.")
Komek.add_command(
    "unmutechat",
    None,
    "Səssizləşdirilmiş bir qrupun səsini açar.")
Komek.add_command(
    "link <istifadəçi adı/id> : <istəyə uyğun mesaj>",
    None,
    "İstəyə bağlı şəxsi mətin ilə istifadəçinin  profilinə qalıcı bir link yaradın.")
Komek.add_command(
    "regexninja on/off",
    None,
    "Dünya miqyasında olaraq regex ninja modulunu aktivləşdirir / deaktiv edər.")
Komek.add()
