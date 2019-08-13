import weather_api
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from apscheduler.schedulers.blocking import BlockingScheduler
from google_func import search_area
from valid import check_input
import random
import threading
import weather_api
from config import BOT_TOKEN
all_type_list = {}
type_list = ['基隆市', '臺北市', '新北市', '桃園縣', '新竹市', '新竹縣', '苗栗縣', '臺中市', '彰化縣', '南投縣',
             '雲林縣', '嘉義市', '嘉義縣', '臺南市', '高雄市', '屏東縣', '臺東縣', '花蓮縣', '宜蘭縣', '澎湖縣', '金門縣', '連江縣']
user_location = {}
sche_thread = []
emoji = ['🚂','🚃','🚄','🚅','🚆','🚇','🚈','🚉','🚊','🚝','🚞','🚋','🚌','🚍','🚎','🚏','🚐','🚑','🚒','🚓','🚔','🚕','🚖','🚗','🚘','🚚','🚛','🚜','🚲','⛽','🚨','🚥','🚦','🚧','⛵','🚣','🚤','🚢','💺','🚁','🚟','🚠','🚡','🚀']
def request_choose(locate, day):
    request = [day for i in range(5)]
    result = weather_api.get_data(locate, request)
    weather_now = result[0]['parameter']['parameterName']
    raining_rate = result[1]['parameter']['parameterName']
    lowest_temp = result[2]['parameter']['parameterName']
    feeling = result[3]['parameter']['parameterName']
    highest_temp = result[4]['parameter']['parameterName']
    return (locate+"的天氣爲"+weather_now+"\n降雨機率: "+raining_rate +
            "%\n最低溫度: "+lowest_temp+"C 最高溫度: "+highest_temp+"C \n舒適度爲"+feeling)
def get_request(locate, update):
    request = [1, 1, 1, 1, 1]
    result = weather_api.get_data(locate, request)
    weather_now = result[0]['parameter']['parameterName']
    raining_rate = result[1]['parameter']['parameterName']
    lowest_temp = result[2]['parameter']['parameterName']
    feeling = result[3]['parameter']['parameterName']
    highest_temp = result[4]['parameter']['parameterName']
    update.message.reply_text(locate+"的天氣爲"+weather_now+"\n降雨機率: "+raining_rate +
                              "%\n最低溫度: "+lowest_temp+"C 最高溫度: "+highest_temp+"C \n舒適度爲"+feeling, reply_markup=InlineKeyboardMarkup([[
                                  InlineKeyboardButton(time, callback_data='{}-{}'.format(index, locate)) for index, time in [(2, '12小時後'), (3, '24小時後')]
                              ]]))
def locate_sentence(bot, update):
    possiple_list = check_input(update.message.text.strip())
    print(possiple_list)
    if len(possiple_list) == 1:
        get_request(possiple_list[0], update)
    elif len(possiple_list) > 5:
        update.message.reply_text("請重新輸入！")
    else:
        update.message.reply_text('我們只支援台灣喔！還是你是要以下選擇', reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton(random.choice(emoji)+ ' ' + locate, callback_data='msg-'+locate) for locate in possiple_list
        ]]))
def notification(location, update):
    def hello():
        update.message.reply_text("個人天氣通知")
        get_request(location, update)
    return hello
def set_notify(bot, update):
    userid = update.message.from_user.id
    if userid not in user_location:
        update.message.reply_text('你還沒設定居住區域啦 幹你娘低能兒')
    print(update.message.text.strip())
    time = update.message.text.strip()[8:]
    print(time)
    if int(time[:2]) >= 0 and int(time[:2]) <= 23 and int(time[3:]) >= 0 and int(time[3:]) < 60:
        location = user_location[userid]
        update.message.reply_text('你的居住地爲'+location+', 設定通知時間爲'+time)
        sche_thread.append(threading.Thread(
            target=schedule, args=(location, update, time,)))
        sche_thread[-1].start()
    else:
        update.message.reply_text("輸入時間不合法")
def schedule(location, update, time):
    sched = BlockingScheduler()
    sched.add_job(func=notification(location, update),
                  trigger='cron', hour=time[:2], minute=time[3:])
    sched.start()
def set_location(bot, update):
    possiple_list = check_input(update.message.text.strip()[5:])
    userid = update.message.from_user.id
    if len(possiple_list) == 1:
        user_location[userid] = possiple_list[0]
        print(user_location)
        update.message.reply_text('已更變居住區域: ' + possiple_list[0])
    elif len(possiple_list) > 5:
        update.message.reply_text("請重新輸入！")
    else:
        update.message.reply_text('目前我們只支持台灣喔！還是您是要...', reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton(random.choice(emoji)+ ' ' + locate, callback_data='set-'+locate+'-'+str(userid)) for locate in possiple_list
        ]]))
def location_handler(bot, update):
    latlng = (update['message']['location']
              ['latitude'], update['message']['location']['longitude'])
    locate = search_area(latlng)
    if locate == None:
        update.message.reply_text('目前本系統只支援台灣喔！')
    else:
        get_request(search_area(latlng), update)
button_map = {
    '1': [(2, '12小時後'), (3, '24小時後')],
    '2': [(1, '12小時前'), (3, '12小時後')],
    '3': [(1, '24小時前'), (2, '12小時前')],
}
def callback_query_handler(bot, update):
    callback_data = update.callback_query.data.split('-')
    print(update.callback_query.data)
    if callback_data[0] == 'msg':
        update.callback_query.edit_message_text(
            request_choose(callback_data[1], 1))
        update.callback_query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton(time, callback_data='{}-{}'.format(index, callback_data[1])) for index, time in button_map['1']
        ]]))
    elif callback_data[0] == 'set':
        user_location[int(callback_data[2])] = callback_data[1]
        update.callback_query.edit_message_text('已更變居住區域: ' + callback_data[1])
        print(user_location)
    else:
        update.callback_query.edit_message_text(
            request_choose(callback_data[1], int(callback_data[0])))
        update.callback_query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton(time, callback_data='{}-{}'.format(index, callback_data[1])) for index, time in button_map[callback_data[0]]
        ]]))
def helping(bot,update):
    update.message.reply_text('歡迎使用Weather Now 專業氣象推播機器人!\n請直接輸入欲查詢的縣市名稱或傳送位置資料即可立即取得最新氣象資訊!\n訊息自動推播功能:\n您可以使用/set 縣市 指令來綁定位置，再使用/notify HH:MM 設定推播時間，機器人便會自動通報氣象。\n感謝您使用本產品!若在使用上有任何問題，歡迎使用/help 指令查看說明。')

def meow_handler(bot,update):
    photos = ['https://i.imgur.com/bYLtKnH.jpg','https://i.imgur.com/vD2BIwP.jpg','https://i.imgur.com/4EscGMW.jpg', 'https://i.imgur.com/e6ZLwtM.jpg','https://i.imgur.com/VyYkZHz.jpg','https://i.imgur.com/mRzIERX.jpg','https://i.imgur.com/wJi74LE.jpg' ]
    update.message.reply_photo(random.choice(photos))

updater = Updater(BOT_TOKEN)
updater.dispatcher.add_handler(
    MessageHandler(Filters.location, location_handler))
updater.dispatcher.add_handler(CallbackQueryHandler(callback_query_handler))
updater.dispatcher.add_handler(MessageHandler(Filters.text, locate_sentence))
updater.dispatcher.add_handler(CommandHandler('notify', set_notify))
updater.dispatcher.add_handler(CommandHandler('set', set_location))
updater.dispatcher.add_handler(CommandHandler('help', helping))
updater.dispatcher.add_handler(CommandHandler('start', helping))
updater.dispatcher.add_handler(CommandHandler('meow', meow_handler))
updater.start_polling()
updater.idle()
