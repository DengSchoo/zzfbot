from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.rule import to_me
from nonebot.matcher import Matcher
from nonebot.adapters import Message
from nonebot.params import Arg, CommandArg, ArgPlainText

from . import warden as wd
from . import spider as sp
mag_search = on_command("mag_search", rule=to_me(), aliases={"磁链", "磁力", "magnet", "磁链搜索", "磁力搜索"}, priority=5)

lovers = ['123', '1425123490']





@mag_search.handle()
async def handle_first_receive(bot: Bot, event: Event):
    user_id = event.get_user_id
    if not wd.warden_id(user_id):
        await mag_search.finish(Message(f'[CQ:at, qq={user_id}] √ ⑧ who?'))
    message = event.get_message
    key_word = str(message).encode('utf-8')
    res = sp.search_res(key_word)
    await mag_search.finish(Message(f'[CQ:at, qq={user_id}] \n {str(event.get_message)}磁链搜索结果如下：{res}'))
