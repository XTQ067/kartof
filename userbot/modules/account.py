from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.contacts import UnblockRequest
from userbot.events import register
from userbot import bot
from userbot.cmdhelp import CmdHelp 
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import MessageEntityMentionName
from telethon.utils import get_input_location
from telethon.errors import ImageProcessFailedError, PhotoCropSizeSmallError
from telethon.errors.rpcerrorlist import (PhotoExtInvalidError,
                                          UsernameOccupiedError)
from telethon.tl.functions.account import (UpdateProfileRequest,
                                           UpdateUsernameRequest)
from telethon.tl.functions.channels import GetAdminedPublicChannelsRequest
from telethon.tl.functions.photos import DeletePhotosRequest, GetUserPhotosRequest, UploadProfilePhotoRequest
from telethon.tl.types import InputPhoto, MessageMediaPhoto, User, Chat, Channel
import asyncio, os


aylar = {
    "Jan": "Yanvar",
    "Feb": "Fevral",
    "Mar": "Mart",
    "Apr": "Aprel",
    "May": "May",
    "Jun": "Iyun",
    "Jul": "Iyul",
    "Aug": "Avqust",
    "Sep": "Sentyabr",
    "Oct": "Oktyabr",
    "Nov": "Noyabr",
    "Dec": "Dekabr"

}


@register(outgoing=True, pattern=r"^.sinfo")
async def sinfos(event):
    await event.edit("`Yoxlanılır...` 🔄")
    chat = "@spambot"
    spamdurumu = None
    async with bot.conversation(chat) as conv:
        try:
            await conv.send_message("/start")
        except YouBlockedUserError:
            await event.client(UnblockRequest(178220800))
            await conv.send_message("/start")
        await event.client.send_read_acknowledge(conv.chat_id)
        spamdurumu = await conv.get_response()
        if spamdurumu.text.startswith("Dear"):
            getspam = spamdurumu.text.split("until ")[1].split(", ")[0]
            spamgun, spamay, spamyil = getspam.split(" ")[0], aylar[getspam.split(" ")[1]], getspam.split(" ")[2]
            spamsaat = spamdurumu.text.split(":")[0].split(", ")[1] + ":" + spamdurumu.text.split(":")[1].split("UTC.")[0]
            toparla = f"ℹ️ Spam müəyyən edildi! Siz spamınız {spamgun} {spamay} {spamyil} {spamsaat}  tarixində bitir."
            await event.edit(toparla)
        elif spamdurumu.text.startswith("Good news"):
            await event.edit('`Siz spam deyilsiniz.` ✅')
        else:
            await event.client.forward_messages(event.chat_id, spamdurumu)
            await event.delete()



from userbot.language import get_value
LANG = get_value("profile")

INVALID_MEDIA = LANG['INVALID_MEDIA']
PP_CHANGED = LANG['PP_CHANGED']
PP_TOO_SMOL = LANG['PP_TOO_SMOL']
PP_ERROR = LANG['PP_ERROR']

BIO_SUCCESS = LANG['BIO_SUCCESS']

NAME_OK = LANG['NAME_OK']
USERNAME_SUCCESS = LANG['USERNAME_SUCCESS']
USERNAME_TAKEN = LANG['USERNAME_TAKEN']


@register(outgoing=True, pattern="^.reserved$")
async def mine(event):
    result = await bot(GetAdminedPublicChannelsRequest())
    output_str = ""
    for channel_obj in result.chats:
        output_str += f"{channel_obj.title}\n@{channel_obj.username}\n\n"
    await event.edit(output_str)


@register(outgoing=True, pattern="^.name")
async def update_name(name):
    newname = name.text[6:]
    if " " not in newname:
        firstname = newname
        lastname = ""
    else:
        namesplit = newname.split(" ", 1)
        firstname = namesplit[0]
        lastname = namesplit[1]

    await name.client(
        UpdateProfileRequest(first_name=firstname, last_name=lastname))
    await name.edit(NAME_OK)


@register(outgoing=True, pattern="^.setpp$")
async def set_profilepic(propic):
    replymsg = await propic.get_reply_message()
    photo = None
    if replymsg.media:
        if isinstance(replymsg.media, MessageMediaPhoto):
            photo = await propic.client.download_media(message=replymsg.photo)
        elif "image" in replymsg.media.document.mime_type.split('/'):
            photo = await propic.client.download_file(replymsg.media.document)
        else:
            await propic.edit(INVALID_MEDIA)

    if photo:
        try:
            await propic.client(
                UploadProfilePhotoRequest(await
                                          propic.client.upload_file(photo)))
            os.remove(photo)
            await propic.edit(PP_CHANGED)
        except PhotoCropSizeSmallError:
            await propic.edit(PP_TOO_SMOL)
        except ImageProcessFailedError:
            await propic.edit(PP_ERROR)
        except PhotoExtInvalidError:
            await propic.edit(INVALID_MEDIA)


@register(outgoing=True, pattern="^.setbio (.*)")
async def set_biograph(setbio):
    newbio = setbio.pattern_match.group(1)
    await setbio.client(UpdateProfileRequest(about=newbio))
    await setbio.edit(BIO_SUCCESS)


@register(outgoing=True, pattern="^.username (.*)")
async def update_username(username):
    newusername = username.pattern_match.group(1)
    try:
        await username.client(UpdateUsernameRequest(newusername))
        await username.edit(USERNAME_SUCCESS)
    except UsernameOccupiedError:
        await username.edit(USERNAME_TAKEN)


@register(outgoing=True, pattern="^.count$")
async def count(event):
    u = 0
    g = 0
    c = 0
    bc = 0
    b = 0
    result = ""
    await event.edit("`Zəhmət olmasa gözləyiniz..`")
    dialogs = await bot.get_dialogs(limit=None, ignore_migrated=True)
    for d in dialogs:
        currrent_entity = d.entity
        if isinstance(currrent_entity, User):
            if currrent_entity.bot:
                b += 1
            else:
                u += 1
        elif isinstance(currrent_entity, Chat):
            g += 1
        elif isinstance(currrent_entity, Channel):
            if currrent_entity.broadcast:
                bc += 1
            else:
                c += 1
        else:
            print(d)

    result += f"`{LANG['USERS']}:`\t**{u}**\n"
    result += f"`{LANG['GROUPS']}:`\t**{g}**\n"
    result += f"`{LANG['SUPERGROUPS']}:`\t**{c}**\n"
    result += f"`{LANG['CHANNELS']}:`\t**{bc}**\n"
    result += f"`{LANG['BOTS']}:`\t**{b}**"

    await event.edit(result)


@register(outgoing=True, pattern=r"^.delpp")
async def remove_profilepic(delpfp):
    group = delpfp.text[8:]
    if group == 'all':
        lim = 0
    elif group.isdigit():
        lim = int(group)
    else:
        lim = 1

    pfplist = await delpfp.client(
        GetUserPhotosRequest(user_id=delpfp.from_id,offset=0, max_id=0,limit=lim))
    input_photos = []
    for sep in pfplist.photos:
        input_photos.append(InputPhoto(id=sep.id,access_hash=sep.access_hash,file_reference=sep.file_reference))
    await delpfp.client(DeletePhotosRequest(id=input_photos))
    await delpfp.edit(
        LANG['DELPFP'] % len(input_photos))

            


if 1 == 1:
    name = "Profil Şəkilləri"
    client = "userbot"

@register(outgoing=True, disable_errors=True, pattern="^.getpp(?: |$)(.*)")
async def potocmd(event):
    id = "".join(event.raw_text.split(maxsplit=2)[1:])
    user = await event.get_reply_message()
    chat = event.input_chat
    if user:
        photos = await event.client.get_profile_photos(user.sender)
        u = True
    else:
        photos = await event.client.get_profile_photos(chat)
        u = False
    if id.strip() == "":
        if len(photos) > 0:
            await event.client.send_file(event.chat_id, photos)
            await event.edit(f"**@NeonUserBot şəkilləri uğurla yüklədi.**")
        else:
            try:
                if u is True:
                    photo = await event.client.download_profile_photo(user.sender)
                else:
                    photo = await event.client.download_profile_photo(event.input_chat)
                await event.client.send_file(event.chat_id, photo)
                await event.edit("**@NeonUserBot şəkilləri uğurla yüklədi.**")
            except a:
                await event.edit("**Bu istifadəçinin heç bir şəkili yoxdur.**")
                return
    else:
        try:
            id = int(id)
            if id <= 0:
                await event.edit("**Zəhmət olmasa bir nəfərə cavab verin.**")
                return
        except:
            await event.edit(f"**Zəhmət olmasa bir nəfərə cavab verin.**")
            return
        if int(id) <= (len(photos)):
            send_photos = await event.client.download_media(photos[id - 1])
            await event.client.send_file(event.chat_id, send_photos)
        else:
            await event.edit("**Bu söhbətdə medyaya icazə verilmir.**")
            await asyncio.sleep(8)
            return

        
        
Help = CmdHelp("account")
Help.add_command("setpp", None, "Cavabladığınız fotonu Telegramda profil foto edər.")
Help.add_command("getpp <rəqəm>", None, "Cavab verdiyiniz insanın qeyd etdiyiniz sayda profil şəklini yükləyər. (Qrupda heç kimi yanıtlamadan yazsanız, sadəcə, qrupun şəklini, kanalda yazsanız, kanalın şəklini endirər.)")
Help.add_command("delpp <rəqəm/all>", None, "Telegram profilinizdə olan şəkilləri silər.")
Help.add_command("name <ad> yaxud .name <ad> <soyad>", None, "Telegramdakı adınızı dəyişdirər.")
Help.add_command("username <yeni istifadəçi adı>", None, "Telegramdakı istifadəçi adınızı dəyişdirir.")
Help.add_command("sinfo", None, "Hesabınızın spam olub olmadığını yoxlayar.")
Help.add_command("count", None, "Qruplarınızı, söhbətlərinizi, aktiv botları vs. sayar.")
Help.add()
