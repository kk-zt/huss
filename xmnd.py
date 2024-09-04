import requests
import telebot
from telebot import types
from telebot.types import InlineKeyboardButton as Btn, InlineKeyboardMarkup as Mak
from pytube import YouTube
from bs4 import BeautifulSoup
import os
import random

# إدخال التوكن الخاص بالبوت
token = "6993614740:AAHUuXVwJ0oWZyrrHiWT3-rEZTVeJ315_y4"
bot = telebot.TeleBot(token)

sent_video_messages = {}
sent_content_messages = {}

# تعيين أوامر البوت
bot.set_my_commands([telebot.types.BotCommand("/start", "🤖 تشغيل البوت")])

# معالجة الأمر /start
@bot.message_handler(commands=["start"])
def start(message):
    markup = types.InlineKeyboardMarkup()
    wevy = types.InlineKeyboardButton("مطور البوت 👨‍🔧", url='https://t.me/u_bll')
    wev = types.InlineKeyboardButton("قناتي", url='https://t.me/ss_1e')
    markup.add(wevy, wev)
    name = message.from_user.first_name
    bot.reply_to(message, f'''<b>مرحباً {name}
-! في بـوت تحميل من تيكـتوك، يوتيوب، وإنستغرام، وفيسبوك، ارسل الآن رابط لتحميل من فضلك.</b>''', parse_mode='HTML', reply_markup=markup)

# معالجة الرسائل النصية
@bot.message_handler(content_types=['text'])
def handle_text(message):
    link = message.text

    if 'insta' in link:  # التحقق من وجود رابط إنستغرام
        try:
            json_data = {'url': link}
            response = requests.post('https://insta.savetube.me/downloadPostVideo', json=json_data).json()
            thu = response['post_video_thumbnail']
            video = response['post_video_url']
            sent_message = bot.send_photo(message.chat.id, thu, reply_to_message_id=message.message_id, reply_markup=Mak().add(Btn('تحميل الفيديو', callback_data='vid')))
            sent_video_messages[sent_message.message_id] = video
        except:
            bot.reply_to(message, 'رابط إنستغرام غير صحيح أو خطأ في الخدمة')

    elif 'tik' in link:  # التحقق من وجود رابط تيك توك
        markup = types.InlineKeyboardMarkup()
        wev = types.InlineKeyboardButton("تم التحميل بواسطه", url='https://t.me/ss_1e')
        markup.add(wev)
        try:
            msgg = bot.send_message(message.chat.id, "*جاري التحميل ...*", parse_mode="markdown")
            url = requests.get(f'https://tikwm.com/api/?url={link}').json()
            music = url['data']['music']
            region = url['data']['region']
            tit = url['data']['title']
            vid = url['data']['play']
            ava = url['data']['author']['avatar']
            name = url['data']['music_info']['author']
            time = url['data']['duration']
            sh = url['data']['share_count']
            com = url['data']['comment_count']
            wat = url['data']['play_count']
            bot.delete_message(chat_id=message.chat.id, message_id=msgg.message_id)
            bot.send_photo(message.chat.id, ava, caption=f'- اسم الحساب : *{name}*\n - دوله الحساب : *{region}*\n\n- عدد مرات المشاهدة : *{wat}*\n- عدد التعليقات : *{com}*\n- عدد مرات المشاركة : *{sh}*\n- طول الفيديو : *{time}*', parse_mode="markdown")
            bot.send_video(message.chat.id, vid, caption=f"{tit}", reply_markup=markup)
        except:
            bot.delete_message(chat_id=message.chat.id, message_id=msgg.message_id)
            bot.reply_to(message, 'خطأ في تحميل الفيديو من تيك توك')

    elif 'youtube.com' in link:  # التحقق من وجود رابط يوتيوب
        if 'watch' in link:
            try:
                yt = YouTube(link)
                video = yt.streams.filter(progressive=True, file_extension='mp4').first()
                video.download()
                
                filem = video.default_filename
                uo = ''.join(random.choice('qwertyuioplkjhgfdsazxcvbn') for _ in range(4))
                namenew = f'{uo}.mp4'
                os.rename(filem, namenew)
                bot.send_video(message.chat.id, open(namenew, 'rb'), caption='*تم التحميل بنجاح*', parse_mode='markdown')
                os.remove(filem)
                os.remove(namenew)
            except Exception as e:
                bot.reply_to(message, f'خطأ: {e}')

    elif 'facebook.com' in link:  # التحقق من وجود رابط فيسبوك
        try:
            response = requests.get(f'https://fbdown.net/?url={link}')
            soup = BeautifulSoup(response.text, 'html.parser')
            video_url = soup.find('a', {'id': 'download'})['href']
            if video_url:
                sent_message = bot.send_photo(message.chat.id, 'http://example.com/thumbnail.jpg', reply_to_message_id=message.message_id, reply_markup=Mak().add(Btn('تحميل الفيديو', callback_data='vid')))
                sent_content_messages[sent_message.message_id] = video_url
            else:
                bot.reply_to(message, 'فشل في استخراج الفيديو أو المنشور من فيسبوك')
        except Exception as e:
            bot.reply_to(message, f'رابط غير صحيح أو خطأ في الخدمة: {e}')

# معالجة الاستجابة لنقرة الأزرار
@bot.callback_query_handler(func=lambda call: call.data == 'vid')
def handle_callback(call):
    message_id = call.message.message_id
    if message_id in sent_video_messages:
        video = sent_video_messages[message_id]
        bot.delete_message(call.message.chat.id, call.message.message_id)
        Mn = f"[تم تحميل بواسطة](https://t.me/ss_1e)"
        bot.send_video(call.message.chat.id, video, caption=Mn, parse_mode="Markdown")
    elif message_id in sent_content_messages:
        video = sent_content_messages[message_id]
        bot.delete_message(call.message.chat.id, call.message.message_id)
        Mn = f"[تم تحميل بواسطة](https://t.me/ss_1e)"
        bot.send_video(call.message.chat.id, video, caption=Mn, parse_mode="Markdown")

def main():
    while True:
        try:
            bot.infinity_polling()
        except Exception as e:
            print(f'Error: {e}')
            import os
            os.system('clear')

if __name__ == '__main__':
    main()