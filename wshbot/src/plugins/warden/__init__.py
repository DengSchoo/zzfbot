import re

from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.rule import to_me
from nonebot.matcher import Matcher
from nonebot.adapters.onebot.v11.message import Message
from nonebot.params import Arg, CommandArg, ArgPlainText

super_user = 1425123490
admins = {2787614041, 1425123490}
users = {2787614041, 1425123490}


def message_processor(user, cmd: str, target: list):

    if cmd == 'add':
        return add_usr(target)

    if cmd == 'rm':
        return rmv_usr(target)



def add_usr(userid: list):
    for item in userid:
        users.add(int(item))
    return '添加成功'

def rmv_usr(userid: list):
    for item in userid:
        users.discard(int(item))
    return '删除成功'


def Warden_User(id: int) -> bool:
    # 判断是否是wly
    return id in users


def Warden_admin(id: int) -> bool:
    # 判断是否是wly
    return id in admins


def Warden_messgae(id):
    # 判断是否是wly
    if id in admins:
        return True
    return False


warden = on_command("warden", aliases={"wd"}, priority=5)


@warden.handle()
async def handle_first_receive(bot: Bot, event: Event):
    user_id = int(event.get_user_id())
    # if not wd.warden_id(str(user_id)):
    #     await mag_search.send(Message(f'[CQ:at, qq={int(user_id)}] √ ⑧ who?'))
    if Warden_admin(user_id):
        message = event.get_message()
        splits = str(message).strip().split(' ')
        if len(splits) < 2:
            return warden.send(message=Message(f'[CQ:at,qq={int(user_id)}]' + '缺少参数'))
        cmd = splits[1]
        comp = re.compile('\d+')
        target = comp.findall(''.join(splits[2:]))
        msg = message_processor(user_id, cmd, target)
        ret_msg = ''
        for item in target:
            ret_msg += f'[CQ:at,qq={int(item)}]'
        return await warden.send(message=Message(f'[CQ:at,qq={int(user_id)}]\n' + ret_msg
                                                 + f"\n权限更改成功：{msg}"))
    await warden.send(message=Message(f'[CQ:at,qq={int(user_id)}]' + '权限不足'))
