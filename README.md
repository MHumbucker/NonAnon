# Telegram NonAnon Bot

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Telegram](https://img.shields.io/badge/Telegram-Bot_API-green.svg)
![License: MIT](https://img.shields.io/badge/license-MIT-orange.svg)

---
## English

## Description

This bot allows users to send *"anonymous"* messages to Telegram channel administrators — which in fact are **not anonymous**.  
Administrators can:

- Reply to messages  
- Ban/unban users  
- Send mass notifications

---

## Language Support

- 🇷🇺 Russian (`language = 7`)  
- 🇬🇧 English (`language = 1`)

---

## Installation & Setup

### 1. Requirements

- Python 3.8+  
- Dependencies:

```bash
pip install pyTelegramBotAPI
```

### 2. Bot Configuration

- Get a token from @BotFather  
- Insert it into the code:

```python
bot = telebot.TeleBot("TOKEN")  # Replace "TOKEN" with your actual token
```

- Set the admin IDs:

```python
ADMINS = {777}  # Replace with real IDs
```

- (Optional) Set the channel ID for broadcasting:

```python
CHANNEL_ID = -888  # Replace with your channel's ID
```

---

## Features

### For Users

- `/start` – Welcome message  
- Send anonymous messages (text, photo, video, documents, etc.)

### For Administrators

- **Ban / Unban users**  
  *Menu: “Ban” → select user → Ban / Unban*
- **Reply to messages**  
  *Reply to the incoming message from the user*
- **Mass notification broadcast**  
  *Menu: “Message users” → input text + attachments*

---

## File Structure

- `ban_list.json` – List of banned users  
- `message_log.json` – Message log (used for replies)

---

## Running the Bot

```bash
python nonanon.py
```


---
## Русский

## Описание

Этот бот позволяет пользователям отправлять *"анонимные"* сообщения администраторам Telegram-канала, которые по факту анонимными не являются.  
Администраторы могут:

- Отвечать на сообщения
- Банить/разбанивать пользователей
- Массово рассылать уведомления

---

## Поддержка языков

- 🇷🇺 Русский (`language = 7`)
- 🇬🇧 Английский (`language = 1`)

---

##  Установка и настройка

### 1. Требования

- Python 3.8+
- Зависимости:

```bash
pip install pyTelegramBotAPI
```

### 2. Настройка бота

- Получите токен у @BotFather
- Вставьте его в код:
```python
bot = telebot.TeleBot("TOKEN")  # Замените "TOKEN" на ваш токен
```
- Укажите ID администраторов:
```python
ADMINS = {777}  # Замените на реальные ID
```
- (Опционально) Укажите ID канала для рассылки:
```python
CHANNEL_ID = -888  # Замените на ID вашего канала
```
## Функционал

### Для пользователей
- `/start` – Приветственное сообщение  
- Отправка анонимных сообщений (текст, фото, видео, документы и др.)

### Для администраторов
- **Бан / Разбан пользователей**  
  *Меню: «Бан» → выбрать пользователя → Бан / Разбан*
- **Ответ на сообщения**  
  *Ответьте реплаем на входящее сообщение от пользователя*
- **Массовая рассылка уведомлений**  
  *Меню: «Сообщение пользователям» → ввод текста + вложения*

---

## Структура файлов

- `ban_list.json` – Список забаненных пользователей  
- `message_log.json` – Лог сообщений (используется для ответов администратора)

---

## Запуск бота

```bash
python nonanon.py
```

