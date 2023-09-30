from telebot import types
import telebot
import dbService
import uuid
import os
import speech_recognition as sr

token = "6339026680:AAHFh25ZDH2bxLvuNIvH7bQLYI6Y6MpPjsU"
bot = telebot.TeleBot(token, parse_mode=None)
language='ru_RU'

GLOSSARIY = "Глоссарий"
AI = "Исскуственный интелект"

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	markup = types.ReplyKeyboardMarkup()
	btn = types.KeyboardButton(GLOSSARIY)
	markup.add(btn)
	bot.reply_to(message, "Привет! Я бот-помощник sizif. Чем могу помочь?",reply_markup=markup)
     
@bot.message_handler(content_types=['text'])
def func(message):
	if(message.text == GLOSSARIY):
		switchKeyboardbutton(message,AI)
	if(message.text == AI):
		switchKeyboardbutton(message,GLOSSARIY)
	
@bot.message_handler(func=lambda m: True)
def echo_all(message):
	ans = dbService.getAnwerByQuestion(str(message.text).lower())
	bot.send_message(message.chat.id,ans)
	

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

@bot.message_handler(content_types=['voice'])
def voice_processing(message):
    filename = str(uuid.uuid4())
    file_name_full="./voice/"+filename+".ogg"
    file_name_full_converted="./ready/"+filename+".wav"
    file_info = bot.get_file(message.voice.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(file_name_full, 'wb') as new_file:
        new_file.write(downloaded_file)


    os.system("ffmpeg -i "+file_name_full+"  "+file_name_full_converted)
    text=recogniseVoice(file_name_full_converted)
    bot.reply_to(message, text)
    os.remove(file_name_full)
    os.remove(file_name_full_converted)

def switchKeyboardbutton(message,buttonText):
	markup = types.ReplyKeyboardMarkup()
	btn = types.KeyboardButton(buttonText)
	markup.add(btn)
	text = "Теперь я беру данные из "+ buttonText
	bot.send_message(message.chat.id,text=text,reply_markup=markup)

bot.infinity_polling()