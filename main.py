from telegram.ext import Updater, CommandHandler,MessageHandler,Filters
from apscheduler.schedulers.blocking import BlockingScheduler
import schedule
import logging
logging.basicConfig()
import weather_api
all_type_list={}
type_list = ['基隆市','臺北市','新北市','桃園縣','新竹市','新竹縣','苗栗縣','臺中市','彰化縣','南投縣','雲林縣','嘉義市','嘉義縣','臺南市','高雄市','屏東縣','臺東縣','花蓮縣','宜蘭縣','澎湖縣','金門縣','連江縣'] 
user_location = {}

#0基隆市 1台北市 2新北市 3桃園縣 4新竹市 5新竹縣 6苗栗縣 7臺中市 8彰化縣 9南投縣 10雲林縣 11嘉義市
#12嘉義縣 13臺南市 14高雄市 15屏東縣 16臺東縣 17花蓮縣 18宜蘭縣 19澎湖縣 20金門縣 21連江縣 

def locate_sentence(bot, update):#receive messege
    
    locate = update.message.text.strip()
    request=[1,1,1,1,1]
    if locate in type_list:
        result = weather_api.get_data(locate,request)
        weather_now = result[0]['parameter']['parameterValue']
        raining_rate = result[1]

def notification(location,update):
    def hello():
        update.message.reply_text('Miku is real')
    #call_request
    return hello

def set_notify(bot,update):
    userid = update.message.from_user.id

    if userid not in user_location:   #遍歷user_location
        update.message.reply_text('你還沒設定居住區域啦 幹你娘低能兒')
        
    print(update.message.text.strip())
    time = update.message.text.strip()[8:]
    print(time)    
    location = user_location[userid]
    update.message.reply_text('你的居住地爲'+location+', 設定通知時間爲'+time)
    sched = BlockingScheduler()
    sched.add_job(func=notification(location,update),trigger='cron',hour=time[:2],minute=time[3:])
    sched.start()
 #   schedule.every().day.at(time).do(notification(location,update))

def set_location(bot,update):
    location = update.message.text.strip()[5:]
    userid=update.message.from_user.id
    if location in type_list:
        if userid in user_location:
            update.message.reply_text('已更變居住區域')
        user_location[userid]=location
        
    else:
        update.message.reply_text('你是住哪裡啦 媽的')

updater = Updater('936215806:AAEbl8MOVWGTW5AONbDWLSkiQQfRFwNKm6g')
        
updater.dispatcher.add_handler(MessageHandler(Filters.text, locate_sentence))
updater.dispatcher.add_handler(CommandHandler('notify',set_notify))    
updater.dispatcher.add_handler(CommandHandler('set', set_location))  
updater.start_polling()

updater.idle()

