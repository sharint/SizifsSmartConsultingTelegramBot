import telebot
import uuid
import os
import speech_recognition as sr

language='ru_RU'
TOKEN='6339026680:AAHFh25ZDH2bxLvuNIvH7bQLYI6Y6MpPjsU'
bot = telebot.TeleBot(TOKEN)



def recogniseVoice(filename):
    r = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio_text = r.record(source)
        try:
            text = r.recognize_google(audio_text,language=language)
            print('Converting audio transcripts into text ...')
            print(text)
            return text
        except:
            print('Извините.. Не удалось распознать...')
            return "Извините.. Не удалось распознать..."

@bot.message_handler(content_types=['voice'])
def voice_processing(message):
    filename = str(uuid.uuid4())
    file_name_full="DigitStripsKFC/voice/"+filename+".ogg"
    file_name_full_converted="DigitStripsKFC/ready/"+filename+".wav"
    file_info = bot.get_file(message.voice.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(file_name_full, 'wb') as new_file:
        new_file.write(downloaded_file)


    os.system("ffmpeg -i "+file_name_full+"  "+file_name_full_converted)
    text=recogniseVoice(file_name_full_converted)
    bot.reply_to(message, text)
    os.remove(file_name_full)
    os.remove(file_name_full_converted)

bot.polling()