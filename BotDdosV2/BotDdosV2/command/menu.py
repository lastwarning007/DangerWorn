import requests, json, time, telebot, datetime
from datetime import datetime

try:
  with open('./config.json', 'r') as f:
    config = json.load(f)
except FileNotFoundError:
  config = {}
  
bot = telebot.TeleBot(config['TOKEN'])

with open("./data/database.json") as e:
  db = json.load(e)
  
def check_username(chat_id):
  try:
    chat_member = bot.get_chat_member(chat_id, chat_id)
    username = chat_member.user.username
    return f"{username}"
  except Exception as e:
    return f"Error: {e}"
        
def my_plans(message):
  user_id = message.from_user.id
  userid = str(user_id)
  info = db['userid'].get(userid)
  if info:
    username = check_username(user_id) or f'Unknown user {user_id}'
    expiry_date = datetime.strptime(info['exp'], '%Y-%m-%d')
    expiry_date_str = expiry_date.strftime('%Y-%m-%d')
        
    max_duration_str = str(info['maxTime'])
    concurrents = info['curCons']
    max_cons = info['maxCons']
    plans = str(info["plans"])
    cooldown = str(info["cooldown"])
        
    bot.reply_to(message, f'Plan details for @{username}\nUser ID: {user_id}\nExpire Time: {expiry_date_str}\nMax Time: {max_duration_str} seconds\nMax Cons: {max_cons}\nConcurrents: {concurrents}\nPlans: {plans.upper()}\nCooldown: {cooldown}')
  else:
    bot.reply_to(message, 'You havent purchased a plan yet.')
