import weather_api
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from apscheduler.schedulers.blocking import BlockingScheduler
from google_func import search_area
import schedule
import logging
logging.basicConfig()
all_type_list = {}
type_list = ['基隆市', '臺北市', '新北市', '桃園縣', '新竹市', '新竹縣', '苗栗縣', '臺中市', '彰化縣', '南投縣',
             '雲林縣', '嘉義市', '嘉義縣', '臺南市', '高雄市', '屏東縣', '臺東縣', '花蓮縣', '宜蘭縣', '澎湖縣', '金門縣', '連江縣']
user_location = {}

# 0基隆市 1台北市 2新北市 3桃園縣 4新竹市 5新竹縣 6苗栗縣 7臺中市 8彰化縣 9南投縣 10雲林縣 11嘉義市
# 12嘉義縣 13臺南市 14高雄市 15屏東縣 16臺東縣 17花蓮縣 18宜蘭縣 19澎湖縣 20金門縣 21連江縣


def request_choose(locate, day):
    request = [day for i in range(5)]
    result = weather_api.get_data(locate, request)
    start_time = result[0]['startTime']
    end_time = result[0]['endTime']
    weather_now = result[0]['parameter']['parameterName']
    weather_index = result[0]['parameter']['parameterValue']
    raining_rate = result[1]['parameter']['parameterName']
    lowest_temp = result[2]['parameter']['parameterName']
    feeling = result[3]['parameter']['parameterName']
    highest_temp = result[4]['parameter']['parameterName']
    return (locate+"的天氣爲"+weather_now+"\n降雨機率: "+raining_rate +
            "%\n最低溫度: "+lowest_temp+"C 最高溫度: "+highest_temp+"C \n舒適度爲"+feeling)


def get_request(locate, update):
    request = [1, 1, 1, 1, 1]
    result = weather_api.get_data(locate, request)
    start_time = result[0]['startTime']
    end_time = result[0]['endTime']
    weather_now = result[0]['parameter']['parameterName']
    weather_index = result[0]['parameter']['parameterValue']
    raining_rate = result[1]['parameter']['parameterName']
    lowest_temp = result[2]['parameter']['parameterName']
    feeling = result[3]['parameter']['parameterName']
    highest_temp = result[4]['parameter']['parameterName']
    update.message.reply_text(locate+"的天氣爲"+weather_now+"\n降雨機率: "+raining_rate +
                              "%\n最低溫度: "+lowest_temp+"C 最高溫度: "+highest_temp+"C \n舒適度爲"+feeling, reply_markup=InlineKeyboardMarkup([[
                                  InlineKeyboardButton(time, callback_data='{}-{}'.format(index, locate)) for index, time in [(2, '12小時後'), (3, '24小時後')]
                              ]]))


def locate_sentence(bot, update):  # receive messege

    locate = update.message.text.strip()

    if locate in type_list:
        get_request(locate, update)
    else:
        update.message.reply_text('靠你確定你說的是臺灣嗎？')


def notification(location, update):
    def hello():
        update.message.reply_text("個人天氣通知")
        get_request(location, update)

    # call_request
    return hello


def set_notify(bot, update):
    userid = update.message.from_user.id

    if userid not in user_location:  # 遍歷user_location
        update.message.reply_text('你還沒設定居住區域啦 幹你娘低能兒')

    print(update.message.text.strip())
    time = update.message.text.strip()[8:]
    print(time)
    location = user_location[userid]
    update.message.reply_text('你的居住地爲'+location+', 設定通知時間爲'+time)
    sched = BlockingScheduler()
    sched.add_job(func=notification(location, update),
                  trigger='cron', hour=time[:2], minute=time[3:])
    sched.start()

 #   schedule.every().day.at(time).do(notification(location,update))


def set_location(bot, update):
    location = update.message.text.strip()[5:]
    userid = update.message.from_user.id
    if location in type_list:
        if userid in user_location:
            update.message.reply_text('已更變居住區域')
        user_location[userid] = location

    else:
        update.message.reply_text('你是住哪裡啦 媽的')


def location_handler(bot, update):
    latlng = (update['message']['location']
              ['latitude'], update['message']['location']['longitude'])
    get_request(search_area(latlng), update)


button_map = {
    '1': [(2, '12小時後'), (3, '24小時後')],
    '2': [(1, '12小時前'), (3, '12小時後')],
    '3': [(1, '24小時前'), (2, '12小時前')],
}


def callback_query_handler(bot, update):
    print(update.callback_query.data)
    callback_data = update.callback_query.data.split('-')
    update.callback_query.edit_message_text(
        request_choose(callback_data[1], int(callback_data[0])))
    update.callback_query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup([[
        InlineKeyboardButton(time, callback_data='{}-{}'.format(index, callback_data[1])) for index, time in button_map[callback_data[0]]
    ]]))


updater = Updater('759998134:AAFQ8soqpmW6sVntS1QWdgj9sdVXuVllLsM')

updater.dispatcher.add_handler(
    MessageHandler(Filters.location, location_handler))
updater.dispatcher.add_handler(CallbackQueryHandler(callback_query_handler))

updater.dispatcher.add_handler(MessageHandler(Filters.text, locate_sentence))
updater.dispatcher.add_handler(CommandHandler('notify', set_notify))
updater.dispatcher.add_handler(CommandHandler('set', set_location))
updater.start_polling()

updater.idle()
