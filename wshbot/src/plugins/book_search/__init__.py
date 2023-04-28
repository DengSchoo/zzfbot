from typing import List

from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, Event, PrivateMessageEvent, GroupMessageEvent
from nonebot.rule import to_me
from nonebot.matcher import Matcher
from nonebot.adapters.onebot.v11.message import Message
from nonebot.params import Arg, CommandArg, ArgPlainText

from . import spider as sp

book_search = on_command("bs", aliases={"找书", "求书", "book_search", 'bs'}, priority=5)

book_help = on_command("bk --help", aliases={"bk_help", "bk help"}, priority=5)


@book_help.handle()
async def handle_first_receive(
        bot: Bot,
        event: Event):
    user_id = int(event.get_user_id())
    langs = sp.langs
    exts = sp.exts
    contents = sp.contents
    sorts = sp.sorts
    help = f'可选选项，不需要关注顺序\n' \
           f'\t支持语言：{",".join(langs.keys())}' \
           f'\t支持文件类型：{",".join(exts)}' \
           f'\t支持内容搜索：{",".join(contents.keys())}' \
           f'\t支持排序：{",".join(sorts.keys())}'

    await book_help.send(Message(f'[CQ:at,qq={int(user_id)}]'
                                 + f"\n{help}"))


@book_search.handle()
async def handle_first_receive(
        bot: Bot,
        event: Event):
    user_id = int(event.get_user_id())
    # if not wd.warden_id(str(user_id)):
    #     await mag_search.send(Message(f'[CQ:at, qq={int(user_id)}] √ ⑧ who?'))
    message = event.get_message()
    msg = (str(message)).strip().split(' ')
    if (len(msg) < 2):
        return '参数不合法 exp: bs 书名 [选项]\n' \
               '详细命令参照 bk --help：'
    key_word = msg[1]
    choice = ""
    if len(msg) > 2:
        choice = msg[2: len(msg) - 1]
    res = sp.search_first_list(key_word, choice)

    def to_node(msg: Message):
        return {"type": "node", "data": {"name": f"{event.group_id}", "uin": event.get_user_id(), "content": msg}}

    def to_Message(msg: str):
        return Message(msg)

    messages = [to_node(msg) for msg in [to_Message(r) for r in res]]
    is_private = isinstance(event, PrivateMessageEvent)
    print(is_private)
    if (is_private):
        await bot.call_api(
            "send_private_forward_msg", user_id=event.get_user_id(), messages=messages
        )
    else:
        await bot.call_api(
            "send_group_forward_msg", group_id=event.group_id, messages=messages
        )
