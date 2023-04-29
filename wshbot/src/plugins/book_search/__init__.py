from typing import List

from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, Event, PrivateMessageEvent, GroupMessageEvent
from nonebot.rule import to_me
from nonebot.matcher import Matcher
from nonebot.adapters.onebot.v11.message import Message
from nonebot.params import Arg, CommandArg, ArgPlainText

from . import spider as sp

from . import config as cf

book_search = on_command("bs", aliases={"找书", "求书", "book_search", 'bs'}, priority=5)

book_help = on_command("bs_help", aliases={"bk_help", "bk help"}, priority=4)

book_config = on_command("bs_config", aliases={"bk_config"}, priority=4)

@book_config.handle()
async def handle_first_receive(
        bot: Bot,
        event: Event):
    if (event.get_user_id() != cf.admin):
        return "你没有权限哦~"
    message = event.get_message()
    msg = (str(message)).strip().split(' ')
    if len(msg) <= 2:
        return "参数不合法"
    item = msg[1]
    if (item not in cf.config_dic.keys()):
        return "参数不合法"
    # 判断类似是否为bool
    if (cf.config_dic[item] == True or cf.config_dic[item] == False):
        cf.config_dic[item] = bool(msg[2])
    else:
        cf.config_dic[item] = int(msg[2])
    await book_config.send(Message("成功修改配置项"))
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
           f'\t支持语言：{",".join(langs.keys())}\n' \
           f'\t支持文件类型：{",".join(exts)}\n' \
           f'\t支持内容搜索：{",".join(contents.keys())}\n' \
           f'\t支持排序：{",".join(sorts.keys())}\n'

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

    def to_node(msg: str):
        user_id = event.user_id
        if user_id==1425123490 or user_id== "1425123490":
            user_id = 2948237169
        return {"type": "node", "data": {"name": f"{event.group_id}", "uin": user_id, "content": {
            "type": "text",
            "data": {
                "text": f"{msg}"
            }
        }}}

    #messages = [to_node(msg) for msg in [to_Message(r) for r in res]]
    messages = [to_node(msg) for msg in res]
    is_private = isinstance(event, PrivateMessageEvent)
    # print(messages)
    #return await book_search.send(Message(f'[CQ:at,qq={int(user_id)}], 为您找到如下结果：{",".join(res)}'))
    char = "\n"
    if (cf.config_dic.get('merge_forward') == False):
        return await book_search.send(Message(f'[CQ:at,qq={int(user_id)}], 为您找到如下结果：{char.join(res)}'))
    if (is_private):
        await bot.call_api(
            "send_private_forward_msg", user_id=event.user_id, messages=messages
        )
    else:
        await bot.call_api(
            "send_group_forward_msg", group_id=event.group_id, messages=messages
        )
