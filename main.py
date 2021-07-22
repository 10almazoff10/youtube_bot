import telebot
import parce

print("Telegram bot by Prokin\nЗагружает с ютуб канала последнее видео\nVersion 0.0.2")
bot = telebot.TeleBot("1869428360:AAGb4_tSe7Fy8Agg2IdK4sNfpbNsV8wOLWM")

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "qq, напиши название канала на ютабе")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
	print("пришло сообщение от пользователя: " + message.text)
	bot.send_message(message.chat.id, "Загружаю..")
	print("начинается парсинг..")
	lists = parce.parse(message.text)
	if type(lists) != str:
		to_user = f"{lists[0]['channel_name']}\n{lists[0]['link']}"
		bot.send_message(message.chat.id, to_user)
		bot.send_photo(message.chat.id, open(lists[0]['pick'], "rb"), disable_notification=True)
		bot.send_message(message.chat.id, "Загружаю видео..." + lists[0]['video_name'], disable_notification=True)
		bot.send_video(message.chat.id, open(lists[0]['last_video'], "rb", ), timeout=500, disable_notification=True)
		print("Видео успешно отправлено")
	elif type(lists) == str:
		bot.send_message(message.chat.id, lists)
	else:
		bot.send_message(message.chat.id, "Возникла непредвиденная ошибка")
bot.polling()

