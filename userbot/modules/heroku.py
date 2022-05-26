import heroku3, requests, asyncio, math, codecs, os

from userbot import (
    HEROKU_APPNAME,
    HEROKU_APIKEY,
    BOTLOG_CHATID,
    BOTLOG
)

from userbot.events import register
from userbot.cmdhelp import CmdHelp

heroku_api = "https://api.heroku.com"
if HEROKU_APPNAME is not None and HEROKU_APIKEY is not None:
    Heroku = heroku3.from_key(HEROKU_APIKEY)
    app = Heroku.app(HEROKU_APPNAME)
    heroku_var = app.config()
else:
    app = None


@register(outgoing=True, pattern=r"^.dyno(?: |$)")
async def dyno_usage(dyno):
    await dyno.edit("`Gözləyiniz...`")
    useragent = ('Mozilla/5.0 (Linux; Android 10; SM-G975F) '
                 'AppleWebKit/537.36 (KHTML, like Gecko) '
                 'Chrome/80.0.3987.149 Mobile Safari/537.36'
                 )
    u_id = Heroku.account().id
    headers = {
        'User-Agent': useragent,
        'Authorization': f'Bearer {HEROKU_APIKEY}',
        'Accept': 'application/vnd.heroku+json; version=3.account-quotas',
    }
    path = "/accounts/" + u_id + "/actions/get-quota"
    r = requests.get(heroku_api + path, headers=headers)
    if r.status_code != 200:
        return await dyno.edit("`Xəta:Bir problem baş verdi😢`\n\n"
                               f">.`{r.reason}`\n")
    result = r.json()
    quota = result['account_quota']
    quota_used = result['quota_used']

    """ - Used - """
    remaining_quota = quota - quota_used
    percentage = math.floor(remaining_quota / quota * 100)
    minutes_remaining = remaining_quota / 60
    hours = math.floor(minutes_remaining / 60)
    minutes = math.floor(minutes_remaining % 60)

    """ - Current - """
    App = result['apps']
    try:
        App[0]['quota_used']
    except IndexError:
        AppQuotaUsed = 0
        AppPercentage = 0
    else:
        AppQuotaUsed = App[0]['quota_used'] / 60
        AppPercentage = math.floor(App[0]['quota_used'] * 100 / quota)
    AppHours = math.floor(AppQuotaUsed / 60)
    AppMinutes = math.floor(AppQuotaUsed % 60)

    await asyncio.sleep(1.5)

    return await dyno.edit("**Dyno istifadəsi**:\n\n"
                           f" ➤ **İşlədilən Dyno Saatı**  **({HEROKU_APPNAME})**:\n"
                           f"     •  `{AppHours}` **saat**  `{AppMinutes}` **Dəqiqə**  "
                           f"**|**  [`{AppPercentage}` **%**]"
                           "\n"
                           " ➤ **Bu ay qalan dyno saatı⚡️**:\n"
                           f"     •  `{hours}` **saat**  `{minutes}` **Dəqiqə**  "
                           f"**|**  [`{percentage}` **%**]"
                           )


Kömək = CmdHelp("heroku")
Kömək.add_command("dyno", None, "Botda qalan və işlədilən dyno saatınız haqqında məlumat verir.")
Kömək.add()
