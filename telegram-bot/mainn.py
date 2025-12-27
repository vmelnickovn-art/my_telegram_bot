
import os
import telebot
from telebot import types

# Убедитесь, что токен установлен в переменных окружения
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


bot = telebot.TeleBot(TOKEN)

# --- Вопросы и ответы ---
QA = {
    'about_what_is': {
        'question': 'Что такое ученическое самоуправление?',
        'answer': (
            "Ученическое самоуправление — это форма организации школьной жизни, при которой учащиеся "
            "принимают активное участие в управлении школой, решении вопросов, касающихся их интересов, "
            "и организации мероприятий. Это возможность для школьников влиять на школьную жизнь и развивать лидерские качества."
        )
    },
    'about_how_to_join': {
        'question': 'Как стать членом органов ученического самоуправления?',
        'answer': (
            "Чтобы стать членом органов самоуправления, нужно пройти выборы или конкурс. "
            "Обычно это происходит через классные собрания, где учащиеся выдвигают кандидатов, "
            "а затем голосуют за них. Важно проявлять инициативу, быть активным и готовым брать на себя ответственность."
        )
    }
}
# ------------------------


# Единый обработчик команды /start
@bot.message_handler(commands=['start'])
def start_command(message):
    markup_reply = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    btn_about = types.KeyboardButton('О самоуправлении')
    btn_news = types.KeyboardButton('Новости')
    btn_site = types.KeyboardButton('Сайт')
    markup_reply.add(btn_about, btn_news)
    markup_reply.add(btn_site)

    markup_inline = types.InlineKeyboardMarkup()
    btn_site_start = types.InlineKeyboardButton('Перейти на сайт "Будь в движении"', url='https://www.youtube.com/')
    markup_inline.add(btn_site_start)

    bot.send_message(
        message.chat.id,
        'Привет! Я бот самоуправления.\n\n'
        'Используй кнопки ниже для навигации или введи /help для подсказок.',
        reply_markup=markup_reply
    )
    bot.send_message(
        message.chat.id,
        'Ты также можешь перейти на наш официальный сайт:',
        reply_markup=markup_inline
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
@bot.message_handler(func=lambda message: True)
def handle_text_messages(message):
    chat_id = message.chat.id
    user_text = message.text.lower()

    if user_text == 'мой id':
        bot.send_message(chat_id, f'Твой ID: {message.from_user.id}')

    # --- ОБНОВЛЕННЫЙ ОБРАБОТЧИК ДЛЯ КНОПКИ "О САМОУПРАВЛЕНИИ" ---
    elif user_text == 'о самоуправлении':
        # Создаем Inline-клавиатуру с вопросами
        markup_about = types.InlineKeyboardMarkup()
        
        # Кнопка 1: Что такое ученическое самоуправление?
        btn_what_is = types.InlineKeyboardButton(
            QA['about_what_is']['question'], 
            callback_data='about_what_is' # Используем ключ из словаря QA
        )
        
        # Кнопка 2: Как стать членом органов ученического самоуправления?
        btn_how_to_join = types.InlineKeyboardButton(
            QA['about_how_to_join']['question'], 
            callback_data='about_how_to_join' # Используем ключ из словаря QA
        )
        
        markup_about.add(btn_what_is)
        markup_about.add(btn_how_to_join)

        bot.send_message(
            chat_id,
            'Мы - школьное самоуправление. Выберите интересующий вас вопрос:',
            reply_markup=markup_about
        )
    # -----------------------------------------------------------------

    elif user_text == 'новости':
        bot.send_message(
            chat_id,
            'Актуальные новости:\n'
            '- 16 декабря: школьный форум \n'
            '- 22 декабря: конкурс талантов \n'
            'Следите за обновлениями на нашем сайте и в социальных сетях!',
            parse_mode='Markdown'
        )
    elif user_text == 'сайт':
        markup_inline_for_site_button = types.InlineKeyboardMarkup()
        btn_link_to_site = types.InlineKeyboardButton('Перейти на наш сайт', url='https://www.youtube.com/')
        markup_inline_for_site_button.add(btn_link_to_site)

        bot.send_message(
            chat_id,
            'Нажмите кнопку ниже, чтобы перейти на наш официальный сайт:',
            reply_markup=markup_inline_for_site_button
        )
    else:
        bot.send_message(chat_id, 'Извини, я тебя не понял. Пожалуйста, используй кнопки или команды /start, /help.')


# --- НОВЫЙ ОБРАБОТЧИК ДЛЯ INLINE-КНОПОК (Callback Query) ---
@bot.callback_query_handler(func=lambda call: call.data in QA)
def callback_inline_questions(call):
    try:
        # Получаем данные, которые мы передали в callback_data (например, 'about_what_is')
        key = call.data
        
        # Получаем ответ из словаря QA
        response = f"*{QA[key]['question']}*\n\n{QA[key]['answer']}"
        
        # Отправляем ответ пользователю
        bot.send_message(
            call.message.chat.id, 
            response, 
            parse_mode='Markdown'
        )
        
        # Обязательно подтверждаем обработку запроса, чтобы убрать "часики" с кнопки
        bot.answer_callback_query(call.id)
        
    except Exception as e:
        print(f"Ошибка при обработке callback_query: {e}")
        bot.answer_callback_query(call.id, "Произошла ошибка при получении информации.")


# --- Запуск бота ---
if __name__ == '__main__':
    print("Бот запущен...")
    bot.polling(none_stop=True)
