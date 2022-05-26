# N Σ O N UserBot.
# Copyright (C) 2021 https://t.me/xwarn

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


from userbot import CMD_HELP, ALIVE_EMOJI
from userbot.events import register
from userbot.main import PLUGIN_MESAJLAR

from userbot.language import get_value
LANG = get_value("__neon")


@register(outgoing=True, pattern="^.neon(?: |$)(.*)")
async def yarasa(event):
    """ Dilvuran Vüqar. """
    args = event.pattern_match.group(1).lower()
    if args:
        if args in CMD_HELP:
            await event.edit(str(CMD_HELP[args]))
        else:
            await event.edit(LANG["NEED_PLUGIN"])
    else:
        string = ""
        sayfa = [sorted(list(CMD_HELP))[i:i + 5]
                 for i in range(0, len(sorted(list(CMD_HELP))), 5)]

        for i in sayfa:
            string += PLUGIN_MESAJLAR['emoji']
            for sira, a in enumerate(i):
                string += "__" + str(a)
                if sira == i.index(i[-1]):
                    string += "__"
                else:
                    string += "__, "
            string += "\n"
        await event.edit(LANG["NEED_MODULE"] + '\n\n' + string)
