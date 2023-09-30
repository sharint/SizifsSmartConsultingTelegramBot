import telebot
import dbService
import uuid
import os
import speech_recognition as sr

token = "6339026680:AAHFh25ZDH2bxLvuNIvH7bQLYI6Y6MpPjsU"
bot = telebot.TeleBot(token, parse_mode=None)
language='ru_RU' # язык перевода

# Выполняется когда пользователь пишет команды /start или /help
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот-помощник sizif. Чем могу помочь?")
         
# Выполняется когда пользователь отправляет текстовое сообщение
@bot.message_handler(func=lambda m: True)
def echo_all(message):
    ans = dbService.getAnwerByQuestion(str(message.text).lower())
    if ans == None:
        ans = "К сожалению, ничего не нашел!"
    else:
        bot.send_message(message.chat.id,ans)

# Выполняется когда пользователь отправляет голосовое сообщение
@bot.message_handler(content_types=['voice'])
def voice_processing(message):
    filename = str(uuid.uuid4())
    file_name_full="./voice/"+filename+".ogg"
    file_name_full_converted="./ready/"+filename+".wav"
    file_info = bot.get_file(message.voice.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(file_name_full, 'wb') as new_file:
        new_file.write(downloaded_file)
    # конвертируем формат ogg в формат wav
    os.system("ffmpeg -i "+file_name_full+"  "+file_name_full_converted)
    text=recogniseVoice(file_name_full_converted)
    bot.reply_to(message, text)
    # запрашиваем данные из базы
    ans = dbService.getAnwerByQuestion(str(text).lower())
    if ans == None:
         ans = "К сожалению, ничего не нашел!"
    else:
        bot.send_message(message.chat.id,ans)
    # удаляем созданные файлы
    os.remove(file_name_full)
    os.remove(file_name_full_converted)

# Распознование голоса
def recogniseVoice(filename):
    r = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio_text = r.record(source)
        try:
            text = r.recognize_google(audio_text,language=language)
            print('Преобарзую аудио в текст ...')
            print(text)
            return text
        except:
            print('Извините.. Не удалось распознать...')
            return "Извините.. Не удалось распознать..."

bot.infinity_polling()