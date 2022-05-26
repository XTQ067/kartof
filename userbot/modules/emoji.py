# NeonUserBot / əkmə lülüş baş
# petito bled
# ⌭ R ⲉ ⳑ ⲁ ⲏ // @relahx





from userbot.events import register 
from userbot.cmdhelp import CmdHelp
from userbot.text import cmojis, emojis, basemojitext

@register(outgoing=True, pattern=r"^.emoji(?:\s|$)([\s\S]*)")
async def emoji(e):
    textx = await e.get_reply_message()
    message = e.pattern_match.group(1).strip()

    if message:
        pass

    elif textx:
        message = textx.text

    else:
        await e.edit(f"ℹ️ __Bir söz və ya mətin ver.__\n🔹 **Nümunə:** `.emoji relahx`")
        return

    try:
        final = "  ".join(message).lower()
        for index in final:
            if index in basemojitext:
                text = emojis[basemojitext.index(index)]
                final = final.replace(index, text)
        await e.edit(final)

    except BaseException:
        await e.edit(f"**❎ Bu həddindən artıq çox böyük mətndir.**")


@register(outgoing=True, pattern=r"^.cmoji(?:\s|$)([\s\S]*)")
async def cmoji(c):
    message = c.pattern_match.group(1).strip()

    if message:
        try:
            emoji, message = message.split(" ", 1)

        except BaseException:
            await c.edit(f"ℹ️ __Bir söz və ya mətin ver.__\n🔹 **Nümunə:** `.cmoji 🔪 relahx`")
            return

    else:
        if len(message) < 1:
            await c.edit(f"ℹ️ __Bir söz və ya mətin ver.__\n🔹 **Nümunə:** `.cmoji 🔪 relahx`")
            return

    try:
        final = "  ".join(message).lower()
        for index in final:
            if index in basemojitext:
                text = cmojis[basemojitext.index(index)].format(e=emoji)
                final = final.replace(
                    index, text
                )
        await c.edit(final)

    except BaseException:
        await c.edit("**❎ Bu həddindən artıq çox böyük mətndir.**")


Help = CmdHelp('emoji')
Help.add_command('emoji','<söz/mətn>','Emojilər ilə bir şey yazın!','emoji <istədiyiniz söz/mətn>')
Help.add_command('cmoji <smaylik> <söz/mətn>','İstədiyiniz hər hansı bir smaylik və ya xarakter ilə bir şey yazın!','cmoji 👋 salam')
Help.add_info('**@NeonUserbot / @relahx**')
Help.add()
