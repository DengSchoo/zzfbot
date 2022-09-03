from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.rule import to_me
from nonebot.matcher import Matcher
from nonebot.adapters.onebot.v11.message import Message
from nonebot.params import Arg, CommandArg, ArgPlainText

from ..warden import *

from . import spider as sp

mag_search = on_command("mag_searchX", aliases={"全资源磁力搜索"}, priority=5)

@mag_search.handle()
async def handle_first_receive(bot: Bot, event: Event):
    user_id = int(event.get_user_id())
    # if not warden.wa(str(user_id)):
    #     await mag_search.send(Message(f'[CQ:at, qq={int(user_id)}] 找wsh申请权限~'))
    message = event.get_message()
    key_word = str(message).strip().split(' ')[1].encode('utf-8')
    res = sp.search_res(key_word)
    await mag_search.send(message=Message(f'[CQ:at,qq={int(user_id)}]'
                                          + f"\n {str(key_word.decode('utf-8'))} 磁链搜索结果如下：{res}"))