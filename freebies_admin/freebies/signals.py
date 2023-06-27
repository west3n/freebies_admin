import os

import aiogram.utils.exceptions
import decouple
from aiogram import Bot
from asgiref.sync import async_to_sync
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import SendMessage
import psycopg2


def connect():
    try:
        db = psycopg2.connect(
            host=decouple.config("DB_HOST"),
            database=decouple.config("DB_NAME"),
            user=decouple.config("DB_USER"),
            password=decouple.config("DB_PASS")
        )
        cur = db.cursor()
        return db, cur
    except:
        db = psycopg2.connect(
            host=decouple.config("DB_HOST"),
            database=decouple.config("DB_NAME"),
            user=decouple.config("DB_USER"),
            password=decouple.config("DB_PASS")
        )
        cur = db.cursor()
        return db, cur


def get_users_list():
    db, cur = connect()
    try:
        cur.execute("SELECT tg FROM freebies_userprofile")
        return [user[0] for user in cur.fetchall()]
    finally:
        db.close()
        cur.close()


@receiver(post_save, sender=SendMessage)
def send_message_for_all(sender, instance, **kwargs):
    path = 'C:/Users/miros/Documents/PycharmProjects/freebies_admin/freebies_admin/'

    async def send_message():
        bot = Bot(decouple.config("BOT_TOKEN"))
        session = await bot.get_session()
        all_id = get_users_list()
        text = ''
        if instance.message_type == 'ad':
            text = f'<em>Реклама:</em> \n{instance.text}'
        if instance.message_type == 'admin':
            text = f'<em>Сообщение от администратора:</em> \n{instance.text}'
        if instance.message_type == 'regular':
            text = instance.text
        if instance.image:
            for tg_id in all_id:
                try:
                    await bot.send_photo(chat_id=tg_id,
                                         photo=open(f'{instance.image}', 'rb'),
                                         caption=text,
                                         parse_mode=aiogram.types.ParseMode.HTML)
                except aiogram.utils.exceptions.BotBlocked as e:
                    print(f"{tg_id} - {e}")
            os.remove(f'{path}{instance.image}')
        else:
            for tg_id in all_id:
                try:
                    await bot.send_message(chat_id=tg_id,
                                           text=text,
                                           parse_mode=aiogram.types.ParseMode.HTML)
                except aiogram.utils.exceptions.BotBlocked as e:
                    print(f"{tg_id} - {e}")
        await session.close()

    async_to_sync(send_message)()
