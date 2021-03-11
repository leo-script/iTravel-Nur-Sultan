#! /usr/bin/env python
# -*- coding: utf-8 -*-


# LIBRARIES: -----------------------------------------------------------------------------
from urllib.request import urlopen
#from bs4 import BeautifulSoup as bs
#from selenium import webdriver
import pandas as pd
import random
import xml.etree.ElementTree as ET
import sys
from datetime import datetime
import asyncio
import logging
import psycopg2
import requests
from psycopg2 import OperationalError
from aiogram.utils.markdown import hlink
from aiogram import Bot, Dispatcher, executor, types 
from aiogram.types import ReplyKeyboardRemove as rem_kb, ReplyKeyboardMarkup, InlineKeyboardMarkup, \
    KeyboardButton, InlineKeyboardButton, ParseMode, InputMediaPhoto, InputMediaVideo, ChatActions, InputFile, message
from aiogram.utils.markdown import text , bold, italic, code, pre
from aiogram.utils.emoji import emojize


# BOT SETTINGS: --------------------------------------------------------------------------

# Enable logging:
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher 
bot = Bot(token='***********')
dp = Dispatcher(bot)


# READING: -------------------------------------------------------------------------------

root = ET.parse('strings.xml').getroot()
s = root


# GLOBAL VARIABLES -----------------------------------------------------------------------

STATE = {}
LANG = {}
txt = {}

# KEYBOARDS ------------------------------------------------------------------------------

rem_kb = types.ReplyKeyboardRemove()

# Making language keyboard
bt_lang_1 = KeyboardButton(emojize(s[0][0][1].text))
bt_lang_2 = KeyboardButton(emojize(s[0][0][2].text))
bt_lang_3 = KeyboardButton(emojize(s[0][0][3].text))
bt_lang_4 = KeyboardButton(emojize(s[0][0][4].text))
lang_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).row(
    bt_lang_1, bt_lang_2).row(bt_lang_3, bt_lang_4)

# Making main menu
bt_menu_services_rus = KeyboardButton(emojize(s[1][0][2].text))
bt_menu_settings_rus = KeyboardButton(emojize(s[1][0][3].text))
bt_menu_changelang_rus = KeyboardButton(emojize(s[1][0][4].text))
bt_menu_about_rus = KeyboardButton(emojize(s[1][0][5].text))

kb_menu_rus = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(
    bt_menu_services_rus).add(bt_menu_settings_rus).add(bt_menu_changelang_rus).add(bt_menu_about_rus)

kb_menu = {}

# Services menu
ibt_services_0_rus = InlineKeyboardButton(emojize(s[1][0][6].text), callback_data='services_bt0')
ibt_services_1_rus = InlineKeyboardButton(emojize(s[1][0][7].text), callback_data='services_bt1')
ibt_services_2_rus = InlineKeyboardButton(emojize(s[1][0][8].text), callback_data='services_bt2')
ibt_services_3_rus = InlineKeyboardButton(emojize(s[1][0][9].text), callback_data='services_bt3')
ibt_services_4_rus = InlineKeyboardButton(emojize(s[1][0][14].text), callback_data='services_bt4')


ikb_services_rus = InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(
    ibt_services_0_rus).add(ibt_services_1_rus).add(ibt_services_2_rus).add(ibt_services_3_rus).add(ibt_services_4_rus)

ikb_services = {}

# Slider
ibt_slider_prev_rus = InlineKeyboardButton(emojize(s[1][0][11].text), parse_mode='html', callback_data='prev')
ibt_slider_next_rus = InlineKeyboardButton(emojize(s[1][0][12].text), parse_mode='html', callback_data='next')
ibt_slider_back_rus = InlineKeyboardButton(emojize(s[1][0][13].text), parse_mode='html', callback_data='back')
ibt_slider_taxi_rus = InlineKeyboardButton(emojize(s[1][0][17].text), callback_data='taxi')
ibt_slider_route_rus = InlineKeyboardButton(emojize(s[1][0][18].text), callback_data='route')
ibt_slider_more_rus = InlineKeyboardButton(emojize(s[1][0][19].text), callback_data='more')
ibt_slider_reviews_rus = InlineKeyboardButton(emojize(s[1][0][20].text), callback_data='reviews')
ibt_slider_airquality_rus = InlineKeyboardButton(emojize(s[1][0][21].text), callback_data='air_quality')

ikb_slider_rus = InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, parse_mode='html').row(
    ibt_slider_prev_rus, ibt_slider_next_rus).row(ibt_slider_taxi_rus, ibt_slider_route_rus).row(ibt_slider_more_rus, ibt_slider_reviews_rus).add(ibt_slider_airquality_rus).add(ibt_slider_back_rus)

ikb_slider = {}

# Button "BACK" for video 4K about Astana
ibt_video_back_rus = InlineKeyboardButton(emojize(s[1][0][13].text), callback_data='back_video')
ibt_video_rus = InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(ibt_video_back_rus)
ibt_video = {}
# Button "Back" for services in slider
ibt_attractions_back_rus = InlineKeyboardButton(emojize(s[1][0][13].text), parse_mode='html', callback_data='back_attractions')
ibt_attractions_back_rus_markup = InlineKeyboardMarkup(resize_keyboard=True, parse_mode='html').add(ibt_attractions_back_rus)
ibt_attractions_back = {}

# Button "Route" in services for attractions
ibt_attractions_location_rus = KeyboardButton("Отправить геолокацию", request_location=True)
ibt_attractions_route_back_rus = InlineKeyboardButton(emojize(s[1][0][13].text), parse_mode='html', callback_data='back_attractions')
ibt_attractions_location = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(ibt_attractions_location_rus)
request_location = {}
ibt_attractions_route_markup = InlineKeyboardMarkup(resize_keyboard=True, parse_mode='html').add(ibt_attractions_route_back_rus)
ibt_attractions_route_back = {}

# FUNCTIONS

def change_lang(id, lang):
    if lang == 'RUS':
        LANG[id] = 'RUS'
        txt[id] = s[1]
        kb_menu[id] = kb_menu_rus
        ikb_services[id] = ikb_services_rus
        ikb_slider[id] = ikb_slider_rus
        ibt_video[id] = ibt_video_rus
        ibt_attractions_back[id] = ibt_attractions_back_rus_markup
        ibt_attractions_route_back[id] = ibt_attractions_route_markup
        request_location[id] = ibt_attractions_location
    elif lang == 'ENG':
        LANG[id] = 'ENG'
        txt[id] = s[2]
    elif lang == 'KAZ':
        LANG[id] = 'KAZ'
        txt[id] = s[3]
    elif lang == 'CHN':
        LANG[id] = 'CHN'
        txt[id] = s[4]

# LISTENERS
# Starting
@dp.message_handler(commands=['start', 'restart', 'reboot'])
async def echo(message: types.Message):
    u = message.from_user
    await message.answer(emojize(s[0][0][0].text), reply_markup=lang_kb)
    STATE[u.id] = 'STARTING_LANG'

# @dp.message_handler(commands='api')
# async def echo(message: types.Message):
#     u = message.from_user
#     for x in range(5):
#         driver = webdriver.Firefox(executable_path=r'geckodriver.exe')
#         driver.get('https://api.smart.astana.kz/ru/services/ecology/Data-on-air-quality/?show=INDICATORS')
#         temperature = driver.find_elements_by_class_name('temperature')
#         datetime = driver.find_elements_by_class_name('datetime')
#         value = driver.find_elements_by_class_name('value')
#         # 0 - wind  1 - press  2 - оксид азота 3 - диоксид азота
#         # 4 - оксид углерода 5 - диоксид серы 6 - сероводород
#         # 7 - взвешанные частицы рм10 8 -  рм 2,5
#         # 9 - wind 10 - press 19
#         msg = text(temperature[x].text, " | ", datetime[x].text, " | ", value[9*x].text, " | ",
#             value[9*x + 1].text, " | ", value[9*x + 2].text, " | ", value[9*x + 3].text, " | ",
#             value[9*x + 4].text, " | ", value[9*x + 5].text, " | ", value[9*x + 6].text, " | ",
#             value[9*x + 7].text, " | ", value[9*x + 8].text, " | ")
#
#         driver.close()
#         await message.answer(msg)


# Language
@dp.message_handler(text=[emojize(s[0][0][1].text),
    emojize(s[0][0][2].text),emojize(s[0][0][3].text),emojize(s[0][0][4].text)])
async def echo(message: types.Message):
    u = message.from_user
    if STATE[u.id] == 'STARTING_LANG':
        if message.text == emojize(s[0][0][1].text):
            change_lang(u.id, 'RUS')
        elif message.text == emojize(s[0][0][2].text):
            change_lang(u.id, 'ENG')
        elif message.text == emojize(s[0][0][3].text):
            change_lang(u.id, 'KAZ')
        elif message.text == emojize(s[0][0][4].text):
            change_lang(u.id, 'CHN')
        msg = text(emojize(txt[u.id][0][0].text), f'<b>{u.first_name}!</b>', '\n', emojize(txt[u.id][0][1].text))
        await message.answer(msg, reply_markup=kb_menu[u.id], parse_mode='html')
        STATE[u.id] = 'MENU'

# Menu
@dp.message_handler(text=[emojize(s[1][0][2].text)])
async def echo(message: types.Message):
    u = message.from_user
    await message.answer(emojize(s[1][0][10].text), reply_markup=ikb_services[u.id])
    STATE[u.id] = 'SERV'

@dp.message_handler(text=[emojize(s[1][0][3].text)])
async def echo(message: types.Message):
    u = message.from_user
    await bot.send_message(u.id, "В разработке")

@dp.message_handler(text=[emojize(s[1][0][4].text)])
async def echo(message: types.Message):
    u = message.from_user
    await message.answer(emojize(s[0][0][0].text), reply_markup=lang_kb)
    STATE[u.id] = 'STARTING_LANG'

@dp.message_handler(text=[emojize(s[1][0][5].text)])
async def echo(message: types.Message):
    u = message.from_user
    await message.answer(emojize(s[1][0][16].text), reply_markup=kb_menu[u.id], parse_mode='html')


# Getting photo ID
@dp.message_handler(content_types=['photo'])
async def handle_docs_photo(message):
    await message.answer(message.photo[-1].file_id)

# Getting video ID
@dp.message_handler(content_types=['video'])
async def handle_docs_photo(message):
    await message.answer(message.video.file_id)


# INLINE CALLBACKS

# Services:
@dp.callback_query_handler(lambda c: c.data == 'services_bt0')
async def process_callback_button1(callback_query: types.CallbackQuery):
    u = callback_query.from_user
    if STATE[u.id] == 'SERV':
        await bot.answer_callback_query(callback_query.id)
        # send photo of baiterek at night
        await bot.send_photo(u.id, txt[u.id][1][0][2].text)
        await bot.send_message(u.id, txt[u.id][1][0][0].text, reply_markup=ikb_slider[u.id], parse_mode='html')
        STATE[u.id] = 'SLIDER_0'

@dp.callback_query_handler(lambda c: c.data == 'services_bt1')
async def process_callback_button1(callback_query: types.CallbackQuery):
    u = callback_query.from_user
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(u.id, 'В разработке: вторая кнопка!')

@dp.callback_query_handler(lambda c: c.data == 'services_bt2')
async def process_callback_button1(callback_query: types.CallbackQuery):
    u = callback_query.from_user
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(u.id, 'В разработке: третья кнопка!')

@dp.callback_query_handler(lambda c: c.data == 'services_bt3')
async def process_callback_button1(callback_query: types.CallbackQuery):
    u = callback_query.from_user
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(u.id, 'В разработке: четвертая кнопка!')

@dp.callback_query_handler(lambda c: c.data == 'services_bt4')
async def process_callback_button1(callback_query: types.CallbackQuery):
    u = callback_query.from_user
    await bot.answer_callback_query(callback_query.id)
    await bot.send_video(u.id, txt[u.id][0][15].text, reply_markup=ibt_video[u.id])


# Slider:
@dp.callback_query_handler(lambda c: c.data == 'prev')
async def process_callback_button1(callback_query: types.CallbackQuery):
    u = callback_query.from_user
    if STATE[u.id] == 'SLIDER_0':
        pass
    elif STATE[u.id] == 'SLIDER_1':
        await bot.edit_message_text(txt[u.id][1][0][0].text, u.id, callback_query.message.message_id, reply_markup = ikb_slider[u.id], parse_mode='html')
        await bot.edit_message_media(InputMediaPhoto(txt[u.id][1][0][2].text), u.id, callback_query.message.message_id - 1)
        STATE[u.id] = 'SLIDER_0'

    elif STATE[u.id] == 'SLIDER_2':
        await bot.edit_message_text(txt[u.id][1][1][0].text, u.id, callback_query.message.message_id,
                                    reply_markup=ikb_slider[u.id], parse_mode='html')
        await bot.edit_message_media(InputMediaPhoto(txt[u.id][1][1][1].text), u.id,
                                     callback_query.message.message_id - 1)
        STATE[u.id] = 'SLIDER_1'

    elif STATE[u.id] == 'SLIDER_3':
        await bot.edit_message_text(txt[u.id][1][2][0].text, u.id, callback_query.message.message_id,
                                    reply_markup=ikb_slider[u.id], parse_mode='html')
        await bot.edit_message_media(InputMediaPhoto(txt[u.id][1][2][1].text), u.id,
                                     callback_query.message.message_id - 1)
        STATE[u.id] = 'SLIDER_2'

    elif STATE[u.id] == 'SLIDER_4':
        await bot.edit_message_text(txt[u.id][1][3][0].text, u.id, callback_query.message.message_id,
                                    reply_markup=ikb_slider[u.id], parse_mode='html')
        await bot.edit_message_media(InputMediaPhoto(txt[u.id][1][3][1].text), u.id,
                                     callback_query.message.message_id - 1)
        STATE[u.id] = 'SLIDER_3'
    elif STATE[u.id] == 'SLIDER_5':
        await bot.edit_message_text(txt[u.id][1][4][0].text, u.id, callback_query.message.message_id,
                                    reply_markup=ikb_slider[u.id], parse_mode='html')
        await bot.edit_message_media(InputMediaPhoto(txt[u.id][1][4][1].text), u.id,
                                     callback_query.message.message_id - 1)
        STATE[u.id] = 'SLIDER_4'
    elif STATE[u.id] == 'SLIDER_6':
        await bot.edit_message_text(txt[u.id][1][5][0].text, u.id, callback_query.message.message_id,
                                    reply_markup=ikb_slider[u.id], parse_mode='html')
        await bot.edit_message_media(InputMediaPhoto(txt[u.id][1][5][1].text), u.id,
                                     callback_query.message.message_id - 1)
        STATE[u.id] = 'SLIDER_5'
    elif STATE[u.id] == 'SLIDER_7':
        await bot.edit_message_text(txt[u.id][1][6][0].text, u.id, callback_query.message.message_id,
                                    reply_markup=ikb_slider[u.id], parse_mode='html')
        await bot.edit_message_media(InputMediaPhoto(txt[u.id][1][6][1].text), u.id,
                                     callback_query.message.message_id - 1)
        STATE[u.id] = 'SLIDER_6'
    elif STATE[u.id] == 'SLIDER_8':
        await bot.edit_message_text(txt[u.id][1][7][0].text, u.id, callback_query.message.message_id,
                                    reply_markup=ikb_slider[u.id], parse_mode='html')
        await bot.edit_message_media(InputMediaPhoto(txt[u.id][1][7][1].text), u.id,
                                     callback_query.message.message_id - 1)
        STATE[u.id] = 'SLIDER_7'
    elif STATE[u.id] == 'SLIDER_9':
        await bot.edit_message_text(txt[u.id][1][8][0].text, u.id, callback_query.message.message_id,
                                    reply_markup=ikb_slider[u.id], parse_mode='html')
        await bot.edit_message_media(InputMediaPhoto(txt[u.id][1][8][1].text), u.id,
                                     callback_query.message.message_id - 1)
        STATE[u.id] = 'SLIDER_8'
    else:
        pass

@dp.callback_query_handler(lambda c: c.data == 'next')
async def process_callback_button1(callback_query: types.CallbackQuery):
    u = callback_query.from_user
    if STATE[u.id] == 'SLIDER_0':
        await bot.edit_message_text(txt[u.id][1][1][0].text, u.id, callback_query.message.message_id, reply_markup=ikb_slider[u.id], parse_mode='html')
        await bot.edit_message_media(InputMediaPhoto(txt[u.id][1][1][1].text), u.id, callback_query.message.message_id - 1)
        STATE[u.id] = 'SLIDER_1'
    elif STATE[u.id] == 'SLIDER_1':
        await bot.edit_message_text(txt[u.id][1][2][0].text, u.id, callback_query.message.message_id, reply_markup=ikb_slider[u.id], parse_mode='html')
        await bot.edit_message_media(InputMediaPhoto(txt[u.id][1][2][1].text), u.id, callback_query.message.message_id - 1)
        STATE[u.id] = 'SLIDER_2'
    elif STATE[u.id] == 'SLIDER_2':
        await bot.edit_message_text(txt[u.id][1][3][0].text, u.id, callback_query.message.message_id, reply_markup=ikb_slider[u.id], parse_mode='html')
        await bot.edit_message_media(InputMediaPhoto(txt[u.id][1][3][1].text), u.id, callback_query.message.message_id - 1)
        STATE[u.id] = 'SLIDER_3'
    elif STATE[u.id] == 'SLIDER_3':
        await bot.edit_message_text(txt[u.id][1][4][0].text, u.id, callback_query.message.message_id,
                                    reply_markup=ikb_slider[u.id], parse_mode='html')
        await bot.edit_message_media(InputMediaPhoto(txt[u.id][1][4][1].text), u.id,
                                     callback_query.message.message_id - 1)
        STATE[u.id] = 'SLIDER_4'
    elif STATE[u.id] == 'SLIDER_4':
        await bot.edit_message_text(txt[u.id][1][5][0].text, u.id, callback_query.message.message_id,
                                    reply_markup=ikb_slider[u.id], parse_mode='html')
        await bot.edit_message_media(InputMediaPhoto(txt[u.id][1][5][1].text), u.id,
                                     callback_query.message.message_id - 1)
        STATE[u.id] = 'SLIDER_5'
    elif STATE[u.id] == 'SLIDER_5':
        await bot.edit_message_text(txt[u.id][1][6][0].text, u.id, callback_query.message.message_id,
                                    reply_markup=ikb_slider[u.id], parse_mode='html')
        await bot.edit_message_media(InputMediaPhoto(txt[u.id][1][6][1].text), u.id,
                                     callback_query.message.message_id - 1)
        STATE[u.id] = 'SLIDER_6'
    elif STATE[u.id] == 'SLIDER_6':
        await bot.edit_message_text(txt[u.id][1][7][0].text, u.id, callback_query.message.message_id,
                                    reply_markup=ikb_slider[u.id], parse_mode='html')
        await bot.edit_message_media(InputMediaPhoto(txt[u.id][1][7][1].text), u.id,
                                     callback_query.message.message_id - 1)
        STATE[u.id] = 'SLIDER_7'
    elif STATE[u.id] == 'SLIDER_7':
        await bot.edit_message_text(txt[u.id][1][8][0].text, u.id, callback_query.message.message_id,
                                    reply_markup=ikb_slider[u.id], parse_mode='html')
        await bot.edit_message_media(InputMediaPhoto(txt[u.id][1][8][1].text), u.id,
                                     callback_query.message.message_id - 1)
        STATE[u.id] = 'SLIDER_8'
    elif STATE[u.id] == 'SLIDER_8':
        await bot.edit_message_text(txt[u.id][1][9][0].text, u.id, callback_query.message.message_id,
                                    reply_markup=ikb_slider[u.id], parse_mode='html')
        await bot.edit_message_media(InputMediaPhoto(txt[u.id][1][9][1].text), u.id,
                                     callback_query.message.message_id - 1)
        STATE[u.id] = 'SLIDER_9'
    elif STATE[u.id] == 'SLIDER_9':
        pass
    else:
        pass
@dp.callback_query_handler(lambda c: c.data == 'back')
async def go_back (callback_query: types.CallbackQuery):
    u = callback_query.from_user
    await bot.send_message(u.id, emojize(s[1][0][10].text), reply_markup=ikb_services[u.id])
    STATE[u.id] = 'SERV'
# Taxi
@dp.callback_query_handler(lambda c: c.data == 'taxi')
async def taxi(callback_query: types.CallbackQuery):
    u = callback_query.from_user
    if STATE[u.id] == 'SLIDER_0':
        text = hlink('Заказать такси до Монумента Байтерек', 'https://api.whatsapp.com/send?phone=77015555555&text=%D0%97%D0%B4%D1%80%D0%B0%D0%B2%D1%81%D1%82%D0%B2%D1%83%D0%B9%D1%82%D0%B5,%20%D0%A5%D0%BE%D1%82%D0%B8%D0%BC%20%D0%B7%D0%B0%D0%BA%D0%B0%D0%B7%D0%B0%D1%82%D1%8C%20%D1%82%D0%B0%D0%BA%D1%81%D0%B8%20%D0%B4%D0%BE%20%D0%9C%D0%BE%D0%BD%D1%83%D0%BC%D0%B5%D0%BD%D1%82%D0%B0%20%D0%91%D0%B0%D0%B9%D1%82%D0%B5%D1%80%D0%B5%D0%BA!')
        await bot.send_message(u.id, text, disable_web_page_preview=True, reply_markup=ibt_attractions_back[u.id],parse_mode='html')

    elif STATE[u.id] == 'SLIDER_1':
        text = hlink('Заказать такси до Монумента "Ханшатыр"', 'https://api.whatsapp.com/send?phone=77015555555&text=%D0%97%D0%B4%D1%80%D0%B0%D0%B2%D1%81%D1%82%D0%B2%D1%83%D0%B9%D1%82%D0%B5,%20%D0%A5%D0%BE%D1%82%D0%B8%D0%BC%20%D0%B7%D0%B0%D0%BA%D0%B0%D0%B7%D0%B0%D1%82%D1%8C%20%D1%82%D0%B0%D0%BA%D1%81%D0%B8%20%D0%B4%D0%BE%20%D0%9C%D0%BE%D0%BD%D1%83%D0%BC%D0%B5%D0%BD%D1%82%D0%B0%20%D0%A5%D0%B0%D0%BD%D1%88%D0%B0%D1%82%D1%8B%D1%80!')
        await bot.send_message(u.id, text, disable_web_page_preview=True, reply_markup=ibt_attractions_back[u.id], parse_mode='html')

    elif STATE[u.id] == 'SLIDER_2':
        text = hlink('Заказать такси до Дворца мира и согласия"', 'https://api.whatsapp.com/send?phone=77015555555&text=%D0%97%D0%B4%D1%80%D0%B0%D0%B2%D1%81%D1%82%D0%B2%D1%83%D0%B9%D1%82%D0%B5,%20%D0%A5%D0%BE%D1%82%D0%B8%D0%BC%20%D0%B7%D0%B0%D0%BA%D0%B0%D0%B7%D0%B0%D1%82%D1%8C%20%D1%82%D0%B0%D0%BA%D1%81%D0%B8%20%D0%B4%D0%BE%20%D0%94%D0%B2%D0%BE%D1%80%D1%86%D0%B0%20%D0%BC%D0%B8%D1%80%D0%B0%20%D0%B8%20%D1%81%D0%BE%D0%B3%D0%BB%D0%B0%D1%81%D0%B8%D1%8F!')
        await bot.send_message(u.id, text, disable_web_page_preview=True, reply_markup=ibt_attractions_back[u.id],parse_mode='html')

    elif STATE[u.id] == 'SLIDER_3':
        text = hlink('Заказать такси до Astana EXPO-2017"', 'https://api.whatsapp.com/send?phone=77015555555&text=%D0%97%D0%B4%D1%80%D0%B0%D0%B2%D1%81%D1%82%D0%B2%D1%83%D0%B9%D1%82%D0%B5,%20%D0%A5%D0%BE%D1%82%D0%B8%D0%BC%20%D0%B7%D0%B0%D0%BA%D0%B0%D0%B7%D0%B0%D1%82%D1%8C%20%D1%82%D0%B0%D0%BA%D1%81%D0%B8%20%D0%B4%D0%BE%20Astana%20EXPO%20-%202017!')
        await bot.send_message(u.id, text, disable_web_page_preview=True, reply_markup=ibt_attractions_back[u.id], parse_mode='html')

    elif STATE[u.id] == 'SLIDER_4':
        text = hlink('Заказать такси до РЦ "Думан"', 'https://api.whatsapp.com/send?phone=77015555555&text=%D0%97%D0%B4%D1%80%D0%B0%D0%B2%D1%81%D1%82%D0%B2%D1%83%D0%B9%D1%82%D0%B5,%20%D0%A5%D0%BE%D1%82%D0%B8%D0%BC%20%D0%B7%D0%B0%D0%BA%D0%B0%D0%B7%D0%B0%D1%82%D1%8C%20%D1%82%D0%B0%D0%BA%D1%81%D0%B8%20%D0%B4%D0%BE%20%D0%A0%D0%A6%20%D0%94%D1%83%D0%BC%D0%B0%D0%BD!')
        await bot.send_message(u.id, text, disable_web_page_preview=True, reply_markup=ibt_attractions_back[u.id], parse_mode='html')

    elif STATE[u.id] == 'SLIDER_5':
        text = hlink('Заказать такси до Набережки (Набережная реки Ишим)', 'https://api.whatsapp.com/send?phone=77015555555&text=%D0%97%D0%B4%D1%80%D0%B0%D0%B2%D1%81%D1%82%D0%B2%D1%83%D0%B9%D1%82%D0%B5,%20%D0%A5%D0%BE%D1%82%D0%B8%D0%BC%20%D0%B7%D0%B0%D0%BA%D0%B0%D0%B7%D0%B0%D1%82%D1%8C%20%D1%82%D0%B0%D0%BA%D1%81%D0%B8%20%D0%B4%D0%BE%20%D0%9D%D0%B0%D0%B1%D0%B5%D1%80%D0%B5%D0%B6%D0%BA%D0%B8%20(%D0%9D%D0%B0%D0%B1%D0%B5%D1%80%D0%B5%D0%B6%D0%BD%D0%B0%D1%8F%20%D1%80%D0%B5%D0%BA%D0%B8%20%D0%98%D1%88%D0%B8%D0%BC)!')
        await bot.send_message(u.id, text, disable_web_page_preview=True, reply_markup=ibt_attractions_back[u.id], parse_mode='html')

    elif STATE[u.id] == 'SLIDER_6':
        text = hlink('Заказать такси до Бульвара Нуржол', 'https://api.whatsapp.com/send?phone=77015555555&text=%D0%97%D0%B4%D1%80%D0%B0%D0%B2%D1%81%D1%82%D0%B2%D1%83%D0%B9%D1%82%D0%B5,%20%D0%A5%D0%BE%D1%82%D0%B8%D0%BC%20%D0%B7%D0%B0%D0%BA%D0%B0%D0%B7%D0%B0%D1%82%D1%8C%20%D1%82%D0%B0%D0%BA%D1%81%D0%B8%20%D0%B4%D0%BE%20%D0%91%D1%83%D0%BB%D1%8C%D0%B2%D0%B0%D1%80%D0%B0%20%D0%9D%D1%83%D1%80%D0%B6%D0%BE%D0%BB!')
        await bot.send_message(u.id, text, disable_web_page_preview=True, reply_markup=ibt_attractions_back[u.id], parse_mode='html')

    elif STATE[u.id] == 'SLIDER_7':
        text = hlink('Заказать такси до Площади Независимости', 'https://api.whatsapp.com/send?phone=77015555555&text=%D0%97%D0%B4%D1%80%D0%B0%D0%B2%D1%81%D1%82%D0%B2%D1%83%D0%B9%D1%82%D0%B5,%20%D0%A5%D0%BE%D1%82%D0%B8%D0%BC%20%D0%B7%D0%B0%D0%BA%D0%B0%D0%B7%D0%B0%D1%82%D1%8C%20%D1%82%D0%B0%D0%BA%D1%81%D0%B8%20%D0%B4%D0%BE%20%D0%9F%D0%BB%D0%BE%D1%89%D0%B0%D0%B4%D0%B8%20%D0%9D%D0%B5%D0%B7%D0%B0%D0%B2%D0%B8%D1%81%D0%B8%D0%BC%D0%BE%D1%81%D1%82%D0%B8!')
        await bot.send_message(u.id, text, disable_web_page_preview=True, reply_markup=ibt_attractions_back[u.id], parse_mode='html')

    elif STATE[u.id] == 'SLIDER_8':
        text = hlink('Заказать такси до Этно-мемориального комплекса "Карта Казахстана - Атамекен"', 'https://api.whatsapp.com/send?phone=77015555555&text=%D0%97%D0%B4%D1%80%D0%B0%D0%B2%D1%81%D1%82%D0%B2%D1%83%D0%B9%D1%82%D0%B5,%20%D0%A5%D0%BE%D1%82%D0%B8%D0%BC%20%D0%B7%D0%B0%D0%BA%D0%B0%D0%B7%D0%B0%D1%82%D1%8C%20%D1%82%D0%B0%D0%BA%D1%81%D0%B8%20%D0%B4%D0%BE%20%D0%AD%D1%82%D0%BD%D0%BE-%D0%BC%D0%B5%D0%BC%D0%BE%D1%80%D0%B8%D0%B0%D0%BB%D1%8C%D0%BD%D0%BE%D0%B3%D0%BE%20%D0%BA%D0%BE%D0%BC%D0%BF%D0%BB%D0%B5%D0%BA%D1%81%D0%B0%20%22%D0%9A%D0%B0%D1%80%D1%82%D0%B0%20%D0%9A%D0%B0%D0%B7%D0%B0%D1%85%D1%81%D1%82%D0%B0%D0%BD%D0%B0%20-%20%D0%90%D1%82%D0%B0%D0%BC%D0%B5%D0%BA%D0%B5%D0%BD%22!')
        await bot.send_message(u.id, text, disable_web_page_preview=True, reply_markup=ibt_attractions_back[u.id], parse_mode='html')

    elif STATE[u.id] == 'SLIDER_9':
        text = hlink('Заказать такси до Колесы обозрения "Ailand"', 'https://api.whatsapp.com/send?phone=77015555555&text=%D0%97%D0%B4%D1%80%D0%B0%D0%B2%D1%81%D1%82%D0%B2%D1%83%D0%B9%D1%82%D0%B5,%20%D0%A5%D0%BE%D1%82%D0%B8%D0%BC%20%D0%B7%D0%B0%D0%BA%D0%B0%D0%B7%D0%B0%D1%82%D1%8C%20%D1%82%D0%B0%D0%BA%D1%81%D0%B8%20%D0%B4%D0%BE%20%D0%9A%D0%BE%D0%BB%D0%B5%D1%81%D1%8B%20%D0%BE%D0%B1%D0%BE%D0%B7%D1%80%D0%B5%D0%BD%D0%B8%D1%8F%20%22Ailand%22!')
        await bot.send_message(u.id, text, disable_web_page_preview=True, reply_markup=ibt_attractions_back[u.id], parse_mode='html')

    else:
        pass

# Create a route
@dp.callback_query_handler(lambda c: c.data == 'route')
async def route(callback_query: types.CallbackQuery):
    u = callback_query.from_user
    if STATE[u.id] == 'SLIDER_0':
        await bot.send_location(u.id, 51.128260, 71.430554)
        await bot.send_message(u.id, "Чтобы проложить маршрут отправьте вашу геолокацию",
                               reply_markup=request_location[u.id], parse_mode='html')
        await bot.send_message(u.id, "Вернуть назад ⬇️", reply_markup=ibt_attractions_back[u.id], parse_mode='html')
        @dp.message_handler(content_вtypes=['location'])
        async def location(message):
            u = message.from_user
            if message.location is not None:
                client_latitude = message.location.latitude
                client_longitude = message.location.longitude
                car_route = hlink('Маршрут для поездки в "автомобиле" до Монумента Байтерек\n\n', f'https://www.google.com/maps/dir/{client_latitude},{client_longitude}/%D0%9C%D0%BE%D0%BD%D1%83%D0%BC%D0%B5%D0%BD%D1%82+%D0%91%D0%B0%D0%B9%D1%82%D0%B5%D1%80%D0%B5%D0%BA,+%D0%91%D0%B0%D0%B9%D1%82%D0%B5%D1%80%D0%B5%D0%BA,+%D0%9D%D1%83%D1%80-%D0%A1%D1%83%D0%BB%D1%82%D0%B0%D0%BD+010000/@{client_latitude},{client_longitude},14z/data=!4m9!4m8!1m0!1m5!1m1!1s0x4245841e0caadcf7:0x4f6ce0ff87111d39!2m2!1d71.4305!2d51.1283!3e0')
                bus_route = hlink('Маршрут для поездки в "автобусе" до Монумента Байтерек', f'https://www.google.com/maps/dir/{client_latitude},{client_longitude}/%D0%9C%D0%BE%D0%BD%D1%83%D0%BC%D0%B5%D0%BD%D1%82+%D0%91%D0%B0%D0%B9%D1%82%D0%B5%D1%80%D0%B5%D0%BA,+%D0%91%D0%B0%D0%B9%D1%82%D0%B5%D1%80%D0%B5%D0%BA,+%D0%9D%D1%83%D1%80-%D0%A1%D1%83%D0%BB%D1%82%D0%B0%D0%BD+010000/@{client_latitude},{client_longitude},13z/data=!3m1!4b1!4m9!4m8!1m0!1m5!1m1!1s0x4245841e0caadcf7:0x4f6ce0ff87111d39!2m2!1d71.4305!2d51.1283!3e3')
                await message.answer(car_route + bus_route, reply_markup=ibt_attractions_back[u.id], disable_web_page_preview=True, parse_mode='html')
            if message.location is None:
                await bot.send_message(u.id, "Чтобы проложить маршрут отправьте вашу геолокацию", reply_markup=request_location[u.id], parse_mode='html')

    elif STATE[u.id] == 'SLIDER_1':
        await bot.send_location(u.id, 51.132691660997885, 71.40396633211998)
        await bot.send_message(u.id, "Чтобы проложить маршрут отправьте вашу геолокацию",
                               reply_markup=request_location[u.id], parse_mode='html')
        await bot.send_message(u.id, "Вернуть назад ⬇️", reply_markup=ibt_attractions_back[u.id], parse_mode='html')
        @dp.message_handler(content_types=['location'])
        async def location(message):
            u = message.from_user
            if message.location is not None:
                client_latitude = message.location.latitude
                client_longitude = message.location.longitude
                car_route = hlink('Маршрут для поездки в "автомобиле" до Монумента Ханшатыр\n\n', f'https://www.google.com/maps/dir/{client_latitude},{client_longitude}/%D0%A5%D0%B0%D0%BD+%D0%A8%D0%B0%D1%82%D1%8B%D1%80,+%D0%BF%D1%80%D0%BE%D1%81%D0%BF%D0%B5%D0%BA%D1%82+%D0%A2%D1%83%D1%80%D0%B0%D0%BD,+%D0%9D%D1%83%D1%80-%D0%A1%D1%83%D0%BB%D1%82%D0%B0%D0%BD/@{client_latitude},{client_longitude},13z/data=!4m9!4m8!1m0!1m5!1m1!1s0x4245869b3329e1c7:0x4f8c40b27c9f9cbd!2m2!1d71.4033994!2d51.1322975!3e0')
                bus_route = hlink('Маршрут для поездки в "автобусе" до Ханшатыр', f'https://www.google.com/maps/dir/{client_latitude},{client_longitude}/%D0%A5%D0%B0%D0%BD+%D0%A8%D0%B0%D1%82%D1%8B%D1%80,+%D0%BF%D1%80%D0%BE%D1%81%D0%BF%D0%B5%D0%BA%D1%82+%D0%A2%D1%83%D1%80%D0%B0%D0%BD,+%D0%9D%D1%83%D1%80-%D0%A1%D1%83%D0%BB%D1%82%D0%B0%D0%BD/@{client_latitude},{client_longitude},13z/data=!3m1!4b1!4m9!4m8!1m0!1m5!1m1!1s0x4245869b3329e1c7:0x4f8c40b27c9f9cbd!2m2!1d71.4033994!2d51.1322975!3e3')
                await message.answer(car_route + bus_route, reply_markup=ibt_attractions_back[u.id], disable_web_page_preview=True, parse_mode='html')
            else:
                await bot.send_message(u.id, "Чтобы проложить маршрут отправьте вашу геолокацию", reply_markup=request_location[u.id], parse_mode='html')

    elif STATE[u.id] == 'SLIDER_2':
        await bot.send_location(u.id, 51.123855805595745, 71.46535629984751)
        await bot.send_message(u.id, "Чтобы проложить маршрут отправьте вашу геолокацию",
                               reply_markup=request_location[u.id], parse_mode='html')
        await bot.send_message(u.id, "Вернуть назад ⬇️", reply_markup=ibt_attractions_back[u.id], parse_mode='html')
        @dp.message_handler(content_types=['location'])
        async def location(message):
            u = message.from_user
            if message.location is not None:
                client_latitude = message.location.latitude
                client_longitude = message.location.longitude
                car_route = hlink('Маршрут для поездки в "автомобиле" до Дворца мира и согласия\n\n', f'https://www.google.com/maps/dir/{client_latitude},{client_longitude}/%D0%94%D0%B2%D0%BE%D1%80%D0%B5%D1%86+%D0%BC%D0%B8%D1%80%D0%B0+%D0%B8+%D1%81%D0%BE%D0%B3%D0%BB%D0%B0%D1%81%D0%B8%D1%8F,+%D0%BF%D1%80%D0%BE%D1%81%D0%BF.+%D0%A2%D0%B0%D1%83%D0%B5%D0%BB%D1%81%D0%B8%D0%B7%D0%B4%D0%B8%D0%BA+57,+%D0%9D%D1%83%D1%80-%D0%A1%D1%83%D0%BB%D1%82%D0%B0%D0%BD+010000/@{client_latitude},{client_longitude},13z/data=!4m9!4m8!1m0!1m5!1m1!1s0x424583f78f3b5e39:0x6d4e83fa1af51470!2m2!1d71.4635324!2d51.1231353!3e0')
                bus_route = hlink('Маршрут для поездки в "автобусе" до  Дворца мира и согласия', f'https://www.google.com/maps/dir/{client_latitude},{client_longitude}/%D0%94%D0%B2%D0%BE%D1%80%D0%B5%D1%86+%D0%BC%D0%B8%D1%80%D0%B0+%D0%B8+%D1%81%D0%BE%D0%B3%D0%BB%D0%B0%D1%81%D0%B8%D1%8F,+%D0%BF%D1%80%D0%BE%D1%81%D0%BF.+%D0%A2%D0%B0%D1%83%D0%B5%D0%BB%D1%81%D0%B8%D0%B7%D0%B4%D0%B8%D0%BA+57,+%D0%9D%D1%83%D1%80-%D0%A1%D1%83%D0%BB%D1%82%D0%B0%D0%BD+010000/@{client_latitude},{client_longitude},13z/data=!3m1!4b1!4m9!4m8!1m0!1m5!1m1!1s0x424583f78f3b5e39:0x6d4e83fa1af51470!2m2!1d71.4635324!2d51.1231353!3e3')
                await message.answer(car_route + bus_route, reply_markup=ibt_attractions_back[u.id], disable_web_page_preview=True, parse_mode='html')
            else:
                await bot.send_message(u.id, "Чтобы проложить маршрут отправьте вашу геолокацию", reply_markup=request_location[u.id], parse_mode='html')

    elif STATE[u.id] == 'SLIDER_3':
        await bot.send_location(u.id, 51.08888749213186, 71.41599764190612)
        await bot.send_message(u.id, "Чтобы проложить маршрут отправьте вашу геолокацию",
                               reply_markup=request_location[u.id], parse_mode='html')
        await bot.send_message(u.id, "Вернуть назад ⬇️", reply_markup=ibt_attractions_back[u.id], parse_mode='html')
        @dp.message_handler(content_types=['location'])
        async def location(message):
            u = message.from_user
            if message.location is not None:
                client_latitude = message.location.latitude
                client_longitude = message.location.longitude
                car_route = hlink('Маршрут для поездки в "автомобиле" до Астана EXPO-2017\n\n', f'https://www.google.com/maps/dir/{client_latitude},{client_longitude}/Nur+alemi+pavilion,+%D0%9D%D1%83%D1%80-%D0%A1%D1%83%D0%BB%D1%82%D0%B0%D0%BD+020000/@{client_latitude},{client_longitude},13z/data=!3m1!4b1!4m9!4m8!1m0!1m5!1m1!1s0x424585ab591c3049:0xe189060ca71800c2!2m2!1d71.4159631!2d51.0892196!3e0')
                bus_route = hlink('Маршрут для поездки в "автобусе" до Астана EXPO-2017', f'https://www.google.com/maps/dir/{client_latitude},{client_longitude}/Nur+alemi+pavilion,+%D0%9D%D1%83%D1%80-%D0%A1%D1%83%D0%BB%D1%82%D0%B0%D0%BD+020000/@{client_latitude},{client_longitude},13z/data=!3m1!4b1!4m9!4m8!1m0!1m5!1m1!1s0x424585ab591c3049:0xe189060ca71800c2!2m2!1d71.4159631!2d51.0892196!3e3')
                await message.answer(car_route + bus_route, reply_markup=ibt_attractions_back[u.id], disable_web_page_preview=True, parse_mode='html')
            else:
                await bot.send_message(u.id, "Чтобы проложить маршрут отправьте вашу геолокацию", reply_markup=request_location[u.id], parse_mode='html')
    elif STATE[u.id] == 'SLIDER_4':
        await bot.send_location(u.id, 51.14764332635027, 71.41766066651262)
        await bot.send_message(u.id, "Чтобы проложить маршрут отправьте вашу геолокацию",
                               reply_markup=request_location[u.id], parse_mode='html')
        await bot.send_message(u.id, "Вернуть назад ⬇️", reply_markup=ibt_attractions_back[u.id], parse_mode='html')
        @dp.message_handler(content_types=['location'])
        async def location(message):
            u = message.from_user
            if message.location is not None:
                client_latitude = message.location.latitude
                client_longitude = message.location.longitude
                car_route = hlink('Маршрут для поездки в "автомобиле" до РЦ "Думан"\n\n', f'https://www.google.com/maps/dir/{client_latitude},{client_longitude}/Duman+Aqua+Park,+%D0%9A%D1%83%D1%80%D0%B3%D0%B0%D0%BB%D1%8C%D0%B4%D0%B6%D0%B8%D0%BD%D1%81%D0%BA%D0%BE%D0%B5+%D1%88,+%D0%9D%D1%83%D1%80-%D0%A1%D1%83%D0%BB%D1%82%D0%B0%D0%BD+020000/@{client_latitude},{client_longitude},16z/data=!4m9!4m8!1m0!1m5!1m1!1s0x424586b8b3e35ea9:0x4addc8176bc7f585!2m2!1d71.4171886!2d51.1475222!3e0')
                bus_route = hlink('Маршрут для поездки в "автобусе" до РЦ "Думан"', f'https://www.google.com/maps/dir/{client_latitude},{client_longitude}/Duman+Aqua+Park,+%D0%9A%D1%83%D1%80%D0%B3%D0%B0%D0%BB%D1%8C%D0%B4%D0%B6%D0%B8%D0%BD%D1%81%D0%BA%D0%BE%D0%B5+%D1%88,+%D0%9D%D1%83%D1%80-%D0%A1%D1%83%D0%BB%D1%82%D0%B0%D0%BD+020000/@{client_latitude},{client_longitude},16z/data=!3m1!4b1!4m9!4m8!1m0!1m5!1m1!1s0x424586b8b3e35ea9:0x4addc8176bc7f585!2m2!1d71.4171886!2d51.1475222!3e3')
                await message.answer(car_route + bus_route, reply_markup=ibt_attractions_back[u.id], disable_web_page_preview=True, parse_mode='html')
            else:
                await bot.send_message(u.id, "Чтобы проложить маршрут отправьте вашу геолокацию", reply_markup=request_location[u.id], parse_mode='html')
    elif STATE[u.id] == 'SLIDER_5':
        await bot.send_location(u.id, 51.161396103774116, 71.41997724005724)
        await bot.send_message(u.id, "Чтобы проложить маршрут отправьте вашу геолокацию",
                               reply_markup=request_location[u.id], parse_mode='html')
        await bot.send_message(u.id, "Вернуть назад ⬇️", reply_markup=ibt_attractions_back[u.id], parse_mode='html')
        @dp.message_handler(content_types=['location'])
        async def location(message):
            u = message.from_user
            if message.location is not None:
                client_latitude = message.location.latitude
                client_longitude = message.location.longitude
                car_route = hlink('Маршрут для поездки в "автомобиле" до Набережной реки Ишим\n\n', f'https://www.google.com/maps/dir/{client_latitude},{client_longitude}/%D0%BD%D0%B0%D0%B1%D0%B5%D1%80%D0%B5%D0%B6%D0%BD%D0%B0%D1%8F,+%D0%9D%D1%83%D1%80-%D0%A1%D1%83%D0%BB%D1%82%D0%B0%D0%BD+020000/@{client_latitude},{client_longitude},15z/data=!3m1!4b1!4m9!4m8!1m0!1m5!1m1!1s0x424586d1d5b81349:0x64f872f1b98950eb!2m2!1d71.4199987!2d51.1612481!3e0')
                bus_route = hlink('Маршрут для поездки в "автобусе" до Набережной реки Ишим', f'https://www.google.com/maps/dir/{client_latitude},{client_longitude}/%D0%BD%D0%B0%D0%B1%D0%B5%D1%80%D0%B5%D0%B6%D0%BD%D0%B0%D1%8F,+%D0%9D%D1%83%D1%80-%D0%A1%D1%83%D0%BB%D1%82%D0%B0%D0%BD+020000/@{client_latitude},{client_longitude},15z/data=!3m1!4b1!4m9!4m8!1m0!1m5!1m1!1s0x424586d1d5b81349:0x64f872f1b98950eb!2m2!1d71.4199987!2d51.1612481!3e3')
                await message.answer(car_route + bus_route, reply_markup=ibt_attractions_back[u.id], disable_web_page_preview=True, parse_mode='html')
            else:
                await bot.send_message(u.id, "Чтобы проложить маршрут отправьте вашу геолокацию", reply_markup=request_location[u.id], parse_mode='html')
    elif STATE[u.id] == 'SLIDER_6':
        await bot.send_location(u.id, 51.12997210356209, 71.42069379000856)
        await bot.send_message(u.id, "Чтобы проложить маршрут отправьте вашу геолокацию",
                               reply_markup=request_location[u.id], parse_mode='html')
        await bot.send_message(u.id, "Вернуть назад ⬇️", reply_markup=ibt_attractions_back[u.id], parse_mode='html')
        @dp.message_handler(content_types=['location'])
        async def location(message):
            u = message.from_user
            if message.location is not None:
                client_latitude = message.location.latitude
                client_longitude = message.location.longitude
                car_route = hlink('Маршрут для поездки в "автомобиле" до Бульвара Нуржол\n\n', f'https://www.google.com/maps/dir/{client_latitude},{client_longitude}/%D0%B1%D1%83%D0%BB.+%D0%9D%D1%83%D1%80%D0%B6%D0%BE%D0%BB,+%D0%9D%D1%83%D1%80-%D0%A1%D1%83%D0%BB%D1%82%D0%B0%D0%BD+020000/@{client_latitude},{client_longitude},13z/data=!4m14!4m13!1m5!3m4!1m2!1d71.4311086!2d51.1247883!3s0x4245841ecd28bc31:0x325fcdd30616deb6!1m5!1m1!1s0x4245841c5ab777c7:0xe87aa517cddeedb3!2m2!1d71.4349095!2d51.1269624!3e0')
                bus_route = hlink('Маршрут для поездки в "автобусе" до Бульвара Нуржол', f'https://www.google.com/maps/dir/{client_latitude},{client_longitude}/%D0%B1%D1%83%D0%BB%D1%8C%D0%B2%D0%B0%D1%80+%D0%9D%D1%83%D1%80%D0%B6%D0%BE%D0%BB,+%D0%9D%D1%83%D1%80-%D0%A1%D1%83%D0%BB%D1%82%D0%B0%D0%BD/@{client_latitude},{client_longitude},13z/data=!4m9!4m8!1m0!1m5!1m1!1s0x4245841c5ab777c7:0xe87aa517cddeedb3!2m2!1d71.4349095!2d51.1269624!3e3')
                await message.answer(car_route + bus_route, reply_markup=ibt_attractions_back[u.id], disable_web_page_preview=True, parse_mode='html')
            else:
                await bot.send_message(u.id, "Чтобы проложить маршрут отправьте вашу геолокацию", reply_markup=request_location[u.id], parse_mode='html')
    elif STATE[u.id] == 'SLIDER_7':
        await bot.send_location(u.id, 51.12157025378239, 71.46997172841554)
        await bot.send_message(u.id, "Чтобы проложить маршрут отправьте вашу геолокацию",
                               reply_markup=request_location[u.id], parse_mode='html')
        await bot.send_message(u.id, "Вернуть назад ⬇️", reply_markup=ibt_attractions_back[u.id], parse_mode='html')
        @dp.message_handler(content_types=['location'])
        async def location(message):
            u = message.from_user
            if message.location is not None:
                client_latitude = message.location.latitude
                client_longitude = message.location.longitude
                car_route = hlink('Маршрут для поездки в "автомобиле" до Площади Независимости\n\n', f'https://www.google.com/maps/dir/{client_latitude},{client_longitude}/%D0%9C%D0%BE%D0%BD%D1%83%D0%BC%D0%B5%D0%BD%D1%82+%22%D0%9A%D0%B0%D0%B7%D0%B0%D1%85%D1%81%D0%BA%D0%B8%D0%B9+%D0%BD%D0%B0%D1%80%D0%BE%D0%B4%22,+%D0%9D%D1%83%D1%80-%D0%A1%D1%83%D0%BB%D1%82%D0%B0%D0%BD+010000/@{client_latitude},{client_longitude},15z/data=!3m1!4b1!4m9!4m8!1m0!1m5!1m1!1s0x424583f118cc2dcb:0xef173b04e8efddae!2m2!1d71.4698859!2d51.1220686!3e0')
                bus_route = hlink('Маршрут для поездки в "автобусе" до Площади Независимости', f'https://www.google.com/maps/dir/{client_latitude},{client_longitude}/%D0%9C%D0%BE%D0%BD%D1%83%D0%BC%D0%B5%D0%BD%D1%82+%22%D0%9A%D0%B0%D0%B7%D0%B0%D1%85%D1%81%D0%BA%D0%B8%D0%B9+%D0%BD%D0%B0%D1%80%D0%BE%D0%B4%22,+%D0%9D%D1%83%D1%80-%D0%A1%D1%83%D0%BB%D1%82%D0%B0%D0%BD+010000/@{client_latitude},{client_longitude},15z/data=!3m1!4b1!4m9!4m8!1m0!1m5!1m1!1s0x424583f118cc2dcb:0xef173b04e8efddae!2m2!1d71.4698859!2d51.1220686!3e3')
                await message.answer(car_route + bus_route, reply_markup=ibt_attractions_back[u.id], disable_web_page_preview=True, parse_mode='html')
            else:
                await bot.send_message(u.id, "Чтобы проложить маршрут отправьте вашу геолокацию", reply_markup=request_location[u.id], parse_mode='html')
    elif STATE[u.id] == 'SLIDER_8':
        await bot.send_location(u.id, 51.1494333120279, 71.41902399534874)
        await bot.send_message(u.id, "Чтобы проложить маршрут отправьте вашу геолокацию",
                               reply_markup=request_location[u.id], parse_mode='html')
        await bot.send_message(u.id, "Вернуть назад ⬇️", reply_markup=ibt_attractions_back[u.id], parse_mode='html')
        @dp.message_handler(content_types=['location'])
        async def location(message):
            u = message.from_user
            if message.location is not None:
                client_latitude = message.location.latitude
                client_longitude = message.location.longitude
                car_route = hlink('Маршрут для поездки в "автомобиле" до Этно-мемориального комплекса "Карта Казахстана - Атамекен"\n\n', f'https://www.google.com/maps/dir/{client_latitude},{client_longitude}/%D0%AD%D1%82%D0%BD%D0%BE-%D0%BC%D0%B5%D0%BC%D0%BE%D1%80%D0%B8%D0%B0%D0%BB%D1%8C%D0%BD%D1%8B%D0%B9+%D0%BA%D0%BE%D0%BC%D0%BF%D0%BB%D0%B5%D0%BA%D1%81+%D0%9A%D0%B0%D1%80%D1%82%D0%B0+%D0%9A%D0%B0%D0%B7%D0%B0%D1%85%D1%81%D1%82%D0%B0%D0%BD%D0%B0+%D0%90%D1%82%D0%B0%D0%BC%D0%B5%D0%BA%D0%B5%D0%BD,+%D0%9A%D0%BE%D1%80%D0%B3%D0%B0%D0%BB%D0%B6%D0%B8%D0%BD%D1%81%D0%BA%D0%BE%D0%B5+%D1%88%D0%BE%D1%81%D1%81%D0%B5,+%D0%9D%D1%83%D1%80-%D0%A1%D1%83%D0%BB%D1%82%D0%B0%D0%BD/@{client_latitude},{client_longitude},12z/data=!4m9!4m8!1m0!1m5!1m1!1s0x424586b8b8dc2c65:0x20ef0e3380044402!2m2!1d71.4185412!2d51.149292!3e0')
                bus_route = hlink('Маршрут для поездки в "автобусе" до Этно-мемориального комплекса "Карта Казахстана - Атамекен"', f'https://www.google.com/maps/dir/{client_latitude},{client_longitude}/%D0%AD%D1%82%D0%BD%D0%BE-%D0%BC%D0%B5%D0%BC%D0%BE%D1%80%D0%B8%D0%B0%D0%BB%D1%8C%D0%BD%D1%8B%D0%B9+%D0%BA%D0%BE%D0%BC%D0%BF%D0%BB%D0%B5%D0%BA%D1%81+%D0%9A%D0%B0%D1%80%D1%82%D0%B0+%D0%9A%D0%B0%D0%B7%D0%B0%D1%85%D1%81%D1%82%D0%B0%D0%BD%D0%B0+%D0%90%D1%82%D0%B0%D0%BC%D0%B5%D0%BA%D0%B5%D0%BD,+%D0%9A%D0%BE%D1%80%D0%B3%D0%B0%D0%BB%D0%B6%D0%B8%D0%BD%D1%81%D0%BA%D0%BE%D0%B5+%D1%88%D0%BE%D1%81%D1%81%D0%B5,+%D0%9D%D1%83%D1%80-%D0%A1%D1%83%D0%BB%D1%82%D0%B0%D0%BD/@{client_latitude},{client_longitude},12z/data=!3m1!4b1!4m9!4m8!1m0!1m5!1m1!1s0x424586b8b8dc2c65:0x20ef0e3380044402!2m2!1d71.4185412!2d51.149292!3e3')
                await message.answer(car_route + bus_route, reply_markup=ibt_attractions_back[u.id], disable_web_page_preview=True, parse_mode='html')
            else:
                await bot.send_message(u.id, "Чтобы проложить маршрут отправьте вашу геолокацию", reply_markup=request_location[u.id], parse_mode='html')

    elif STATE[u.id] == 'SLIDER_9':
        await bot.send_location(u.id, 51.14745365317472, 71.41494178185667)
        await bot.send_message(u.id, "Чтобы проложить маршрут отправьте вашу геолокацию",
                               reply_markup=request_location[u.id], parse_mode='html')
        await bot.send_message(u.id, "Вернуть назад ⬇️", reply_markup=ibt_attractions_back[u.id], parse_mode='html')
        @dp.message_handler(content_types=['location'])
        async def location(message):
            u = message.from_user
            if message.location is not None:
                client_latitude = message.location.latitude
                client_longitude = message.location.longitude
                car_route = hlink('Маршрут для поездки в "автомобиле" до Колесы обозрения «Ailand»\n\n', f'https://www.google.com/maps/dir/{client_latitude},{client_longitude}/%D0%9A%D0%BE%D0%BB%D0%B5%D1%81%D0%BE+%D0%BE%D0%B1%D0%BE%D0%B7%D1%80%D0%B5%D0%BD%D0%B8%D1%8F+Ailand,+%D0%9D%D1%83%D1%80-%D0%A1%D1%83%D0%BB%D1%82%D0%B0%D0%BD/@{client_latitude},{client_longitude},12z/data=!3m1!4b1!4m9!4m8!1m0!1m5!1m1!1s0x424586bf73698705:0x589fc5ebba8e562!2m2!1d71.4144268!2d51.1473931!3e0')
                bus_route = hlink('Маршрут для поездки в "автобусе" до Колесы обозрения «Ailand»', f'https://www.google.com/maps/dir/{client_latitude},{client_longitude}/%D0%9A%D0%BE%D0%BB%D0%B5%D1%81%D0%BE+%D0%BE%D0%B1%D0%BE%D0%B7%D1%80%D0%B5%D0%BD%D0%B8%D1%8F+Ailand,+%D0%9D%D1%83%D1%80-%D0%A1%D1%83%D0%BB%D1%82%D0%B0%D0%BD/@{client_latitude},{client_longitude},12z/data=!3m1!4b1!4m9!4m8!1m0!1m5!1m1!1s0x424586bf73698705:0x589fc5ebba8e562!2m2!1d71.4144268!2d51.1473931!3e3')
                await message.answer(car_route + bus_route, reply_markup=ibt_attractions_back[u.id], disable_web_page_preview=True, parse_mode='html')
            else:
                await bot.send_message(u.id, "Чтобы проложить маршрут отправьте вашу геолокацию", reply_markup=request_location[u.id], parse_mode='html')
    else:
        pass


@dp.callback_query_handler(lambda c: c.data == 'back_video')
async def go_back_video (callback_query: types.CallbackQuery):
    u = callback_query.from_user
    await bot.send_message(u.id, emojize(s[1][0][10].text), reply_markup=ikb_services[u.id])
    STATE[u.id] = 'SERV'

@dp.callback_query_handler(lambda c: c.data == 'back_attractions')
async def go_back_attractions(callback_query: types.CallbackQuery):
    u = callback_query.from_user
    await bot.send_message(u.id, "Топ 10 достопримечательностей г. Нур-Султан", reply_markup=kb_menu[u.id])
    if STATE[u.id] == 'SLIDER_0':
        await bot.send_photo(u.id, txt[u.id][1][0][2].text)
        await bot.send_message(u.id, txt[u.id][1][0][0].text, reply_markup=ikb_slider[u.id], parse_mode='html')
        STATE[u.id] = 'SLIDER_0'
    elif STATE[u.id] == 'SLIDER_1':
        await bot.send_photo(u.id, txt[u.id][1][1][1].text)
        await bot.send_message(u.id, txt[u.id][1][1][0].text, reply_markup=ikb_slider[u.id], parse_mode='html')
        STATE[u.id] = 'SLIDER_1'
    elif STATE[u.id] == 'SLIDER_2':
        await bot.send_photo(u.id, txt[u.id][1][2][1].text)
        await bot.send_message(u.id, txt[u.id][1][2][0].text, reply_markup=ikb_slider[u.id], parse_mode='html')
        STATE[u.id] = 'SLIDER_2'
    elif STATE[u.id] == 'SLIDER_3':
        await bot.send_photo(u.id, txt[u.id][1][3][1].text)
        await bot.send_message(u.id, txt[u.id][1][3][0].text, reply_markup=ikb_slider[u.id], parse_mode='html')
        STATE[u.id] = 'SLIDER_3'
    elif STATE[u.id] == 'SLIDER_4':
        await bot.send_photo(u.id, txt[u.id][1][4][1].text)
        await bot.send_message(u.id, txt[u.id][1][4][0].text, reply_markup=ikb_slider[u.id], parse_mode='html')
        STATE[u.id] = 'SLIDER_4'
    elif STATE[u.id] == 'SLIDER_5':
        await bot.send_photo(u.id, txt[u.id][1][5][1].text)
        await bot.send_message(u.id, txt[u.id][1][5][0].text, reply_markup=ikb_slider[u.id], parse_mode='html')
        STATE[u.id] = 'SLIDER_5'
    elif STATE[u.id] == 'SLIDER_6':
        await bot.send_photo(u.id, txt[u.id][1][6][1].text)
        await bot.send_message(u.id, txt[u.id][1][6][0].text, reply_markup=ikb_slider[u.id], parse_mode='html')
        STATE[u.id] = 'SLIDER_6'
    elif STATE[u.id] == 'SLIDER_7':
        await bot.send_photo(u.id, txt[u.id][1][7][1].text)
        await bot.send_message(u.id, txt[u.id][1][7][0].text, reply_markup=ikb_slider[u.id], parse_mode='html')
        STATE[u.id] = 'SLIDER_7'
    elif STATE[u.id] == 'SLIDER_8':
        await bot.send_photo(u.id, txt[u.id][1][8][1].text)
        await bot.send_message(u.id, txt[u.id][1][8][0].text, reply_markup=ikb_slider[u.id], parse_mode='html')
        STATE[u.id] = 'SLIDER_8'
    elif STATE[u.id] == 'SLIDER_9':
        await bot.send_photo(u.id, txt[u.id][1][9][1].text)
        await bot.send_message(u.id, txt[u.id][1][9][0].text, reply_markup=ikb_slider[u.id], parse_mode='html')
        STATE[u.id] = 'SLIDER_9'
    else:
        pass


@dp.callback_query_handler(lambda c: c.data == 'air_quality')
async def air_quality(callback_query: types.CallbackQuery):
    u = callback_query.from_user

    if STATE[u.id] == 'SLIDER_0':
        api_data = 'http://opendata.kz/api/sensor/getListWithLastHistory?cityId=1'
        data = requests.get(api_data)
        CO2 = data.json()["sensors"][13]["history"][0]["data"]["field1"]
        PM25 = data.json()["sensors"][13]["history"][0]["data"]["field2"]
        TEMP = data.json()["sensors"][13]["history"][0]["data"]["field3"]
        Humidity = data.json()["sensors"][13]["history"][0]["data"]["field5"]
        Date = data.json()["sensors"][13]["history"][0]["data"]["field1_created_at"]
        await bot.send_message(u.id, emojize(f"Качество воздуха в районе Монумента Байтерек \n\n<b>CO2 (Углекислый газ), ppm:  {CO2}</b>  🟢  В норме\n<b>PM2.5 (Частицы загрязнители):  {PM25}</b>    🟢 В норме\n<b>Температура, C:  {TEMP}</b> 🌡\n<b>Влажность, %:  {Humidity}</b> 💨\nДанные получены: {Date} 📅\n"), reply_markup=ibt_attractions_back[u.id], parse_mode='html')

    elif STATE[u.id] == 'SLIDER_1':
        api_data = 'http://opendata.kz/api/sensor/getListWithLastHistory?cityId=1'
        data = requests.get(api_data)
        CO2 = data.json()["sensors"][27]["history"][0]["data"]["field1"]
        PM25 = data.json()["sensors"][27]["history"][0]["data"]["field2"]
        TEMP = data.json()["sensors"][27]["history"][0]["data"]["field3"]
        Humidity = data.json()["sensors"][27]["history"][0]["data"]["field5"]
        Date = data.json()["sensors"][27]["history"][0]["data"]["field1_created_at"]
        await bot.send_message(u.id, emojize(
                f"Качество воздуха в районе ТРЦ 'Ханшатыр' \n\n<b>CO2 (Углекислый газ), ppm:  {CO2}</b>  🟢  В норме\n<b>PM2.5 (Частицы загрязнители):  {PM25}</b>    🟢 В норме\n<b>Температура, C:  {TEMP}</b> 🌡\n<b>Влажность, %:  {Humidity}</b> 💨\nДанные получены: {Date} 📅\n"),
                                   reply_markup=ibt_attractions_back[u.id], parse_mode='html')

    elif STATE[u.id] == 'SLIDER_2':
        api_data = 'http://opendata.kz/api/sensor/getListWithLastHistory?cityId=1'
        data = requests.get(api_data)
        CO2 = data.json()["sensors"][36]["history"][0]["data"]["field1"]
        PM25 = data.json()["sensors"][36]["history"][0]["data"]["field2"]
        TEMP = data.json()["sensors"][36]["history"][0]["data"]["field3"]
        Humidity = data.json()["sensors"][36]["history"][0]["data"]["field5"]
        Date = data.json()["sensors"][36]["history"][0]["data"]["field1_created_at"]
        await bot.send_message(u.id, emojize(
            f"Качество воздуха в районе Дворца мира и согласия' \n\n<b>CO2 (Углекислый газ), ppm:  {CO2}</b>  🟢  В норме\n<b>PM2.5 (Частицы загрязнители):  {PM25}</b>    🟢 В норме\n<b>Температура, C:  {TEMP}</b> 🌡\n<b>Влажность, %:  {Humidity}</b> 💨\nДанные получены: {Date} 📅\n"),
                               reply_markup=ibt_attractions_back[u.id], parse_mode='html')

    elif STATE[u.id] == 'SLIDER_3':
        api_data = 'http://opendata.kz/api/sensor/getListWithLastHistory?cityId=1'
        data = requests.get(api_data)
        CO2 = data.json()["sensors"][48]["history"][0]["data"]["field1"]
        PM25 = data.json()["sensors"][48]["history"][0]["data"]["field2"]
        TEMP = data.json()["sensors"][48]["history"][0]["data"]["field3"]
        Humidity = data.json()["sensors"][48]["history"][0]["data"]["field5"]
        Date = data.json()["sensors"][48]["history"][0]["data"]["field1_created_at"]
        await bot.send_message(u.id, emojize(
            f"Качество воздуха в районе Дворца мира и согласия' \n\n<b>CO2 (Углекислый газ), ppm:  {CO2}</b>  🟢  В норме\n<b>PM2.5 (Частицы загрязнители):  {PM25}</b>    🟢 В норме\n<b>Температура, C:  {TEMP}</b> 🌡\n<b>Влажность, %:  {Humidity}</b> 💨\nДанные получены: {Date} 📅\n"),
                               reply_markup=ibt_attractions_back[u.id], parse_mode='html')
    elif STATE[u.id] == 'SLIDER_4':
        api_data = 'http://opendata.kz/api/sensor/getListWithLastHistory?cityId=1'
        data = requests.get(api_data)
        CO2 = data.json()["sensors"][10]["history"][0]["data"]["field1"]
        PM25 = data.json()["sensors"][10]["history"][0]["data"]["field2"]
        TEMP = data.json()["sensors"][10]["history"][0]["data"]["field3"]
        Humidity = data.json()["sensors"][10]["history"][0]["data"]["field5"]
        Date = data.json()["sensors"][10]["history"][0]["data"]["field1_created_at"]
        await bot.send_message(u.id, emojize(
            f"Качество воздуха в районе РЦ 'Думан' \n\n<b>CO2 (Углекислый газ), ppm:  {CO2}</b>  🟢  В норме\n<b>PM2.5 (Частицы загрязнители):  {PM25}</b>    🟢 В норме\n<b>Температура, C:  {TEMP}</b> 🌡\n<b>Влажность, %:  {Humidity}</b> 💨\nДанные получены: {Date} 📅\n"),
                               reply_markup=ibt_attractions_back[u.id], parse_mode='html')

    elif STATE[u.id] == 'SLIDER_5':
        api_data = 'http://opendata.kz/api/sensor/getListWithLastHistory?cityId=1'
        data = requests.get(api_data)
        CO2 = data.json()["sensors"][43]["history"][0]["data"]["field1"]
        PM25 = data.json()["sensors"][43]["history"][0]["data"]["field2"]
        TEMP = data.json()["sensors"][43]["history"][0]["data"]["field3"]
        Humidity = data.json()["sensors"][43]["history"][0]["data"]["field5"]
        Date = data.json()["sensors"][43]["history"][0]["data"]["field1_created_at"]
        await bot.send_message(u.id, emojize(
            f"Качество воздуха в районе Набережной реки Ишим' \n\n<b>CO2 (Углекислый газ), ppm:  {CO2}</b>  🟡 Неподходящее для особо восприимчивых\n<b>PM2.5 (Частицы загрязнители):  {PM25}</b>  🟡 Неподходящее для особо восприимчивых\n<b>Температура, C:  {TEMP}</b> 🌡\n<b>Влажность, %:  {Humidity}</b> 💨\nДанные получены: {Date} 📅\n"),
                               reply_markup=ibt_attractions_back[u.id], parse_mode='html')

    elif STATE[u.id] == 'SLIDER_6':
        api_data = 'http://opendata.kz/api/sensor/getListWithLastHistory?cityId=1'
        data = requests.get(api_data)
        CO2 = data.json()["sensors"][27]["history"][0]["data"]["field1"]
        PM25 = data.json()["sensors"][27]["history"][0]["data"]["field2"]
        TEMP = data.json()["sensors"][27]["history"][0]["data"]["field3"]
        Humidity = data.json()["sensors"][27]["history"][0]["data"]["field5"]
        Date = data.json()["sensors"][27]["history"][0]["data"]["field1_created_at"]
        await bot.send_message(u.id, emojize(
            f"Качество воздуха в районе Бульвара Нуржол' \n\n<b>CO2 (Углекислый газ), ppm:  {CO2}</b>   🟢  В норме\n<b>PM2.5 (Частицы загрязнители):  {PM25}</b>  🟢  В норме\n<b>Температура, C:  {TEMP}</b> 🌡\n<b>Влажность, %:  {Humidity}</b> 💨\nДанные получены: {Date} 📅\n"),
                               reply_markup=ibt_attractions_back[u.id], parse_mode='html')

    elif STATE[u.id] == 'SLIDER_7':
        api_data = 'http://opendata.kz/api/sensor/getListWithLastHistory?cityId=1'
        data = requests.get(api_data)
        CO2 = data.json()["sensors"][36]["history"][0]["data"]["field1"]
        PM25 = data.json()["sensors"][36]["history"][0]["data"]["field2"]
        TEMP = data.json()["sensors"][36]["history"][0]["data"]["field3"]
        Humidity = data.json()["sensors"][36]["history"][0]["data"]["field5"]
        Date = data.json()["sensors"][36]["history"][0]["data"]["field1_created_at"]
        await bot.send_message(u.id, emojize(
            f"Качество воздуха в районе Площади Независимости' \n\n<b>CO2 (Углекислый газ), ppm:  {CO2}</b>   🟢  В норме\n<b>PM2.5 (Частицы загрязнители):  {PM25}</b>  🟢  В норме\n<b>Температура, C:  {TEMP}</b> 🌡\n<b>Влажность, %:  {Humidity}</b> 💨\nДанные получены: {Date} 📅\n"),
                               reply_markup=ibt_attractions_back[u.id], parse_mode='html')
    elif STATE[u.id] == 'SLIDER_8':
        api_data = 'http://opendata.kz/api/sensor/getListWithLastHistory?cityId=1'
        data = requests.get(api_data)
        CO2 = data.json()["sensors"][10]["history"][0]["data"]["field1"]
        PM25 = data.json()["sensors"][10]["history"][0]["data"]["field2"]
        TEMP = data.json()["sensors"][10]["history"][0]["data"]["field3"]
        Humidity = data.json()["sensors"][10]["history"][0]["data"]["field5"]
        Date = data.json()["sensors"][10]["history"][0]["data"]["field1_created_at"]
        await bot.send_message(u.id, emojize(
            f"Качество воздуха в районе Этно-мемориального комплекса 'Карта Казахстана - Атамекен' \n\n<b>CO2 (Углекислый газ), ppm:  {CO2}</b>   🟢  В норме\n<b>PM2.5 (Частицы загрязнители):  {PM25}</b>  🟢  В норме\n<b>Температура, C:  {TEMP}</b> 🌡\n<b>Влажность, %:  {Humidity}</b> 💨\nДанные получены: {Date} 📅\n"),
                               reply_markup=ibt_attractions_back[u.id], parse_mode='html')
    elif STATE[u.id] == 'SLIDER_9':
        api_data = 'http://opendata.kz/api/sensor/getListWithLastHistory?cityId=1'
        data = requests.get(api_data)
        CO2 = data.json()["sensors"][10]["history"][0]["data"]["field1"]
        PM25 = data.json()["sensors"][10]["history"][0]["data"]["field2"]
        TEMP = data.json()["sensors"][10]["history"][0]["data"]["field3"]
        Humidity = data.json()["sensors"][10]["history"][0]["data"]["field5"]
        Date = data.json()["sensors"][10]["history"][0]["data"]["field1_created_at"]
        await bot.send_message(u.id, emojize(
            f"Качество воздуха в районе Колесы обозрения 'Ailand' \n\n<b>CO2 (Углекислый газ), ppm:  {CO2}</b>   🟢  В норме\n<b>PM2.5 (Частицы загрязнители):  {PM25}</b>  🟢  В норме\n<b>Температура, C:  {TEMP}</b> 🌡\n<b>Влажность, %:  {Humidity}</b> 💨\nДанные получены: {Date} 📅\n"),
                               reply_markup=ibt_attractions_back[u.id], parse_mode='html')
    else:
        pass

# STARTING -------------------------------------------------------------------------------

if __name__ == '__main__':
    executor.start_polling(dp)


# TO DO ----------------------------------------------------------------------------------
