
import importlib
from importlib import import_module
from sqlite3 import connect
import os
import requests
from telethon.tl.types import InputMessagesFilterDocument
from telethon.errors.rpcerrorlist import PhoneNumberInvalidError
from . import BRAIN_CHECKER, LOGS, PLUGIN_CHANNEL_ID, NEON_VERSION, bot
from .modules import ALL_MODULES
import userbot.modules.sql_helper.mesaj_sql as MSJ_SQL
import userbot.modules.sql_helper.qaleriya_sql as QALERIYA_SQL
from telethon.tl import functions

from random import choice
import chromedriver_autoinstaller
import re
import userbot.cmdhelp
from userbot.text import (DIZCILIK_STR, 
                          ALIVE_MESAJLAR,
                          AFKSTR, 
                          UNAPPROVED_MSG)


DB = connect("learning-data-root.check")
CURSOR = DB.cursor()
CURSOR.execute("""SELECT * FROM BRAIN1""")
ALL_ROWS = CURSOR.fetchall()
INVALID_PH = '\nXETA: Yazılan telefon nömresi keçersizdir' \
             '\n  Meslehet: Ölke kodundan isdifade etmekle nömreni yazın' \
             '\n       Telefon nömrenizi yeniden yoxlayın.'

for i in ALL_ROWS:
    BRAIN_CHECKER.append(i[0])
connect("learning-data-root.check").close()


def extractCommands(file):
    FileRead = open(file, encoding="cp437").read()

    if '/' in file:
        file = file.split('/')[-1]

    Pattern = re.findall(r"@register\(.*pattern=(r|)\"(.*)\".*\)", FileRead)
    Komutlar = []

    if re.search(r'CmdHelp\(.*\)', FileRead):
        pass
    else:
        dosyaAdi = file.replace('.py', '')
        CmdHelp = userbot.cmdhelp.CmdHelp(dosyaAdi, False)

        # Komandaları alırıq #
        for Command in Pattern:
            Command = Command[1]
            if Command == '' or len(Command) <= 1:
                continue
            Komut = re.findall("(^.*[a-zA-Z0-9şğüöçı]\\w)", Command)
            if (len(Komut) >= 1) and (not Komut[0] == ''):
                Komut = Komut[0]
                if Komut[0] == '^':
                    KomutStr = Komut[1:]
                    if KomutStr[0] == '.':
                        KomutStr = KomutStr[1:]
                    Komutlar.append(KomutStr)
                else:
                    if Command[0] == '^':
                        KomutStr = Command[1:]
                        if KomutStr[0] == '.':
                            KomutStr = KomutStr[1:]
                        else:
                            KomutStr = Command
                        Komutlar.append(KomutStr)



            neonpy = re.search(
                '\"\"\"NEONPY(.*)\"\"\"', FileRead, re.DOTALL)
            if neonpy is not None:
                neonpy = neonpy.group(0)
                for Satir in neonpy.splitlines():
                    if ('"""' not in Satir) and (':' in Satir):
                        Satir = Satir.split(':')
                        Isim = Satir[0]
                        Deger = Satir[1][1:]

                        if Isim == 'INFO':
                            CmdHelp.add_info(Deger)
                        elif Isim == 'WARN':
                            CmdHelp.add_warning(Deger)
                        else:
                            CmdHelp.set_file_info(Isim, Deger)
            for Komut in Komutlar:
                # if re.search('\[(\w*)\]', Komut):
                # Komut = re.sub('(?<=\[.)[A-Za-z0-9_]*\]', '', Komut).replace('[', '')
                CmdHelp.add_command(
                    Komut, None, 'Bu plugin xaricden yüklenmişdir. Her hansı bir açıqlama yoxdur.')
            CmdHelp.add()


try:
    bot.start()
    idim = bot.get_me().id
    neonbl = []
    if idim in neonbl:
        bot.disconnect()

    try:
        chromedriver_autoinstaller.install()
    except BaseException:
        pass

    QALERIYA = {}

    PLUGIN_MESAJLAR = {}
    ORJ_PLUGIN_MESAJLAR = {
        "alive": str(choice(ALIVE_MESAJLAR)),
        "afk": str(choice(AFKSTR)),
        "kickme": "`Sağolun mən getdim.` ✨",
        "pm": UNAPPROVED_MSG,
        "dızcı": str(choice(DIZCILIK_STR)),
        "ban": "{mention}`, banlandı!`",
        "mute": "{mention}`, səssizləşdirildi!`",
        "approve": "{mention}`, mənə mesaj yazmağın üçün icazə verildi",
        "disapprove": "{mention}`, artıq mənə yaza bilməzsən!`",
        "block": "{mention}`, bloklandın😊",
        "restart": "Bot yenidər başladılır...",
        "emoji": "🈴",
        "tagstop": "**Tag prosesi uğurla dayandırıldı.** ✅"
    }

    PLUGIN_MESAJLAR_TURLER = ["alive",
                              "afk",
                              "kickme",
                              "emoji",
                              "restart",
                              "pm",
                              "dızcı",
                              "ban",
                              "mute",
                              "approve",
                              "disapprove",
                              "block",
                              "tagstop"]

    for mesaj in PLUGIN_MESAJLAR_TURLER:
        dmsj = MSJ_SQL.getir_mesaj(mesaj)
        if not dmsj:
            PLUGIN_MESAJLAR[mesaj] = ORJ_PLUGIN_MESAJLAR[mesaj]
        else:
            if dmsj.startswith("MEDYA_"):
                medya = int(dmsj.split("MEDYA_")[1])
                medya = bot.get_messages(PLUGIN_CHANNEL_ID, ids=medya)

                PLUGIN_MESAJLAR[mesaj] = medya
            else:
                PLUGIN_MESAJLAR[mesaj] = dmsj
    if PLUGIN_CHANNEL_ID is not None:
        LOGS.info("Pluginler Yüklenir...")
        try:
            KanalId = bot.get_entity(PLUGIN_CHANNEL_ID)
        except BaseException:
            KanalId = "me"

        for plugin in bot.iter_messages(
                KanalId, filter=InputMessagesFilterDocument):
            if plugin.file.name and (len(plugin.file.name.split('.')) > 1) \
                    and plugin.file.name.split('.')[-1] == 'py':
                Split = plugin.file.name.split('.')

                if not os.path.exists("./userbot/modules/" + plugin.file.name):
                    dosya = bot.download_media(plugin, "./userbot/modules/")
                else:
                    LOGS.info("Bu plugin onsuzda yüklənib " + plugin.file.name)
                    extractCommands('./userbot/modules/' + plugin.file.name)
                    dosya = plugin.file.name
                    continue

                try:
                    spec = importlib.util.spec_from_file_location(
                        "userbot.modules." + Split[0], dosya)
                    mod = importlib.util.module_from_spec(spec)

                    spec.loader.exec_module(mod)
                except Exception as e:
                    LOGS.info(
                        f"Yükləmə uğursuz! Plugin xətalıdır.\n\nXəta: ```{e}```")

                    try:
                        plugin.delete()
                    except BaseException:
                        pass

                    if os.path.exists("./userbot/modules/" + plugin.file.name):
                        os.remove("./userbot/modules/" + plugin.file.name)
                    continue
                extractCommands('./userbot/modules/' + plugin.file.name)
    else:
        bot.send_message(
            "me",
            f"`Zehmet olmasa pluginlerin qalıcı olması üçün PLUGIN_CHANNEL_ID'i ayarlayın.`")
except PhoneNumberInvalidError:
    print(INVALID_PH)
    exit(1)


async def FotoDegistir(foto):
    FOTOURL = QALERIYA_SQL.TUM_QALERIYA[foto].foto
    r = requests.get(FOTOURL)

    with open(str(foto) + ".jpg", 'wb') as f:
        f.write(r.content)
    file = await bot.upload_file(str(foto) + ".jpg")
    try:
        await bot(functions.photos.UploadProfilePhotoRequest(
            file
        ))
        return True
    except BaseException:
        return False

for module_name in ALL_MODULES:
    imported_module = import_module("userbot.modules." + module_name)

LOGS.info("N Σ O N işləyir. Yeniliklər üçün - @NeonUserBot.")
LOGS.info("N Σ O N Support - @NeonSUP.")
LOGS.info(f"Bot versiyası: {NEON_VERSION}")

bot.run_until_disconnected()
