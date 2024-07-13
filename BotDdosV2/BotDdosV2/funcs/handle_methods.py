import telebot, json
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

try:
  with open('./config.json', 'r') as f:
    config = json.load(f)
except FileNotFoundError:
  config = {}
  
bot = telebot.TeleBot(config['TOKEN'])

def show_methods_layer7b(chat_id):
    methods = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    methods.add(KeyboardButton('HTTPS'), KeyboardButton('TLS'))
    methods.add(KeyboardButton('❌ Cancel'))
    bot.send_message(chat_id, 'Please select an attack method:', reply_markup=methods)
    
def show_methods_layer7v(chat_id):
    methods = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    methods.add(KeyboardButton('STROM'), KeyboardButton('POWER'))
    methods.add(KeyboardButton('❌ Cancel'))
    bot.send_message(chat_id, 'Please select an attack method:', reply_markup=methods)

def show_methods_layer4(chat_id):
    methods = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    methods.add(KeyboardButton('UDP'),KeyboardButton('TCP'))
    methods.add(KeyboardButton('❌ Cancel'))
    bot.send_message(chat_id, 'Please select an attack method:', reply_markup=methods)
    
def show_layer(chat_id):
    layer = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    layer.add(KeyboardButton('Layer4'), KeyboardButton('Layer7'))
    layer.add(KeyboardButton('❌ Cancel'))
    bot.send_message(chat_id, 'Selected Layer attack : ', reply_markup=layer)
