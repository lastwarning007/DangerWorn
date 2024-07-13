import requests, json, socket, time, telebot

try:
  with open('./config.json', 'r') as f:
    config = json.load(f)
except FileNotFoundError:
  config = {}
  
bot = telebot.TeleBot(config['TOKEN'])

def checkhost(message):
    try:
        url = message.text.split()[1]
    except IndexError:
        bot.reply_to(message, """
Usage:
/checkhost <url_website>
Example:
/checkhost https://google.com
""")
        return
    
    if url.startswith("http://"):
        ip = url.split("http://")[1].split("/")[0]
    elif url.startswith("https://"):
        ip = url.split("https://")[1].split("/")[0]
    else:
        bot.reply_to(message, "Invalid URL format.")
        return

    try:
        socket.gethostbyname(ip)
        bot.reply_to(message, "Loading...")
        
        jsonfood = requests.get(f'https://check-host.net/check-http?host={ip}&max_nodes=15', headers={'Accept': 'application/json'})
        jsonfood = jsonfood.text
        j = json.loads(jsonfood)
        link = j['permanent_link']
        req_id = j["request_id"]
        time.sleep(12)
        jsonfood = requests.get(f'https://check-host.net/check-result/{req_id}', headers={'Accept': 'application/json'})
        jsonfood = jsonfood.text
        j = json.loads(jsonfood)

        response = f"HTTP response check-host result on {ip}\n\n"
        for x in j:
          timeout = 0
          try:
            for y in j[x][0]:
              emoji = "❌"
              if 100 <= int(j[x][0][3]) <= 199:
                emoji = "🌐"
              if 200 <= int(j[x][0][3]) <= 299:
                emoji = "✅"
              if 300 <= int(j[x][0][3]) <= 399:
                emoji = "⚠️"
              if 400 <= int(j[x][0][3]) <= 499:
                emoji = "❌"
              ptimeout = j[x][0][2]
          except TypeError:
            emoji = "❌"
            ptimeout = "Timeout"
          x = x.replace('.check-host.net', '')
          country_code = f"{x[0]}{x[1]}"
          country_info = requests.get(f'https://restcountries.com/v3.1/alpha/{country_code}')
          if country_info.status_code == 200:
            country_data = country_info.json()
            flagemoji = country_data[0].get('flag', 'Unknown')
            response += f"{flagemoji} : {emoji} {ptimeout}\n"
          else:
            response += f"Unknown : {emoji} {ptimeout}\n"
        response += f"\n[Check in website](https://check-host.net/check-http?host={url}&csrf_token=b840e00f710d178ff149ff35e463ff409f3b2504)\n"
        response += f"[Permanent link]({link})"
        bot.reply_to(message, response, parse_mode='Markdown')
    except socket.gaierror:
      bot.reply_to(message, f"{ip} is invalid, please retry")
      
def ipinfo(message):
    try:
        url = message.text.split()[1]
        if url.startswith("http://"):
          host = url.split("http://")[1].split("/")[0]
        elif url.startswith("https://"):
          host = url.split("https://")[1].split("/")[0]
        else:
          host = url
    except IndexError:
        bot.reply_to(message, "Please enter host/url\n(e.g, /ipinfo 8.8.8.8")
        return
      
    try:
        r = requests.get(f"http://ip-api.com/json/{host}?fields=33292287")
        res = r.json()
        hasil = f"""
IP: {res['query']}
Continent: {res['continent']}
ContinentCode: {res['continentCode']}
Country: {res['country']}
Country: {res['countryCode']}
Region: {res['region']}
RegionName: {res['regionName']}
City: {res['city']}
District: {res['district']}
Zip: {res['zip']}
Lat: {res['lat']}
Lon: {res['lon']}
TimeZone: {res['timezone']}
Currency: {res['currency']}
Isp: {res['isp']}
Org: {res['org']}
As: {res['as']}
Asname: {res['asname']}
Reverse: {res['reverse']}
Mobile: {res['mobile']}
Proxy: {res['proxy']}
Hosting: {res['hosting']}
        """
        bot.reply_to(message, hasil)
    except Exception as e:
        bot.reply_to(message, f"Terjadi kesalahan: {str(e)}")