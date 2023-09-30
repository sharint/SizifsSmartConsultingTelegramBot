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
BACK = "Назад"


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    markup = createStartMarkup()
    bot.reply_to(message, "Привет! Я бот-помощник sizif. Чем могу помочь?",reply_markup=markup)
     
@bot.message_handler(content_types=['text'])
def func(message):
    if(message.text == GLOSSARIY):
        markup = createBackMarkup()
        bot.send_message(message.chat.id,text="Вы выбрали глоссарий, напшите что вы хотите найти",reply_markup=markup)
        bot.register_next_step_handler(message, glossaryAnswer)
    elif(message.text == AI):
        markup = createBackMarkup()
        bot.send_message(message.chat.id,text="Вы выбрали искусственый интелект, напшите что вы хотите найти",reply_markup=markup)
        bot.register_next_step_handler(message, aiAnswer)
    elif(message.text == BACK):
        markup = createStartMarkup()
        text = "Возвращаю в главное меню"
        bot.send_message(message.chat.id,text=text,reply_markup=markup)
        
def glossaryAnswer(message):
    text = message.text
    if text == BACK:
        markup = createStartMarkup()
        bot.send_message(message.chat.id, text="Возвращаю назад",reply_markup=markup)
        return
    ans = dbService.getAnwerByQuestion(str(message.text).lower())
    bot.send_message(message.from_user.id,text=ans)

def aiAnswer(message):
    text = message.text
    if text == BACK:
        markup = createStartMarkup()
        bot.send_message(message.chat.id, text="Возвращаю назад",reply_markup=markup)
        return
    ans = "Вам ответил искусственый интелект"
    bot.send_message(message.from_user.id,text=ans)

    
     
    

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

def createStartMarkup():
    markup = types.ReplyKeyboardMarkup()
    glosBtn = types.KeyboardButton(GLOSSARIY)
    aiBtn = types.KeyboardButton(AI)
    markup.add(glosBtn,aiBtn)
    return markup

def createBackMarkup():
    markup = types.ReplyKeyboardMarkup()
    backBtn = types.KeyboardButton(BACK)
    markup.add(backBtn)
    return markup


bot.infinity_polling()