"""
G-Muter Plugin for userbot. //Needs MongoDB to work.
cmds: .gmute user_id|reply to user messsage	//G-Mutes a User.
	  .ungmute user_id|reply to user messsage //Un-Gmutes a User.
	  .listgmuted //List Currently G-Muted Users.
By:- JaskaranSM ( @Zero_cool7870 )
"""

import logging

from pymongo import MongoClient
from sample_config import Config
from telethon import events
from userbot import bot
from userbot.util import admin_cmd

logging.basicConfig(level=logging.INFO)


MONGO_URI = Config.MONGO_DB_URI


if MONGO_URI is None:
    logging.error("ADD MONGO_URI in Env Vars Plox.")
try:
    clnt = MongoClient(MONGO_URI)
    db = clnt["Userbot"]["gmute"]
    muted = db.muted
except Exception as e:
    logging.error(str(e))


@bot.on(admin_cmd(pattern="gmute ?(.*)", allow_sudo=True))
async def gmute_user(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    me = await bot.get_me()
    if not event.reply_to_msg_id and not input_str:
        await event.edit("`Give a User id or Reply To a User Message To Mute.`")
        return
    if event.reply_to_msg_id:
        msg = await event.get_reply_message()
        user_id = msg.sender_id
    else:
        user_id = int(input_str)

    await event.edit("`Getting a duct tape..`")
    try:
        chat = await event.get_chat()
        is_admin = chat.admin_rights
        is_creator = chat.creator
    except:
        await event.edit("`You Need to Run this command in a Group Chat.`")
        return
    if is_admin or is_creator:
        try:
            c = muted.find({})
            for i in c:
                if i['user_id'] == user_id:
                    await event.edit("`User is Already G-Muted.`")
                    return
            if user_id == me.id:
                await event.edit("`Cant Mute Myself..`")
                return
            muted.insert_one({'user_id': user_id})
            await event.edit("`G-Muted` [{}](tg://user?id={}).".format(str(user_id), str(user_id)))
            logging.info("G-Muted {}".format(str(user_id)))
        except Exception as e:
            logging.error(str(e))
            await event.edit("Error: "+str(e))
            return
    else:
        await event.edit("`You are not admin Here.`")


@bot.on(admin_cmd(pattern="ungmute ?(.*)", allow_sudo=True))
async def un_gmute_user(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    if not event.reply_to_msg_id and not input_str:
        await event.edit("`Give a User id or Reply To a User Message To Mute.`")
        return
    if event.reply_to_msg_id:
        msg = await event.get_reply_message()
        user_id = msg.sender_id
    else:
        user_id = int(input_str)
    await event.edit("`Removing Duct Tape from User's Mouth.`")
    try:
        muted.delete_one({'user_id': user_id})
        await event.edit("`Un-Gmuted` [{}](tg://user?id={}).".format(str(user_id), str(user_id)))
        logging.info("Un-Gmuted {}".format(str(user_id)))
    except Exception as e:
        logging.error(str(e))
        await event.edit("Error: "+str(e))


@bot.on(admin_cmd(pattern="listgmuted", allow_sudo=True))
async def list_gmuted(event):
    if event.fwd_from:
        return
    try:
        cur = muted.find({})
        msg = "**G-Muted Users:**\n"
        for c in cur:
            msg += "__User:__ `"+str(c['user_id'])+"`\n"
        await event.edit(msg)
    except Exception as e:
        logging.error(str(e))
        await event.edit("Error: "+str(e))


@bot.on(events.NewMessage())
async def gmute_listener(sender):
    if MONGO_URI is None:
        return
    try:
        chat = await sender.get_chat()
        is_admin = chat.admin_rights
        is_creator = chat.creator
    except:
        return
    if not is_admin and not is_creator:
        return
    try:
        curs = muted.find({})
        for c in curs:
            if c['user_id'] == sender.sender_id:
                await sender.delete()
    except Exception as e:
        logging.error(str(e))
