import telebot
from config import *
from logic import *

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Привет! Я бот, который может показывать города на карте. Напиши /help для списка команд.")

@bot.message_handler(commands=['help'])
def handle_help(message):
    bot.send_message(message.chat.id, "Доступные команды:\n"
                             "/show_city [Название города] - Показать город на карте\n"
                             "/remember_city [Название города] - Запомнить город\n"
                             "/show_my_cities - Показать все запомненные города\n"
                             "/set_marker_color [цвет] - Изменить цвет маркеров\n"
                             "/show_countries - Показать контуры стран на карте\n"
                             "/show_continents - Показать контуры континентов\n"
                             "/show_oceans - Показать океаны на карте")

@bot.message_handler(commands=['show_city'])
def handle_show_city(message):
    city_name = message.text.split()[-1]
    try:
        manager.create_graph(city_name, marker_color=manager.get_marker_color(message.chat.id))
        bot.send_photo(message.chat.id, open('map.png', 'rb'))
    except Exception as e:
        bot.send_message(message.chat.id, f'Ошибка: {e}')

@bot.message_handler(commands=['remember_city'])
def handle_remember_city(message):
    user_id = message.chat.id
    city_name = message.text.split()[-1]
    if manager.add_city(user_id, city_name):
        bot.send_message(message.chat.id, f'Город {city_name} успешно сохранен!')
    else:
        bot.send_message(message.chat.id, 'Такого города я не знаю. Убедись, что он написан на английском!')

@bot.message_handler(commands=['show_my_cities'])
def handle_show_visited_cities(message):
    cities = manager.select_cities(message.chat.id)
    try:
        manager.create_graph(cities, marker_color=manager.get_marker_color(message.chat.id))
        bot.send_photo(message.chat.id, open('map.png', 'rb'))
    except Exception as e:
        bot.send_message(message.chat.id, f'Ошибка: {e}')

@bot.message_handler(commands=['set_marker_color'])
def handle_set_marker_color(message):
    color = message.text.split()[-1]
    manager.set_marker_color(message.chat.id, color)
    bot.send_message(message.chat.id, f'Цвет маркеров изменен на {color}')

@bot.message_handler(commands=['show_countries'])
def handle_show_countries(message):
    try:
        manager.create_graph(countries=True, marker_color=manager.get_marker_color(message.chat.id))
        bot.send_photo(message.chat.id, open('map.png', 'rb'))
    except Exception as e:
        bot.send_message(message.chat.id, f'Ошибка: {e}')

@bot.message_handler(commands=['show_continents'])
def handle_show_continents(message):
    try:
        manager.create_graph(continents=True, marker_color=manager.get_marker_color(message.chat.id))
        bot.send_photo(message.chat.id, open('map.png', 'rb'))
    except Exception as e:
        bot.send_message(message.chat.id, f'Ошибка: {e}')

@bot.message_handler(commands=['show_oceans'])
def handle_show_oceans(message):
    try:
        manager.create_graph(oceans=True, marker_color=manager.get_marker_color(message.chat.id))
        bot.send_photo(message.chat.id, open('map.png', 'rb'))
    except Exception as e:
        bot.send_message(message.chat.id, f'Ошибка: {e}')

if __name__ == "__main__":
    manager = DB_Map.db(DATABASE)
    manager.create_user_table()
    bot.polling()
