import telebot
from telebot import types
from config import API
from database import *
from send_gpt_post import send_post_request
from content_settings import content
from logs_settings import *

bot = telebot.TeleBot(API)
create_table()

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    logging.debug(f'/start - {user_id}')
    bot.send_message(user_id, 'Добро пожаловать в умного помощника по физике и химии.'
                              'Выберите предмет и уровень знаний для получения ответа!')
    data = get_users_data('user_id')
    if (user_id,) not in data:
        set_user_data(user_id)
    settings_subject(message, user_id)

@bot.message_handler(commands=['info'])
def info(message):
    user_id = message.chat.id
    bot.send_message(user_id, '''Доступные команды
    /start - запуск бота
    /continue - продолжение ответа
    /debug - логи''')

def settings_subject(message, user_id):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('физика', callback_data='физика'),
               types.InlineKeyboardButton('химия', callback_data='химия'))
    msg = bot.send_message(user_id, 'Выберите предмет', reply_markup=markup)
    update_user_data('user_msg', msg.id, user_id)

def settings_level(message, user_id, msg):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('easy', callback_data='easy'),
               types.InlineKeyboardButton('hard', callback_data='hard'))
    bot.edit_message_text(message_id=msg, chat_id=user_id,
                          reply_markup=markup, text='Выберите уровень знаний')

@bot.message_handler(commands=['continue'])
def continue_answer(message):
    user_id = message.chat.id
    data = get_user_data(user_id)
    gpt_answer = data[0][-1]
    user_message = data[0][-2]
    subject = data[0][3]
    level = data[0][4]
    assistant_content = "Решим задачу по шагам: " + gpt_answer
    system_content = content[subject][level]
    answer = send_post_request(user_id, user_message,
                               assistant_content, system_content)
    bot.send_message(user_id, answer)

@bot.message_handler(commands=['debug'])
def debug(message):
    logging.debug(f'Получены логи пользователем {message.chat.id}')
    with open('logs.txt', encoding='utf-8') as file:
        bot.send_document(message.chat.id, file)

@bot.message_handler()
def question(message):
    user_id = message.chat.id
    user = get_user_data(user_id)
    subject, level = user[0][3], user[0][4]
    if not subject:
        bot.send_message(user_id, 'Сначала выберите предмет')
    elif not level:
        bot.send_message(user_id, 'Выберите уровень знаний')
    else:
        update_user_data('question', message.text, user_id)
        system_content = content[subject][level]
        answer = send_post_request(user_id, message.text,
                          system_content=system_content)
        update_user_data('answer', answer, user_id)
        bot.send_message(user_id, answer)

@bot.callback_query_handler(func = lambda call: True)
def call_data(call):
    user_id = call.message.chat.id
    data = get_user_data(user_id)
    msg = data[0][2]
    if call.data in ('физика', 'химия'):
        update_user_data('subject', call.data, user_id)
        settings_level(call.message, user_id, msg)
    elif call.data in ('hard', 'easy'):
        update_user_data('level', call.data, user_id)
        bot.edit_message_text(message_id=msg, chat_id=user_id,
                              text='Введите ваш запрос: ', reply_markup=None)

if __name__ == '__main__':
    bot.polling()