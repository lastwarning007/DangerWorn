import telebot, json, datetime, time
from datetime import datetime

try:
  with open('./config.json', 'r') as f:
    config = json.load(f)
except FileNotFoundError:
  config = {}
  
bot = telebot.TeleBot(config['TOKEN'])

with open("./data/database.json") as e:
  db = json.load(e)
  
with open("./data/admin.json") as e:
  admin = json.load(e)
  admins = admin["admin"]
  
def check_username(chat_id):
  try:
    chat_member = bot.get_chat_member(chat_id, chat_id)
    username = chat_member.user.username
    return f"{username}"
  except Exception as e:
    return f"Error: {e}"
  
def addplans(message):
  args = message.text.split(' ')
  user_id = message.from_user.id
  if user_id not in admins:
    bot.reply_to(message, f'You not admin access.')
    return
  
  if len(args) != 7:
    bot.reply_to(message, 'Using: /addplans [id] [expiry date] [max attack times] [max cons] [cooldown] [plans]\n/addplans 1918282 2025-10-24 60 50 60 basic')
    return
  
  target_user_id = int(args[1])
  expiry_date_str = args[2]
  maxtime = int(args[3])
  maxcons = int(args[4])
  cooldown = int(args[5])
  plans = str(args[6])
  expired = datetime.strptime(expiry_date_str, '%Y-%m-%d')
  db["userid"][str(target_user_id)]= {"exp": expired.strftime('%Y-%m-%d'), "maxTime": maxtime, "cooldown": cooldown,"plans": plans.upper(), "maxCons": maxcons, "curCons": 0}
  with open("./data/database.json", "w") as json_file:
    json.dump(db, json_file, indent=4)
  bot.reply_to(message, f"Username: {check_username(target_user_id)}\nExpiry Date: {expired}\nMax Time: {maxtime}\nMax Cons: {maxcons}\nCooldown: {cooldown}\nPlans: {plans}")
        
def updateuser(message):
    args = message.text.split(' ')
    user_id = message.from_user.id
    if user_id not in admins:
        bot.reply_to(message, 'You do not have admin access.')
        return

    if len(args) != 7:
        bot.reply_to(message, 'Usage: /updateuser [id] [expiry date] [max attack times] [max cons] [cooldown] [plans]')
        return

    target_user_id = int(args[1])
    expiry_date_str = args[2]
    maxtime = int(args[3])
    maxcons = int(args[4])
    cooldown = int(args[5])
    plans = args[6].upper()
    expired = datetime.strptime(expiry_date_str, '%Y-%m-%d')
    
    db["userid"][str(target_user_id)]= {"exp": expired.strftime('%Y-%m-%d'), "maxTime": maxtime, "cooldown": cooldown,"plans": plans.upper(), "maxCons": maxcons, "curCons": 0}
    with open("./data/database.json", "w") as json_file:
       json.dump(db, json_file, indent=4)
    bot.reply_to(message, f"Username: {check_username(target_user_id)}\nExpiry Date: {expired}\nMax Time: {maxtime}\nMax Cons: {maxcons}\nCooldown: {cooldown}\nPlans: {plans}")

def userlist(message):
  user_id = message.from_user.id
  if user_id not in admins:
    bot.reply_to(message, f'You do not have admin access.')
    return
    
  userlist = ''
  for user_id, info in db['userid'].items():
    userlist += f"User ID: {user_id}\n"
    for key, value in info.items():
      userlist += f"{key}: {value}\n"
  bot.reply_to(message, userlist)
  
def removeplans(message):
  texts = message.text.split(' ')
  user_id = message.from_user.id
  if user_id not in admins:
    bot.reply_to(message, f'You not admin access.')
    return
  
  if len(texts) != 2:
      bot.reply_to(message, 'Using: /removeplans [id]')
      return
      
  user_ids = str(texts[1])
  if user_ids in db["userid"]:
    del db["userid"][user_ids]
    with open("./data/database.json", "w") as json_file:
      json.dump(db, json_file, indent=4)
    bot.reply_to(message, 'Removed {} from the access list.'.format(user_ids))
  else:
    bot.reply_to(message, 'User {} not in the access list.'.format(user_id))
    
def addserver(message):
  args = message.text.split(' ')
  user_id = message.from_user.id
  if user_id not in admins:
    bot.reply_to(message, 'You do not have admin access.')
    return
    
  if len(args) != 4:
    bot.reply_to(message, 'Usage: /addserver [hostname] [username] [password]')
    return
      
  try:
    with open("./data/vps_servers.json", "r") as json_file:
      db = json.load(json_file)
  except FileNotFoundError:
    db = []
    
  hostname, username, password = args[1], args[2], args[3]
  db.append({"hostname": hostname, "username": username, "password": password})
  with open("./data/vps_servers.json", "w") as json_file:
    json.dump(db, json_file, indent=4)
        
  bot.reply_to(message, f"Server Successfully Added\nHostname: {hostname}\nUsername: {username}\nPassword: {password}")
