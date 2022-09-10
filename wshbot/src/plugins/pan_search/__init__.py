from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.rule import to_me
from nonebot.matcher import Matcher
from nonebot.adapters.onebot.v11.message import Message
from nonebot.params import Arg, CommandArg, ArgPlainText
from . import pan_spider as ps
from ..warden import Warden_User

pan_search = on_command("pan_search", aliases={"网盘",  "网盘搜索", "ps"}, priority=5)

@pan_search.handle()
async def handle_first_receive(bot: Bot, event: Event):
    user_id = int(event.get_user_id())
    if not Warden_User(int(user_id)):
        return await pan_search.send(Message(f'[CQ:at,qq={int(user_id)}]' + '找王姐或者wsh申请权限~'))
    message = event.get_message()
    splits = str(message).strip().split(' ')
    key_word = ', '.join(splits[1:])
    #search_key = ' '.join(splits[1:])
    # 返回结果
    res = ps.pan_res_search(str(message).strip())
    return await pan_search.send(message=Message(f'[CQ:at,qq={int(user_id)}]'
                                          + f"\n {str(key_word)} 网盘搜索结果如下：\n{res}"))


pan_search_help = on_command("pan_help", aliases={"网盘搜索帮助", "pan_help"}, priority=5)

tab_str = "\t\t"

help_str = "云盘搜索帮助：\n" + f"{tab_str}【格式】：pan_search/ps 网盘源 搜索内容 排序 文件类型\n"
help_source = f"{tab_str}【网盘源】: 阿里云：aliyun/al、百度网盘：baidu/bd\n"
help_content = f"{tab_str}【内容】：搜索内容，多内容用+连接\n"
help_div = f"{tab_str}-------从以下部分开始为可选内容----------\n"
help_sort = f"{tab_str}【排序】: 默认、时间(降序)、精确\n"
help_type = f"{tab_str}【文件类型】: 全部类型, 视频, 音乐, 图片, 文档, 压缩包, 其它, 文件夹\n\n"
help_exp1 = f"{tab_str}例：纯净搜索\n{tab_str}{tab_str}ps al 数据结构\n"
help_exp2 = f"{tab_str}例：排序，\n{tab_str}{tab_str}ps al 数据结构 精确\n"
help_exp3 = f"{tab_str}例：文件类型，\n{tab_str}{tab_str}ps al 数据结构 默认 视频\n"
help_exp4 = f"{tab_str}例：排序+文件类型，\n{tab_str}{tab_str}ps al 数据结构 时间 文档\n"




@pan_search_help.handle()
async def handle_first_receive(bot: Bot, event: Event):
    user_id = int(event.get_user_id())
    help = help_str + help_source + help_content + help_div + help_sort + help_type \
           + help_exp1 + help_exp2 + help_exp3 + help_exp4
    return await pan_search_help.send(message=Message(f'[CQ:at,qq={int(user_id)}]'
                                          + f"\n{help}"))