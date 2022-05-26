import sys
from asyncio import create_subprocess_shell as asyncsubshell
from asyncio import subprocess as asyncsub
from os import remove
from time import gmtime, strftime
from traceback import format_exc

from telethon import events

from userbot import bot, BOTLOG_CHATID, LOGSPAMMER, PATTERNS


def register(**args):
    """ Yeni bir feailiyyet qeyd edin """
    pattern = args.get('pattern', None)
    disable_edited = args.get('disable_edited', False)
    groups_only = args.get('groups_only', False)
    trigger_on_fwd = args.get('trigger_on_fwd', False)
    trigger_on_inline = args.get('trigger_on_inline', False)
    disable_errors = args.get('disable_errors', False)

    if pattern:
        args["pattern"] = pattern.replace("^.", "^[" + PATTERNS + "]")
    if "disable_edited" in args:
        del args['disable_edited']

    if "ignore_unsafe" in args:
        del args['ignore_unsafe']

    if "groups_only" in args:
        del args['groups_only']

    if "disable_errors" in args:
        del args['disable_errors']

    if "trigger_on_fwd" in args:
        del args['trigger_on_fwd']

    if "trigger_on_inline" in args:
        del args['trigger_on_inline']

    def decorator(func):
        async def wrapper(check):
            if LOGSPAMMER:
                send_to = check.chat_id
            else:
                send_to = BOTLOG_CHATID

            if not trigger_on_fwd and check.fwd_from:
                return

            if check.via_bot_id and not trigger_on_inline:
                return

            if groups_only and not check.is_group:
                await check.respond("**Bu modul qrup üçün nəzərdə tutulub.**\n**Lakin, mən buranın qrup olduğuna inanmıram** 🤔")
                return

            try:
                await func(check)

            except events.StopPropagation:
                raise events.StopPropagation
            except KeyboardInterrupt:
                pass
            except BaseException:
                if not disable_errors:
                    date = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                    
                    text = "❗️ **N Σ O N xəta faylı.** ❗️\n"
                    link = "@NeonSUP"
                    text += "**Xəta faylında botda baş verən hər hansı tərsliklərlə bağlı məlumatlar olur.**"
                    text += "**Bu xətanın niyə baş verdiyini öyrənmək üçün bu faylı**\n"
                    text += f"**{link} dəstək qrupuna göndər.**\n"
                    
                    ftext = "⇨⇨⇨⇨⇨⇨⇨⇨⇨⇨⇨⇨⇨ MƏLUMATLAR. ⇦⇦⇦⇦⇦⇦⇦⇦⇦⇦⇦⇦\n"
                    ftext += "\nTarix: " + date
                    ftext += "\nQrup ID: " + str(check.chat_id)
                    ftext += "\nGönderen İsdifadeçinin ID: " + \
                        str(check.sender_id)

                    ftext = "\n⇨⇨⇨⇨⇨⇨⇨⇨⇨ N Σ O N XƏTA HESABATI. ⇦⇦⇦⇦⇦⇦⇦⇦⇦\n"

                    ftext += "\n\nHadisə:\n"
                    ftext += str(check.text)
                    ftext += "\n\nİzləmə Məlumatı:\n"
                    ftext += str(format_exc())
                    ftext += "\n\nXƏTA:\n"
                    ftext += str(sys.exc_info()[1])
                    
                    ftext += "\n\n⇨⇨⇨⇨⇨⇨⇨⇨⇨ XƏTA SONLUĞU. ⇦⇦⇦⇦⇦⇦⇦⇦⇦⇦⇦"

                    command = "git log --pretty=format:\"%an: %s\" -10"

                    ftext += "\n\n\nSon 10 commit:\n"

                    process = await asyncsubshell(command,
                                                  stdout=asyncsub.PIPE,
                                                  stderr=asyncsub.PIPE)
                    stdout, stderr = await process.communicate()
                    result = str(stdout.decode().strip()) \
                        + str(stderr.decode().strip())

                    ftext += result

                    file = open("neon.log", "w+")
                    file.write(ftext)
                    file.close()

                    if LOGSPAMMER:
                        await check.client.respond("`Bağışla, [N Σ O N](https://t.me/NeonSup) çökdü.\
                        \nXeta hesabatları UserBot gündelik qrupunda gizlener.`")

                    await check.client.send_file(send_to,
                                                 "neon.log",
                                                 thumb="userbot/neon.jpg",
                                                 caption=text)
                    remove("neon.log")
            else:
                pass
        if not disable_edited:
            bot.add_event_handler(wrapper, events.MessageEdited(**args))
        bot.add_event_handler(wrapper, events.NewMessage(**args))

        return wrapper

    return decorator
