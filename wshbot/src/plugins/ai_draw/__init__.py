# python3
# -*- coding: utf-8 -*-
# @Time    : 2022/12/3 22:25
# @Author  : yzyyz
# @Email   :  youzyyz1384@qq.com
# @File    : __init__.py.py
# @Software: PyCharm
import json
import re
import httpx
from nonebot import on_command, logger, get_driver
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import ActionFailed
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, MessageSegment, Event, GroupMessageEvent, PrivateMessageEvent
from nonebot.internal.matcher import Matcher
from nonebot.internal.params import ArgStr, ArgPlainText
from nonebot.params import CommandArg
from nonebot.typing import T_State
from .source_data import ask_url

aidraw = on_command(".draw", aliases={".aidraw", ".naifu"}, priority=2, block=True)


@aidraw.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State, matcher: Matcher, args: Message = CommandArg()):
    if isinstance(event, GroupMessageEvent):
        if event.group_id == 485496634:
            await aidraw.finish("当前群无法使用AI绘画")
    if args:
        args = str(args)
        porn_word_list = ['sexy', 'nude', 'denudate', 'without clothes', 'lustful', 'trannsexual', 'semen', 'vaginal',
                          'vagina', 'penis', 'reproductive organs', 'fucked silly', 'fuck', 'pussy', 'pussy juice',
                          'naked apron', 'naked']
        filter_text = ""
        is_limited = False
        for w in porn_word_list:
            if w in args:
                is_limited = True
                args.replace(w, "")
                filter_text += w + ","
            if w.upper() in args:
                is_limited = True
                args.replace(w, "")
                filter_text += w + ","
        if is_limited:
            await aidraw.send(MessageSegment.reply(event.message_id) + f"已过滤{filter_text}")
        model = 1
        seed = ''
        await aidraw.send(f"请稍后..")
        if '模型2' in args:
            args.replace("模型2", "")
            model = 2
        if '-seed' in args:
            seed = re.compile(r'-seed\s*(\d*)').findall(args)[0]
            args.replace("-seed", "")
        if '-best' in args:
            args.replace("-best", "")
            args += "masterpiece,best quality,official art,extremely detailed CG unity 8k wallpaper, "
        res = await ask_url(args, model, seed)
        if res:
            try:
                img = f"https://novelai.8zyw.cn/{res['url']}"
                logger.info(f"AI绘画图片地址：{img}")
                r = ""
                r += f"\n{res['seed']}"
                await aidraw.send(MessageSegment.reply(event.message_id) + MessageSegment.image(img) + r)
            except Exception as e:
                await aidraw.finish(MessageSegment.reply(event.message_id) + "生成出错了~")
        else:
            await aidraw.finish(MessageSegment.reply(event.message_id) + "生成出错了~")
    else:
        await aidraw.finish(MessageSegment.reply(event.message_id) + "请输入内容")


draw_help = on_command("draw_help", aliases={"画图帮助", "aidraw_help"}, priority=2, block=True)


@draw_help.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State, matcher: Matcher, args: Message = CommandArg()):
    await draw_help.finish(
        "AI绘画插件使用方法：\n"
        f"{'-' * 30}\n"
        ".draw [内容] -seed [种子] 模型2 -best\n\n"
        "例如：\n"
        "● 最简单用例：\n"
        "      .draw cat\n\n"
        "● 使用 safe-diffusion 模型：\n"
        "      .draw cat 模型2\n\n"
        "● 使用指定种子：\n"
        "      .draw cat -seed123456\n(每张图片后的数字就是种子)\n\n"
        "● 使用指定种子和模型2：\n"
        "      .draw cat -seed123456 模型2\n\n"
        "● 高质量关键词\n"
        "      .draw cat -best\n"
        "      -best 代表【masterpiece,best quality,official art,extremely detailed CG unity 8k wallpaper,】\n"
        "发送【镜头】、【效果】可获取相关标签\n"

    )


draw_clear = on_command("draw_clear", aliases={"画图清空", "aidraw_clear"}, priority=2, block=True)


@draw_clear.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State, matcher: Matcher, args: Message = CommandArg()):
    async with httpx.AsyncClient() as client:
        res = await client.get("https://ai.8zyw.club/ajax.php?act=clear")
        if res.status_code == 200:
            await draw_clear.finish(f"{res.json()['msg']}")
        else:
            await draw_clear.finish(f"{res.json()['msg']}")
