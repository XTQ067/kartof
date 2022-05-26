# N Σ O N // Nusrets
# ƏKMƏ BLƏT

from userbot.cmdhelp import CmdHelp
from userbot.events import register as neon
import os


@neon(outgoing=True, pattern="^.ytv (.*)")
async def inf(event):
    try:
        await event.edit("🔸 __Video məlumatları hazırlanır...__")
    except BaseException:
        pass
    os.system("pip install pytube")
    from pytube import YouTube
    url = event.pattern_match.group(1)
    axtar = YouTube(f"{url}")
    ad = axtar.title
    await event.edit(f"🔸 __{ad}'ı video kimi yükləyirəm...__")
    video = YouTube(f"{url}").streams.get_highest_resolution().download()
    await event.edit(f"🔸 __{ad} video kimi göndərirəm..__")
    await event.client.send_file(
        event.chat_id,
        video,
        caption=f"""
<b>Ad 🔖</b> ➠ <code>{ad}</code>
""",
        parse_mode="html")
    await event.delete()
    os.remove(video)


@neon(outgoing=True, pattern="^.yta (.*)")
async def audio(e):
    me = await e.client.get_me()
    my_mention = f'[{me.first_name}](tg://user?id={me.id})'
    u = f"@{me.username}" if me.username else my_mention
    try:
        await e.edit("🔸 __Musiqi hazırlanır. Gözləyin..__")
    except BaseException:
        pass
    os.system("pip install pytube")
    from pytube import YouTube
    os.system("pip install moviepy")
    import moviepy.editor as mp
    inputstr = e.pattern_match.group(1)
    axtar = YouTube(f"{inputstr}")
    mp3 = axtar.title
    await e.edit(f"🔸 __{mp3}__ __yüklənir...__")
    hmm = YouTube(f"{inputstr}").streams.filter(
        file_extension='mp4').first().download()
    await e.edit(f"🔸 __{mp3} musiqi olaraq hazırlanır...__")
    mahni = axtar.title + ".mp3"
    my_clip = mp.VideoFileClip(hmm)
    my_clip.audio.write_audiofile(mahni)
    await e.edit(f"🔸 __{mp3}__ __mp3 olaraq göndərilir...__")
    await e.client.send_file(
        e.chat_id,
        mahni,
        caption=f"""
<b>Ad 🔖</b> ➠ <code>{mp3}</code>
<b>Sahibim 💟</b> ➠ <b>{u}</b>
""",
        parse_mode="html")
    os.remove(hmm)
    os.remove(mahni)
    my_clip.close()
    await e.delete()


@neon(pattern="^.yt(?: |$)(.*)", outgoing=True)
async def YouTube_Search(e):
    try:
        from youtube_search import YoutubeSearch
    except BaseException:
        os.system("pip install youtube_search")
    from youtube_search import YoutubeSearch
    if e.fwd_from:
        return
    yt = e.pattern_match.group(1)
    axtar = await e.edit("`Axtarılır...`")
    nəticə = YoutubeSearch(f"{yt}",
                           max_results=5).to_dict()
    başlıq = "<b>N Σ O N YOUTUBE AXTARIŞI</b> \n\n"
    for n in nəticə:
        sorğu = n["id"]
        url = f"https://www.youtube.com/watch?v={sorğu}"
        ad = n["title"]
        kanal = n["channel"]
        uzunluğu = n["duration"]
        görüntüləmə = n["views"]
        başlıq += (
            f"<b>Ad</b> ➠ <code>{ad}</code> \n"
            f"<b>Link</b> ➠  {url} \n"
            f"<b>Kanal</b> ➠ <code>{kanal}</code> \n"
            f"<b>Video Uzunluğu</b> ➠ <code>{uzunluğu}</code> \n"
            f"<b>Görüntülənmə</b> ➠ <code>{görüntüləmə}</code> \n\n"
        )
        await axtar.edit(başlıq,
                         parse_mode="html")

Help = CmdHelp('yt')
Help.add_command('yt <musiqi Adı>', None, 'YouTube üzərindən verdiyiniz mətn üzrə axtarış edər.')
Help.add_command('yta <link 🔗>', None, 'Yazdığınız linki YouTube üzərindən musiqi olaraq yükləyər.')
Help.add_command('ytv <link 🔗>', None, "Yazdığınız linki YouTube üzərindən video kimi endirər.")
Help.add_info('**@NeonDevs / @NeonUserBot**')
Help.add()
