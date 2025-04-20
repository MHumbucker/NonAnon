import telebot
import time
import json
import os
from telebot.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

bot = telebot.TeleBot("TOKEN") #change
language = 1 #1 - US, 7 - RU
ADMINS = {777} # change
CHANNEL_ID = 888 # change
users = {}
message_logs = {}

BAN_LIST_FILE = 'ban_list.json'
LOG_FILE = 'message_log.json'

def load_data():
	global users
	if os.path.exists(BAN_LIST_FILE):
		with open(BAN_LIST_FILE, 'r') as file:
			users = json.load(file)

def save_data():
	with open(BAN_LIST_FILE, 'w') as file:
		json.dump(users, file)

def load_message_logs():
	global message_logs
	if os.path.exists(LOG_FILE):
		with open(LOG_FILE, 'r') as file:
			message_logs = json.load(file)

def save_message_logs():
	with open(LOG_FILE, 'w') as file:
		json.dump(message_logs, file)

def admin_menu():
	markup = ReplyKeyboardMarkup(resize_keyboard=True)
	if language == 7:
		markup.add("Бан меню", "Сообщение пользователям")
	else:
		markup.add("Ban menu", "Message users")
	return markup

def ban_menu():
	markup = ReplyKeyboardMarkup(resize_keyboard=True)
	if language == 7:
		markup.add("Бан", "Разбан", "Назад")
	else:
		markup.add("Ban", "Unban", "Back")
	return markup

def yes_no_menu():
	markup = ReplyKeyboardMarkup(resize_keyboard=True)
	if language == 7:
		markup.add("Да", "Нет")
	else:
		markup.add("Yes", "No")
	return markup

def cancel_menu():
	markup = ReplyKeyboardMarkup(resize_keyboard=True)
	if language == 7:
		markup.add("Отмена")
	else:
		markup.add("Cancel")
	return markup

def start_start():
	try:
		if language == 7:
			bot.send_message(ADMINS, "Бот запущен")
		else:
			bot.send_message(ADMINS, "Bot started")
	except:
		return

start_start()

@bot.message_handler(func=lambda message: message.from_user.id in ADMINS and (message.text == "Бан меню" or message.text == "Ban menu"))
def show_ban_menu(message):
	if language == 7:
		bot.send_message(message.chat.id, "🔒 Выберите действие:", reply_markup=ban_menu())
	else:
		bot.send_message(message.chat.id, "🔒 Choose action:", reply_markup=ban_menu())

@bot.message_handler(func=lambda message: message.from_user.id in ADMINS and (message.text == "Назад" or message.text == "Back"))
def back_to_admin_menu(message):
	if language == 7:
		bot.send_message(message.chat.id, "🔧 Админ меню", reply_markup=admin_menu())
	else:
		bot.send_message(message.chat.id, "🔧 Admin menu", reply_markup=admin_menu())

@bot.message_handler(func=lambda message: message.from_user.id in ADMINS and (message.text == "Бан" or message.text == "Ban"))
def process_ban(message):
	if language == 7:
		bot.send_message(message.chat.id, "Введите UID пользователя для бана:")
	else:
		bot.send_message(message.chat.id, "Enter user UID to ban:")
	bot.register_next_step_handler(message, yn_ban)

@bot.message_handler(func=lambda message: message.from_user.id in ADMINS and (message.text == "Разбан" or message.text == "Unban"))
def process_unban(message):
	if language == 7:
		bot.send_message(message.chat.id, "Введите UID пользователя для разбана:")
	else:
		bot.send_message(message.chat.id, "Enter user UID to unban:")
	bot.register_next_step_handler(message, yn_unban)

def yn_ban(message):
	try:
		ban_id = int(message.text)
	except ValueError:
		if language == 7:
			bot.send_message(message.chat.id, "❌ Введите корректный UID!", reply_markup=admin_menu())
		else:
			bot.send_message(message.chat.id, "❌ Enter correct UID!", reply_markup=admin_menu())
		return

	users[ban_id] = 'ban'
	save_data()
	if language == 7:
		bot.send_message(message.chat.id, f"✅ Пользователь с UID {ban_id} забанен!", reply_markup=admin_menu())
	else:
		bot.send_message(message.chat.id, f"✅ User with UID {ban_id} banned!", reply_markup=admin_menu())

def yn_unban(message):
	try:
		ban_id = int(message.text)
	except ValueError:
		if language == 7:
			bot.send_message(message.chat.id, "❌ Введите корректный UID!", reply_markup=admin_menu())
		else:
			bot.send_message(message.chat.id, "❌ Enter correct UID!", reply_markup=admin_menu())
		return

	if users.get(ban_id) == 'ban':
		users[ban_id] = 'unban'
		save_data()
		if language == 7:
			bot.send_message(message.chat.id, f"✅ Пользователь с UID {ban_id} разбанен!", reply_markup=admin_menu())
		else:
			bot.send_message(message.chat.id, f"✅ User with UID {ban_id} unbanned!", reply_markup=admin_menu())
	else:
		if language == 7:
			bot.send_message(message.chat.id, "❌ Этот пользователь не в бане!", reply_markup=admin_menu())
		else:
			bot.send_message(message.chat.id, "❌ This user is not banned!", reply_markup=admin_menu())

@bot.message_handler(func=lambda message: message.from_user.id in ADMINS and (message.text == "Сообщение пользователям" or message.text == "Message users"))
def ask_for_message_content(message):
	if language == 7:
		bot.send_message(message.chat.id, "Введите текст сообщения (/z для отмены):")
	else:
		bot.send_message(message.chat.id, "Enter message text (/z to cancel):")
	bot.register_next_step_handler(message, process_message_text)

def process_message_text(message):
	if message.text.lower() == "/z":
		if language == 7:
			bot.send_message(message.chat.id, "❌ Операция отменена.", reply_markup=admin_menu())
		else:
			bot.send_message(message.chat.id, "❌ Operation canceled.", reply_markup=admin_menu())
		return

	text = message.text
	if language == 7:
		bot.send_message(message.chat.id, "Отправь вложение /yes (/no если без вложений)")
	else:
		bot.send_message(message.chat.id, "Send attachment /yes (/no if no attachments)")
	bot.register_next_step_handler(message, ask_for_attachment, text)

def ask_for_attachment(message, text):
	if message.content_type == 'text' and message.text.lower() == "/no":
		if language == 7:
			bot.send_message(message.chat.id, "Отлично, вложений не будет.")
			bot.send_message(message.chat.id, "Введите ссылку для inline (/no если без ссылки):")
		else:
			bot.send_message(message.chat.id, "Okay, no attachments.")
			bot.send_message(message.chat.id, "Enter inline link (/no if no link):")
		bot.register_next_step_handler(message, ask_for_link, text, None, None) 
		return

	media_files = []
	if message.content_type == 'text' and message.text.lower() == "/yes":
		if language == 7:
			bot.send_message(message.chat.id, "Отправьте одно фото или видео (для завершения отправьте /no):")
		else:
			bot.send_message(message.chat.id, "Send one photo or video (send /no to finish):")
		bot.register_next_step_handler(message, process_attachments, text, media_files)
		return

	if language == 7:
		bot.send_message(message.chat.id, "Неверная команда. Пожалуйста, используйте /yes или /no.")
	else:
		bot.send_message(message.chat.id, "Invalid command. Please use /yes or /no.")
	bot.register_next_step_handler(message, ask_for_attachment, text)

def process_attachments(message, text, media_files):
	if message.content_type == 'text' and message.text.lower() == "/no":
		if language == 7:
			bot.send_message(message.chat.id, "Отлично, вложений нет.")
			bot.send_message(message.chat.id, "Введите ссылку для inline (/no если без ссылки):")
		else:
			bot.send_message(message.chat.id, "Okay, no attachments.")
			bot.send_message(message.chat.id, "Enter inline link (/no if no link):")
		bot.register_next_step_handler(message, ask_for_link, text, media_files, None)
		return

	if message.content_type in ['photo', 'video']:
		if len(media_files) >= 1:
			if language == 7:
				bot.send_message(message.chat.id, "Вы уже отправили одно вложение. Больше добавлять нельзя.")
			else:
				bot.send_message(message.chat.id, "You already sent one attachment. Can't add more.")
		else:
			media_files.append(message)

	if language == 7:
		bot.send_message(message.chat.id, "Введите ссылку для inline (/no если без ссылки):")
	else:
		bot.send_message(message.chat.id, "Enter inline link (/no if no link):")
	bot.register_next_step_handler(message, ask_for_link, text, media_files, None)

def ask_for_link(message, text, media_files, link):
	if message.text.lower() == "/no":
		if language == 7:
			bot.send_message(message.chat.id, "Отлично, без ссылки.")
		else:
			bot.send_message(message.chat.id, "Okay, no link.")
		send_message_to_users(message, text, media_files, None)
		return

	link = message.text
	send_message_to_users(message, text, media_files, link)

def send_message_to_users(message, text, media_files, link):
	confirmation_markup = yes_no_menu()
	if language == 7:
		bot.send_message(message.chat.id, "Вы хотите отправить следующее сообщение?", reply_markup=confirmation_markup)
	else:
		bot.send_message(message.chat.id, "Do you want to send this message?", reply_markup=confirmation_markup)

	final_message = f"Text: {text}\n" if language == 1 else f"Текст: {text}\n"
	if link:
		final_message += f"Link: {link}\n" if language == 1 else f"Ссылка: {link}\n"
	if media_files:
		final_message += f"Attachments: {len(media_files)} files.\n" if language == 1 else f"Вложения: {len(media_files)} файлов.\n"

	bot.send_message(message.chat.id, final_message)
	bot.register_next_step_handler(message, confirm_send_message, text, media_files, link)

def confirm_send_message(message, text, media_files, link):
	if message.text.lower() == "да" or message.text.lower() == "yes":
		sent_users = set()

		for user_id, status in users.items():
			if status == 'unban':
				if send_message_to_user(user_id, text, media_files, link):
					sent_users.add(user_id)

		try:
			chat_members = bot.get_chat_administrators(CHANNEL_ID)
			channel_members = bot.get_chat_members_count(CHANNEL_ID)
		except Exception as e:
			if language == 7:
				bot.send_message(message.chat.id, f"❌ Ошибка доступа к каналу: {e}", reply_markup=admin_menu())
			else:
				bot.send_message(message.chat.id, f"❌ Channel access error: {e}", reply_markup=admin_menu())
			return

		for user_id in channel_members:
			if user_id not in sent_users:
				send_message_to_user(user_id, text, media_files, link)

		if language == 7:
			bot.send_message(message.chat.id, "✅ Сообщение отправлено всем подходящим пользователям.", reply_markup=admin_menu())
		else:
			bot.send_message(message.chat.id, "✅ Message sent to all suitable users.", reply_markup=admin_menu())
	else:
		if language == 7:
			bot.send_message(message.chat.id, "❌ Операция отменена.", reply_markup=admin_menu())
		else:
			bot.send_message(message.chat.id, "❌ Operation canceled.", reply_markup=admin_menu())

def send_message_to_user(user_id, text, media_files, link):
	try:
		markup = InlineKeyboardMarkup()
		if link:
			if language == 7:
				markup.add(InlineKeyboardButton("Перейти", url=link))
			else:
				markup.add(InlineKeyboardButton("Go", url=link))

		if media_files:
			for file in media_files:
				if file.content_type == 'photo':
					bot.send_photo(user_id, file.photo[0].file_id, caption=text, reply_markup=markup)
				elif file.content_type == 'video':
					bot.send_video(user_id, file.video.file_id, caption=text, reply_markup=markup)
		else:
			bot.send_message(user_id, text, reply_markup=markup)
		return True
	except Exception as e:
		print(f"Error sending message to user {user_id}: {e}")
		return False

@bot.message_handler(commands=['start'])
def start(message):
	user_id = message.from_user.id
	if user_id not in users:
		users[user_id] = 'unban'

	if user_id in ADMINS:
		bot.send_message(user_id, "🔧 Админ меню" if language == 7 else "🔧 Admin menu", reply_markup=admin_menu())
	else:
		if language == 7:
			bot.send_message(user_id, "🔥 Добро пожаловать в бот анонимных сообщений канала *Лучший канал*!\n\n✉️ Здесь вы можете отправить анонимное сообщение администраторам.\n📸 Просто отправьте текст, фото, видео или документ.\n💬 Ваше сообщение будет доставлено анонимно!", parse_mode="Markdown")
		else:
			bot.send_message(user_id, "🔥 Welcome to the *Best channel* anonymous messages bot!\n\n✉️ Here you can send anonymous messages to admins.\n📸 Just send text, photo, video or document.\n💬 Your message will be delivered anonymously!", parse_mode="Markdown")

@bot.message_handler(content_types=['text', 'photo', 'video', 'document', 'sticker', 'voice', 'video_note', 'animation'])
def handle_message(message):
	user_id = message.from_user.id

	if user_id in ADMINS and message.reply_to_message:
		reply_text = message.text or ("[No text]" if language == 1 else "[Нет текста]")
		if message.reply_to_message.message_id in message_logs:
			sender_id, _ = message_logs[message.reply_to_message.message_id]
			if language == 7:
				bot.send_message(message.chat.id, "✅ Успешно!")
			else:
				bot.send_message(message.chat.id, "✅ Success!")
		else:
			if language == 7:
				bot.send_message(message.chat.id, "❌ Ошибка! Невозможно определить получателя.")
			else:
				bot.send_message(message.chat.id, "❌ Error! Can't determine recipient.")
			return

		try:
			if language == 7:
				bot.send_message(sender_id, f"📩 *Ответ администратора:*\n\n{reply_text}", parse_mode="Markdown")
			else:
				bot.send_message(sender_id, f"📩 *Admin reply:*\n\n{reply_text}", parse_mode="Markdown")
		except Exception as e:
			if language == 7:
				bot.send_message(message.chat.id, f"❌ Ошибка при отправке ответа: {e}")
			else:
				bot.send_message(message.chat.id, f"❌ Error sending reply: {e}")
		return

	if users.get(user_id) == 'ban':
		if language == 7:
			bot.send_message(message.chat.id, "🚫 Вы забанены и не можете использовать этого бота.")
		else:
			bot.send_message(message.chat.id, "🚫 You are banned and can't use this bot.")
		return

	if user_id in ADMINS:
		if language == 7:
			bot.send_message(message.chat.id, "Вы админ, вам не нужно отправлять анонимные сообщения.")
		else:
			bot.send_message(message.chat.id, "You're admin, you don't need to send anonymous messages.")
		return

	if language == 7:
		user_info = f"👤 *Новый анонимный отправитель:*\n🔹 ID: `{user_id}`\n"
	else:
		user_info = f"👤 *New anonymous sender:*\n🔹 ID: `{user_id}`\n"

	if message.from_user.username:
		safe_username = message.from_user.username.replace("_", "\\_")
		user_info += f"🔹 Username: @{safe_username}\n"
	if message.from_user.first_name:
		user_info += f"🔹 First name: {message.from_user.first_name}\n" if language == 1 else f"🔹 Имя: {message.from_user.first_name}\n"
	if message.from_user.last_name:
		user_info += f"🔹 Last name: {message.from_user.last_name}\n" if language == 1 else f"🔹 Фамилия: {message.from_user.last_name}\n"

	admins_notified = False

	for admin_id in ADMINS:
		try:
			bot.send_message(admin_id, user_info, parse_mode="Markdown")

			forwarded_message = None
			if message.text:
				forwarded_message = bot.send_message(admin_id, message.text)
			elif message.photo:
				forwarded_message = bot.send_photo(admin_id, message.photo[-1].file_id, caption=message.caption or "")
			elif message.animation:
				forwarded_message = bot.send_animation(admin_id, message.animation.file_id, caption=message.caption or "")
			elif message.video:
				forwarded_message = bot.send_video(admin_id, message.video.file_id, caption=message.caption or "")
			elif message.sticker:
				forwarded_message = bot.send_sticker(admin_id, message.sticker.file_id)
			elif message.voice:
				forwarded_message = bot.send_voice(admin_id, message.voice.file_id)
			elif message.video_note:
				forwarded_message = bot.send_video_note(admin_id, message.video_note.file_id)
			elif message.document:
				forwarded_message = bot.send_document(admin_id, message.document.file_id, caption=message.caption or "")
			else:
				if language == 7:
					bot.send_message(message.chat.id, "❌ Ошибка! Неподдерживаемый тип сообщения.")
				else:
					bot.send_message(message.chat.id, "❌ Error! Unsupported message type.")
				return

			if forwarded_message and forwarded_message.message_id not in message_logs:
				message_logs[forwarded_message.message_id] = [user_id, [admin_id]]
			elif forwarded_message:
				message_logs[forwarded_message.message_id][1].append(admin_id)

			save_message_logs()
			admins_notified = True
		except Exception as e:
			print(f"Error sending to admin {admin_id}: {e}")

	if admins_notified:
		if language == 7:
			bot.send_message(message.chat.id, "✅ Ваше анонимное сообщение доставлено.")
		else:
			bot.send_message(message.chat.id, "✅ Your anonymous message has been delivered.")
	else:
		if language == 7:
			bot.send_message(message.chat.id, "❌ Ошибка! Сообщение не доставлено.")
		else:
			bot.send_message(message.chat.id, "❌ Error! Message not delivered.")

load_data()
load_message_logs()

def run_bot():
	while True:
		try:
			bot.polling(none_stop=True, interval=0)
		except telebot.apihelper.ApiException as e:
			print(f"Telegram API error: {e}")
		except Exception as e:
			print(f"Error occurred: {e}")

		print("Lost connection to Telegram, waiting to reconnect...")
		time.sleep(5)

if __name__ == "__main__":
	run_bot()