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


def message_processor(user, cmd, target):
    if cmd == 'add':
        add_usr(target)
        return
    if cmd == 'rm':
        rmv_usr(target)
        return


def add_usr(userid):
    users.add(userid)


def rmv_usr(userid):
    users.remove(userid)


def Warden_User(id):
    # 判断是否是wly
    if id in users:
        return True
    return False


def Warden_admin(id):
    # 判断是否是wly
    if id in admins:
        return True
    return False


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
        cmd = splits[1].encode('utf-8')
        comp = re.compile('\d+')
        target = int(comp.findall(str(message).strip().split(' ')[2])[0])
        message_processor(user_id, cmd, target)
        return await warden.send(message=Message(f'[CQ:at,qq={int(user_id)}]' + f'[CQ:at,qq={int(target)}]'
                                                 + f"权限更改成功"))
    await warden.send(message=Message(f'[CQ:at,qq={int(user_id)}]' + '权限不足'))
