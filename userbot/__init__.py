# N Σ O N UserBot.
# Copyright (C) 2021-2022 @NeonDevs

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://github.com/XTQ067/kartof/blob/master/LICENSE>.


from telethon.tl.functions.channels import EditPhotoRequest, CreateChannelRequest
from telethon.events import callbackquery, InlineQuery, NewMessage
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.contacts import UnblockRequest
from logging import basicConfig, getLogger, INFO, DEBUG
from telethon.sync import TelegramClient, custom
from telethon.sessions import StringSession
from distutils.util import strtobool as sb
from time import sleep 
from userbot.text import ZALG_LIST
from dotenv import load_dotenv
from pySmartDL import SmartDL
from sys import version_info
from requests import get
from re import compile
from math import ceil
import os, time, random
from random import randint


load_dotenv("config.env")

# Bot gündeliyi
CONSOLE_LOGGER_VERBOSE = sb(os.environ.get("CONSOLE_LOGGER_VERBOSE", "False"))

ASYNC_POOL = []

if CONSOLE_LOGGER_VERBOSE:
    basicConfig(
        format="%(asctime)s - @NeonUserBot - %(levelname)s - %(message)s",
        level=DEBUG,
    )
else:
    basicConfig(
        format="%(asctime)s - @NeonUserBot - %(levelname)s - %(message)s",
        level=INFO)

LOGS = getLogger(__name__)

if version_info[0] < 3 or version_info[1] < 6:
    LOGS.info("Ən az Python 3.6 versiyasına sahib olmalısınız."
              "Birdən çox xüsusiyyət buna bağlıdır. Bot söndürülür.")
    quit(1)

CONFIG_CHECK = os.environ.get(
    "___________XAIS_______BU_____SETIRI_____SILIN__________", None)

if CONFIG_CHECK:
    LOGS.info(
        "Zehmet olmasa ilk setirdeki yazını config.env faylından silin"
    )
    quit(1)

# Bot'un dili
LANGUAGE = os.environ.get("LANGUAGE", "DEFAULT").upper()

if LANGUAGE not in ["EN", "TR", "AZ", "UZ", "DEFAULT"]:
    LOGS.info("Namelum dil yazıdnız buna göre DEFAULT dil işledilir.")
    LANGUAGE = "DEFAULT"

# N Σ O N Versiyası
NEON_VERSION = "v2"

# Telegram API KEY ve HASH
API_KEY = os.environ.get("API_KEY", None)
API_HASH = os.environ.get("API_HASH", None)

# Alive ucun

ALIVE_EMOJI = os.environ.get(
    "ALIVE_EMOJI") or "🈴 "


SILINEN_PLUGIN = {}

# UserBot Session String
STRING_SESSION = os.environ.get("STRING_SESSION", None)

# BotLog üçün yaradılan chat'ın id'i.
BOTLOG_CHATID = int(os.environ.get("BOTLOG_CHATID", None))

# BotLog.
BOTLOG = sb(os.environ.get("BOTLOG", "True"))
LOGSPAMMER = sb(os.environ.get("LOGSPAMMER", "False"))

# Hey! Bu bir bot. :)
PM_AUTO_BAN = sb(os.environ.get("PM_AUTO_BAN", "False"))

# Yenileme üçün
HEROKU_MEMEZ = sb(os.environ.get("HEROKU_MEMEZ", "False"))
HEROKU_APPNAME = os.environ.get("HEROKU_APPNAME", None)
HEROKU_APIKEY = os.environ.get("HEROKU_APIKEY", None)

# Yenileme üçün repo linki
UPSTREAM_REPO_URL = os.environ.get(
    "UPSTREAM_REPO_URL",
    "https://github.com/xtq067/kartof.git")

# Konsol gündeliy
CONSOLE_LOGGER_VERBOSE = sb(os.environ.get("CONSOLE_LOGGER_VERBOSE", "False"))

# SQL
DB_URI = os.environ.get("DATABASE_URL", "sqlite:///neon.db")

# OCR API
OCR_SPACE_API_KEY = os.environ.get("OCR_SPACE_API_KEY", None)

# remove.bg API
REM_BG_API_KEY = os.environ.get("REM_BG_API_KEY", "xGE67a8gmw59pARmEE9DKrBf")

# AVTO PP
AVTO_PP = os.environ.get("AVTO_PP", None)

# Warn
WARN_LIMIT = int(os.environ.get("WARN_LIMIT", 3))
WARN_MODE = os.environ.get("WARN_MODE", "gmute")

if WARN_MODE not in ["gmute", "gban"]:
    WARN_MODE = "gmute"

# Qaleriya
QALERIYA_VAXT = int(os.environ.get("QALERIYA_VAXT", 60))

# Sticker Paket Adı
S_PACK_NAME = os.environ.get("S_PACK_NAME", "@NeonUserBot Sticker")

# SUDO
try:
    SUDO = set(int(x) for x in os.environ.get("SUDO", "").split())
except ValueError:
    raise Exception("SUDO qeyd etməmisiniz!")

#
CHROME_DRIVER = os.environ.get("CHROME_DRIVER", None)
GOOGLE_CHROME_BIN = os.environ.get("GOOGLE_CHROME_BIN", None)

PLUGINID = os.environ.get("PLUGIN_CHANNEL_ID", None)
# Plugin İçin
if not PLUGINID:
    PLUGIN_CHANNEL_ID = "me"
else:
    PLUGIN_CHANNEL_ID = int(PLUGINID)

# OpenWeatherMap API
OPEN_WEATHER_MAP_APPID = os.environ.get("OPEN_WEATHER_MAP_APPID", "e71bd502d0c7ede5a5d1396920eb98e0")
WEATHER_DEFCITY = os.environ.get("WEATHER_DEFCITY", None)

# Lydia API
LYDIA_API_KEY = os.environ.get("LYDIA_API_KEY", None)

# Anti Spambot
ANTI_SPAMBOT = sb(os.environ.get("ANTI_SPAMBOT", "False"))
ANTI_SPAMBOT_SHOUT = sb(os.environ.get("ANTI_SPAMBOT_SHOUT", "False"))

# Saat & Tarix - Ölke Saat dilimi
COUNTRY = str(os.environ.get("COUNTRY", ""))
TZ_NUMBER = int(os.environ.get("TZ_NUMBER", 1))

#
CLEAN_WELCOME = sb(os.environ.get("CLEAN_WELCOME", "True"))

# Last.fm
BIO_PREFIX = os.environ.get("BIO_PREFIX", "@NeonUserBot | ")
DEFAULT_BIO = os.environ.get("DEFAULT_BIO", None)


# Google Drive
G_DRIVE_CLIENT_ID = os.environ.get("G_DRIVE_CLIENT_ID", None)
G_DRIVE_CLIENT_SECRET = os.environ.get("G_DRIVE_CLIENT_SECRET", None)
G_DRIVE_AUTH_TOKEN_DATA = os.environ.get("G_DRIVE_AUTH_TOKEN_DATA", None)
GDRIVE_FOLDER_ID = os.environ.get("GDRIVE_FOLDER_ID", None)
TEMP_DOWNLOAD_DIRECTORY = os.environ.get("TMP_DOWNLOAD_DIRECTORY",
                                         "./downloads")

# Inline bot
BOT_TOKEN = os.environ.get("BOT_TOKEN", None)
BOT_USERNAME = os.environ.get("BOT_USERNAME", None)

# Genius
GENIUS = os.environ.get("GENIUS", None)
CMD_HELP = {}
CMD_HELP_BOT = {}
PM_AUTO_BAN_LIMIT = int(os.environ.get("PM_AUTO_BAN_LIMIT", 4))

SPOTIFY_DC = os.environ.get("SPOTIFY_DC", None)
SPOTIFY_KEY = os.environ.get("SPOTIFY_KEY", None)

PAKET_ISMI = os.environ.get("PAKET_ISMI", "Yarasa Sticker")

# Avto qatılma
AVTO_QATILMA = sb(os.environ.get("AVTO_QATILMA", "True"))

# Patternler
PATTERNS = os.environ.get("PATTERNS", ".;!,")
WHITELIST = [1930942562, 1849828581, 1901206758]
#              Vuqar      Oksigen      Nusrte
yetimler = []

# CloudMail.ru ve MEGA.nz
if not os.path.exists('bin'):
    os.mkdir('bin')

binaries = {
    "https://raw.githubusercontent.com/yshalsager/megadown/master/megadown":
    "bin/megadown",
    "https://raw.githubusercontent.com/yshalsager/cmrudl.py/master/cmrudl.py":
    "bin/cmrudl"
}

for binary, path in binaries.items():
    downloader = SmartDL(binary, path, progress_bar=False)
    downloader.start()
    os.chmod(path, 0o755)

# 'bot'
if STRING_SESSION:
    # pylint: devre dışı=geçersiz ad
    bot = TelegramClient(StringSession(STRING_SESSION), API_KEY, API_HASH)
else:
    # pylint: devre dışı=geçersiz ad
    bot = TelegramClient("userbot", API_KEY, API_HASH)


if os.path.exists("learning-data-root.check"):
    os.remove("learning-data-root.check")
else:
    LOGS.info("Braincheck faylı yoxdur, getirilir...")

URL = 'https://raw.githubusercontent.com/quiec/databasescape/master/learning-data-root.check'
with open('learning-data-root.check', 'wb') as load:
    load.write(get(URL).content)


async def check_botlog_chatid():
    if not BOTLOG_CHATID and LOGSPAMMER:
        LOGS.info(
            "Xüsusi xeta gündeliyinin işlemesi üçün BOTLOG_CHATID ayarlanmalıdır.")
        quit(1)

    elif not BOTLOG_CHATID and BOTLOG:
        LOGS.info(
            "Günlüye qeyd etme xüsusiyyetinin işlemesi üçün BOTLOG_CHATID ayarlanmalıdır.")
        quit(1)

    elif not BOTLOG or not LOGSPAMMER:
        return

    entity = await bot.get_entity(BOTLOG_CHATID)
    if entity.default_banned_rights.send_messages:
        LOGS.info(
            "Hesabınızın BOTLOG_CHATID qrupuna mesaj gönderme yetkisi yoxdur. "
            "Qrup ID'sini doğru yazıb yazmadığınızı yoxlayın.")
        quit(1)

        
# Assistant's client
if BOT_TOKEN is not None:
    tgbot = TelegramClient(
        "TG_BOT_TOKEN",
        api_id=API_KEY,
        api_hash=API_HASH
    ).start(bot_token=BOT_TOKEN)
else:
    tgbot = None


def butonlastir(sayfa, moduller):
    Satir = 5

    moduller = sorted(
        [modul for modul in moduller if not modul.startswith("_")])
    pairs = list(map(list, zip(moduller[::2], moduller[1::2])))
    if len(moduller) % 2 == 1:
        pairs.append([moduller[-1]])
    max_pages = ceil(len(pairs) / Satir)
    pairs = [pairs[i:i + Satir] for i in range(0, len(pairs), Satir)]
    butonlar = []
    for pairs in pairs[sayfa]:
        butonlar.append([custom.Button.inline("✅ " + pair,
                                              data=f"bilgi[{sayfa}]({pair})") for pair in pairs])

    butonlar.append([custom.Button.inline("⬅️ Geri",
                                          data=f"sayfa({(max_pages - 1) if sayfa == 0 else (sayfa - 1)})"),
                     custom.Button.inline("İrəli ➡️",
                                          data=f"sayfa({0 if sayfa == (max_pages - 1) else sayfa + 1})")])
    return [max_pages, butonlar]


with bot:
    if AVTO_QATILMA:
        try:
            bot(JoinChannelRequest("@NeonUserBot"))
            bot(JoinChannelRequest("@NeonSUP"))
            bot(JoinChannelRequest("@NeonPlugin"))
        except BaseException:
            pass

    moduller = CMD_HELP
    me = bot.get_me()
    nusrte = me.id

    '''
from random import randint
import heroku3
import sys

heroku_api = "https://api.heroku.com"
if HEROKU_APPNAME is not None and HEROKU_APIKEY is not None:
    Heroku = heroku3.from_key(HEROKU_APIKEY)
    app = Heroku.app(HEROKU_APPNAME)
    heroku_var = app.config()
else:
    app = None
     
async def asistan():
    if BOT_TOKEN:
        return
    await bot.start()
    LOGS.info("Asistan qurulur...")
    me.first_name + "-nin asistanı"
    usnm = me.username
    name = me.first_name
    if usnm:
        username = usnm + "_bot"
    else:
        username = f"neon" + str(random.randint(0, 1000000))[2:] + "bot"
    bf = "@BotFather"
    await bot(UnblockRequest(bf))
    await bot.send_message(bf, "/cancel")
    time.sleep(3)
    await bot.send_message(bf, "/start")
    time.sleep(3)
    await bot.send_message(bf, "/newbot")
    time.sleep(3)
    isdone = (await bot.get_messages(bf, limit=1))[0].text
    if isdone.startswith("That I cannot do."):
        LOGS.info(
            "Avtomatik bot yaratma prosesi alınmadı. @BotFather-dən manual olaraq bot yaradın."
        )
        sys.exit(1)
    await bot.send_message(bf, name)
    time.sleep(3)
    isdone = (await bot.get_messages(bf, limit=1))[0].text
    if not isdone.startswith("Good."):
        await bot.send_message(bf, "N Σ O N Asistan")
        time.sleep(3)
        isdone = (await bot.get_messages(bf, limit=1))[0].text
        if not isdone.startswith("Good."):
            LOGS.info(
                "Avtomatik bot yaratma prosesi alınmadı. @BotFather-dən manual olaraq bot yaradın."
            )
            sys.exit(1)
    await bot.send_message(bf, username)
    time.sleep(3)
    isdone = (await bot.get_messages(bf, limit=1))[0].text
    await bot.send_read_acknowledge("botfather")
    if isdone.startswith("Sorry,"):
        ran = randint(1, 100)
        username = f"neon" + str(random.randint(0, 1000000))[2:] + "_bot"
        await bot.send_message(bf, username)
        time.sleep(3)
        nowdone = (await bot.get_messages(bf, limit=1))[0].text
        if nowdone.startswith("Done!"):
            token = nowdone.split("`")[1]
            await bot.send_message(bf, "/setinline")
            time.sleep(3)
            await bot.send_message(bf, f"@{username}")
            time.sleep(3)
            await bot.send_message(bf, "Search")
            time.sleep(3)
            await bot.send_message(bf, "/setabouttext")
            time.sleep(3)
            await bot.send_message(bf, f"@{username}")
            time.sleep(3)
            await bot.send_message(bf, "@NeonUserBot Asistan")
            time.sleep(3)
            await bot.send_message(bf, "/setuserpic")
            time.sleep(3)
            await bot.send_message(bf, f"@{username}")
            time.sleep(3)
            await bot.send_file(bf, "userbot/neon.jpg")

            heroku_var["BOT_TOKEN"] = token
            heroku_var["BOT_USERNAME"] = username
            LOGS.info(f"@{username} Asistanınız hazırdır.")
        else:
            LOGS.info(
                "Avtomatik bot yaratma prosesi alınmadı. @BotFather-dən manual olaraq bot yaradın."
            )
            sys.exit(1)
    elif isdone.startswith("Done!"):
        token = isdone.split("`")[1]
        await bot.send_message(bf, "/setinline")
        time.sleep(3)
        await bot.send_message(bf, f"@{username}")
        time.sleep(3)
        await bot.send_message(bf, "Search")
        time.sleep(3)
        await bot.send_message(bf, "/setabouttext")
        time.sleep(3)
        await bot.send_message(bf, f"@{username}")
        time.sleep(3)
        await bot.send_message(bf, "@NeonUserBot Asistan")
        time.sleep(3)
        await bot.send_message(bf, "/setuserpic")
        time.sleep(3)
        await bot.send_message(bf, f"@{username}")
        time.sleep(3)
        await bot.send_file(bf, "userbot/neon.jpg") 
        time.sleep(3)
        await bot.send_message(bf, "/setcommands") 
        time.sleep(3)
        await bot.send_message(bf, f"@{username}")
        time.sleep(3)
        await bot.send_message(
            bf, 
            "start - Başlat.\
            \nhelp - Kömək.")
        heroku_var["BOT_TOKEN"] = token
        heroku_var["BOT_USERNAME"] = username
        LOGS.info(f"@{username} asistanınız hazırdır.")
    else:
        LOGS.info(
            "Avtomatik bot yaratma prosesi alınmadı. @BotFather-dən manual olaraq bot yaradın."
        )
        sys.exit(1)
with bot:
    bot.loop.run_until_complete(asistan())
'''

'''
async def botlog():
  if BOTLOG is True:
    await bot.start()
    
    LOGS.info("BOTLOG qurulur...")
    KanalId = await bot(CreateChannelRequest(
        title='N Σ O N',
        about="@NeonUserBot",
        megagroup=True
    ))
    KanalId = KanalId.chats[0].id

    Photo = await bot.upload_file(file='userbot/neon.jpg')
    await bot(EditPhotoRequest(channel=KanalId, 
        photo=Photo))
    msg = await bot.send_message(KanalId, "**Bu qrup qurulum zamanı yaradılmışdır, buradan çıxmayın!**")
    await msg.pin()

    KanalId = str(KanalId)
    heroku_var["BOTLOG"] = True
    heroku_var["BOTLOG_CHATID"] = KanalId
    LOGS.info("BOTLOG hazırdır.")
    sys.exit(1)
  else:
    return

with bot:
    bot.loop.run_until_complete(botlog())

'''

uid = me.id
SON_GORULME = 0
COUNT_MSG = 0
USERS = {}
BRAIN_CHECKER = []
COUNT_PM = {}
LASTMSG = {}
ENABLE_KILLME = True
ISAFK = False
AFKREASON = None
