
import os
from datetime import datetime

from PIL import Image
from telegraph import Telegraph, exceptions, upload_file

from userbot import TEMP_DOWNLOAD_DIRECTORY, bot
from userbot.events import register
from userbot.cmdhelp import CmdHelp as cmd

telegraph = Telegraph()
r = telegraph.create_account(short_name="telegraph")
auth_url = r["auth_url"]


@register(outgoing=True, pattern="^\.telegraph$")
@register(outgoing=True, pattern="^\.graph$")
async def telegraphs(graph):
    if not os.path.isdir(TEMP_DOWNLOAD_DIRECTORY):
        os.makedirs(TEMP_DOWNLOAD_DIRECTORY)

    if graph.reply_to_msg_id:
        start = datetime.now()
        r_message = await graph.get_reply_message()

        if r_message.media:
                downloaded_file_name = await bot.download_media(
                    r_message, TEMP_DOWNLOAD_DIRECTORY
                )
                end = datetime.now()
                ms = (end - start).seconds
                await graph.edit(
                    "{} saniyə içində {} yükləndi.".format(downloaded_file_name, ms)
                )
                try:
                    if downloaded_file_name.endswith((".webp")):
                        resize_image(downloaded_file_name)
                except AttributeError:
                    return await graph.edit("`Media təmin edilmir`")
                try:
                    start = datetime.now()
                    media_urls = upload_file(downloaded_file_name)
                except exceptions.TelegraphException as exc:
                    await graph.edit("ERROR: " + str(exc))
                    os.remove(downloaded_file_name)
                else:
                    end = datetime.now()
                    ms_two = (end - start).seconds
                    os.remove(downloaded_file_name)
                    await graph.edit(
                        "Link: ```https://telegra.ph{}```".format(
                            media_urls[0], (ms + ms_two)
                        ),
                        link_preview=True,
                    )

        elif r_message.text:
                user_object = await bot.get_entity(r_message.from_id)
                title_of_page = user_object.first_name 
                page_content = r_message.message
                if r_message.media:
                    if page_content != "":
                        title_of_page = page_content
                    downloaded_file_name = await bot.download_media(
                        r_message, TEMP_DOWNLOAD_DIRECTORY
                    )
                    m_list = None
                    with open(downloaded_file_name, "rb") as fd:
                        m_list = fd.readlines()
                    for m in m_list:
                        page_content += m.decode("UTF-8") + "\n"
                    os.remove(downloaded_file_name)
                page_content = page_content.replace("\n", "<br>")
                response = telegraph.create_page(
                    title_of_page, html_content=page_content
                )
                end = datetime.now()
                ms = (end - start).seconds
                await graph.edit(
                    "Link: ```hhttps://telegra.ph/{}```".format(
                        response["path"], ms
                    ),
                    link_preview=True,
                )
    else:
        await graph.edit("`Mesaja cavab ver.`")


def resize_image(image):
    im = Image.open(image)
    im.save(image, "PNG")


Kömək = cmd('telegraph')
Kömək.add_command("telegraph & .graph","<Mesaja cavab>","Cavab verdiyiniz mesajı Telegrapha yükləyər və linkini əldə edər.")
Kömək.add()
