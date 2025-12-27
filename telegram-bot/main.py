import os

import telebot
from telebot import types


TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

bot = telebot.TeleBot(TOKEN)




# Единый обработчик команды /start
@bot.message_handler(commands=['start'])
def start_command(message):


    markup_reply = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    btn_about = types.KeyboardButton('О самоуправлении')
    btn_news = types.KeyboardButton('Новости')
    btn_site = types.KeyboardButton('Сайт')
    markup_reply.add(btn_about, btn_news)  # Добавляем кнопки в один ряд
    markup_reply.add(btn_site) # Добавляем кнопку "Сайт" в Reply-клавиатуру

    # Создаем Inline-клавиатуру для ссылки на сайт (появляется внутри сообщения)
    # Эту Inline-кнопку вы отправляете сразу при старте, она ведет на сайт.
    # Обратите внимание, что переменная `btn_site` здесь отличается от `btn_site_reply` выше,
    # даже если они названы одинаково, это разные объекты
    markup_inline = types.InlineKeyboardMarkup()
    btn_site_start = types.InlineKeyboardButton('Перейти на сайт "Будь в движении"', url='https://www.youtube.com/')
    markup_inline.add(btn_site_start)

    bot.send_message(
        message.chat.id,
        'Привет! Я бот самоуправления.\n\n'
        'Используй кнопки ниже для навигации или введи /help для подсказок.',
        reply_markup=markup_reply  # Отправляем Reply-клавиатуру
    )
    bot.send_message(
        message.chat.id,
        'Ты также можешь перейти на наш официальный сайт:',
        reply_markup=markup_inline  # Отправляем Inline-клавиатуру
    )


# Обработчик команды /help
@bot.message_handler(commands=['help'])
def help_command(message):

    bot.send_message(
        message.chat.id,
        'Я могу помочь тебе с информацией о нашем самоуправлении. '
        'Используй кнопки в главном меню для доступа к разделам "О самоуправлении", "Новости", "Контакты".\n'
        'Чтобы узнать свой ID, просто напиши "мой id".'
    )

# Обработчик для всех остальных текстовых сообщений
# func=lambda message: True означает, что этот обработчик будет вызван для любого текстового сообщения,
# которое не было обработано предыдущими @bot.message_handler (например, командами или кнопками с точным текстом).
@bot.message_handler(func=lambda message: True)
def handle_text_messages(message):
    chat_id = message.chat.id
    user_text = message.text.lower()  # Переводим текст в нижний регистр для удобства сравнения


    if user_text == 'мой id':
        bot.send_message(chat_id, f'Твой ID: {message.from_user.id}')
    elif user_text == 'о самоуправлении':
        bot.send_message(
            chat_id,
            'Мы - школьное самоуправление.'
        )
    elif user_text == 'новости':
        bot.send_message(
            chat_id,
            'Актуальные новости:\n'
            '- 16 декабря: школьный форум \n'
            '- 22 декабря: конкурс талантов \n'
            'Следите за обновлениями на нашем сайте и в социальных сетях!',
            parse_mode='Markdown'  # Используем Markdown для жирного текста
        )
    # --- НОВЫЙ ОБРАБОТЧИК ДЛЯ КНОПКИ "САЙТ" ИЗ REPLY-КЛАВИАТУРЫ ---
    elif user_text == 'сайт':

        # Создаем Inline-клавиатуру специально для этой цели
        markup_inline_for_site_button = types.InlineKeyboardMarkup()# Делает чтобы работали и кнопка сайт и текст
        # Добавляем Inline-кнопку с прямой ссылкой
        btn_link_to_site = types.InlineKeyboardButton('Перейти на наш сайт', url='https://www.youtube.com/')
        markup_inline_for_site_button.add(btn_link_to_site)

        bot.send_message(
            chat_id,
            'Нажмите кнопку ниже, чтобы перейти на наш официальный сайт:',
            reply_markup=markup_inline_for_site_button # Отправляем сообщение с Inline-кнопкой
        )
    # --- КОНЕЦ НОВОГО ОБРАБОТЧИКА ---
    else:
        # Если ни одно из предыдущих условий не сработало, бот отвечает, что не понял команду
        bot.send_message(chat_id, 'Извини, я тебя не понял. Пожалуйста, используй кнопки или команды /start, /help.')


# --- Запуск бота ---
if __name__ == '__main__': # Исправлено: __name__

    # bot.polling() запускает бесконечный цикл получения обновлений
    # none_stop=True делает так, чтобы бот не останавливался при возникновении ошибок, а продолжал работать
    bot.polling(none_stop=True)