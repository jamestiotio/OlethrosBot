# coding=utf-8
# Olethros Bot
# A multi-functional butler bot for SUTD Class 19F07 Telegram Group
# Written by James Raphael Tiovalen - @jamestiotio (2019)
# Only for personal use

# Import libraries

import sys
import os
import logging
import datetime
import secrets
import json
from bson import json_util
import re
import traceback
from functools import wraps
from tabulate import tabulate
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, \
    CallbackQueryHandler, ConversationHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, \
    KeyboardButton, ReplyKeyboardMarkup, ParseMode
from rextester import Rextester, RextesterException
import botinfo
from dbhelper import DBHelper
from flask import Flask

app = Flask(__name__)

# Initialize global variables
BOT_TOKEN = botinfo.BOT_TOKEN
ADMIN_LIST = botinfo.ADMIN_LIST
main_chat = botinfo.main_chat
private_chat = botinfo.private_chat
bot = telegram.Bot(token=BOT_TOKEN)
# Create the EventHandler and pass it the bot's token.
updater = Updater(token=BOT_TOKEN)
job_queue = updater.job_queue

rextester = Rextester()

# Setup webhook if necessary
# WEBHOOK_URL = botinfo.WEBHOOK_URL
# PORT = int(os.environ.get('PORT', '8443'))

db = DBHelper()

ladder = {
    8  : 'Legendary',
    7  : 'Epic',
    6  : 'Fantastic',
    5  : 'Superb',
    4  : 'Great',
    3  : 'Good',
    2  : 'Fair',
    1  : 'Average',
    0  : 'Mediocre',
    -1 : 'Poor',
    -2 : 'Terrible'
}

fate_options = { 
        -1 : '[-]', 
        0  : '[  ]', 
        1  : '[+]' 
}

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s -'
                           '%(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def get_ladder(result):
    if result > 8:
        return 'Beyond Legendary'
    elif result < -2:
        return 'Beyond Terrible'
    else:
        return ladder[result]


# Only accessible if `user_id` is in `ADMIN_LIST`
def restricted(func):
    @wraps(func)
    def wrapped(bot, update, *args, **kwargs):
        user_id = update.effective_user.id
        username = update.message.from_user.username if update.message.from_user.username else update.message.from_user.first_name
        if user_id not in ADMIN_LIST:
            reply_markup = telegram.ReplyKeyboardRemove()
            print('Unauthorized admin access denied for user {}.'
                  .format(user_id))
            bot.send_message(chat_id=update.message.chat_id,
                             text='Unauthorized admin access denied for user '
                                  '@{}.'.format(username),
                             reply_markup=reply_markup)
            return
        return func(bot, update, *args, **kwargs)

    return wrapped


# Only accessible in main group chat
def main_group(func):
    @wraps(func)
    def main_wrapped(bot, update, *args, **kwargs):
        chat_id = update.effective_message.chat_id
        user_id = update.effective_user.id
        if chat_id != main_chat:
            reply_markup = telegram.ReplyKeyboardRemove()
            print('Attempt by {} to start bot outside main chat detected.'
                  .format(user_id))
            bot.send_message(chat_id=chat_id,
                             text='Please interact with the bot in our SUTD Class 19F07 '
                              'main chat group instead. See you there!',
                             reply_markup=reply_markup)
            return
        return func(bot, update, *args, **kwargs)

    return main_wrapped


# I had an idea, but now I'm not sure on what to do with this command... ._.
@restricted
@main_group
def summon(bot, update):
    reply_markup = telegram.ReplyKeyboardRemove()
    bot.send_message(chat_id=main_chat,
                     text='I have been summoned!!! Aaaargh!',
                     reply_markup=reply_markup)
    bot.send_message(chat_id=main_chat,
                     text='... Nothing happened. 😔',
                     reply_markup=reply_markup)


@main_group
def start(bot, update):
    reply_markup = telegram.ReplyKeyboardRemove()
    bot.send_message(chat_id=main_chat,
                     text='Hi there! I am Olethros Bot, '
                          'a multi-functional butler bot for this class group.\r\n\r\n'
                          '• /track to initiate the daily birthday tracking function.\r\n'
                          '• /feelgood to send the feel-good message.\r\n'
                          '• /summon to attempt to summon a user.\r\n'
                          '• /run to execute snippets of code.\r\n'
                          '• /roll to roll different kinds of dice.\r\n'
                          '• /set_reminder to set a reminder.\r\n'
                          '• /vote to vote for an option in a currently active poll.\r\n'
                          '• /karma to add to, subtract from or check a user\'s karma points.\r\n'
                          '• /leaderboard to show a user karma list with non-zero karma.\r\n\r\n'
                          'If you need more help, please contact @jamestiotio.\r\n'
                          'I hope that you have a great day ahead!',
                     reply_markup=reply_markup)


@restricted
def stop(bot, update):
    sys.exit(0)


# Credit to @veetaw and @GingerPlusPlus for the Rextester functions
@main_group
def run(bot, update):
    message_text = update.effective_message.text

    if len(message_text.split(" ")) < 3:
        return

    stdin = ''
    if "\stdin" in message_text:
        stdin = ' '.join(message_text.split('\stdin ')[1:])
        message_text = message_text.replace('\stdin ' + stdin, '')

    language = message_text.split(' ')[1].lower()
    
    if message_text.split(' ')[2:].startswith("```", 0, 3) and message_text.split(' ')[2:].endswith("```", 0, 3):
        code = ' '.join(message_text.split(' ')[2:])[3:-3]
    else:
        code = ' '.join(message_text.split(' ')[2:])

    try:
        response = rextester.execute(language=language, code=code, stdin=stdin)
    except RextesterException:
        bot.send_message(chat_id=main_chat, text='Error at Rextester or unknown language!')
        return

    extra = ''
    if response['Warnings']:
        extra = extra + '\r\nWarnings: \r\n' + response['Warnings']
    if response['Errors']:
        extra = extra + '\r\nErrors: \r\n' + response['Errors']

    stats = ''
    if response['Stats']:
        stats = '\r\nStats: \r\n' + response['Stats'] + '.'

    output = ' No output. '
    if response['Result']:
        output = response['Result']

    if len(extra) < 4070:  # Prevent message_too_long
        bot.send_message(chat_id=main_chat, text='Output: ' + output[:(4080 - len(extra) - len(stats))] + extra + stats)
    else:
        bot.send_message(chat_id=main_chat, text='Too many long errors/warnings to show output. Sorry!')


# Main daily birthday check function
def check(bot, job):
    print('Conducting daily routine check...')
    class_list = db.get_class_list()
    birthday_users = []
    current_month = int(datetime.datetime.now().strftime('%m'))
    current_date = int(datetime.datetime.now().strftime('%d'))

    for i in class_list:
        if i["Birthmonth"] == current_month and i["Birthdate"] == current_date:
            birthday_users.append(str(i["Name"]))

    if len(birthday_users) != 0:
        for user in birthday_users:
            wishes = ['Happy birthday to {}! Have a blessed year ahead!'.format(user),
                      'A blessed birthday to {}! Wishing you a memorable year ahead!'.format(user),
                      'Another adventure-filled year awaits you. Wishing you a joyful birthday, {}!'.format(user),
                      'Count not the years, but the life you live. Wishing you a wonderful birthday, {}!'.format(user),
                      'May you have a lovely birthday today, {}! Wishing you endless joy and tons of precious memories!'.format(user)]
   
            bot.send_message(chat_id=main_chat,
                             text=secrets.choice(wishes))
    else:
        pass


@restricted
@main_group
def track(bot, update, job_queue):
    bot.send_message(chat_id=main_chat,
                     text='Birthday tracking has been started!')
    check(bot, None)
    job_queue.run_daily(callback=check,
                        time=datetime.time(0, 0, 1, 0),
                        context=main_chat)


@main_group
def feelgood(bot, update):
    bot.send_message(chat_id=main_chat,
                     text='Some advice from @jamestiotio:\r\n\r\n'
                          '1. Get up at the same time every day.\r\n'
                          '2. Eat a protein-rich breakfast every day.\r\n'
                          '3. When feeling anxious, eat a bit of food.\r\n'
                          '4. Be honest with yourself and be willing to negotiate, don\'t paralyze yourself by trying to do too much at once.\r\n'
                          '5. Try to get professional help. If you feel bad all of the time, that\'s not normal but it is fixable.\r\n'
                          'https://en.wikipedia.org/wiki/List_of_suicide_crisis_lines \r\n'
                          'Note: Some of the suicide lines are text only, so if you have anxiety about talking to someone (which is understandable!), try to use one of those.\r\n'
                          '6. Confide in someone you trust. If everyone you know drags you down, cut \'em out and focus on being a stronger person and acquiring friends who help you celebrate.\r\n'
                          '7. If you are willing to share, post your success story here in 6 months when you\'re on top of the world.\r\n\r\n'
                          'If you\'re in dire need, message @jamestiotio, however no one here is a professional so we cannot take responsibility for you. Do share your problems with your family and close friends. Also, do try to visit the counsellor if you feel comfortable with that!')


# Credit to @treetrnk for the dice-rolling functions
@main_group
def rf(bot, update, args):
    if len(args) > 0:
        args[0] = '4df+' + str(args[0])
    else:
        args = ['4df']
        
    roll(bot, update, args)


# Credit to @treetrnk for the dice-rolling functions
@main_group
def roll(bot, update, args):
    username = update.message.from_user.username if update.message.from_user.username else update.message.from_user.first_name
    equation = args[0].strip() if len(args) > 0 else False
    equation_list = re.findall(r'(\w+!?>?\d*)([+*/()-]?)', equation)
    comment = ' ' + ' '.join(args[1:]) if len(args) > 1 else ''
    space = ''
    dice_num = None
    is_fate = False
    use_ladder = False
    result = {
        'visual': [],
        'equation': [],
        'total': ''
    }

    try:
        for pair in equation_list:
            # print(f"pair: {pair}")
            for item in pair:
                if item and len(item) > 1 and 'd' in item:
                    dice = re.search(r'(\d*)d([0-9fF]+)(!)?', item)
                    try:
                        dice_num = int(dice.group(1)) if dice.group(1) else 1
                        sides = dice.group(2)
                        try:
                            if int(dice.group(1)) <= 0:
                                raise Exception('Invalid number of dice!')
                        except AttributeError:
                            raise Exception('Invalid number of dice!')
                        if (sides not in ['f','F'] and int(sides) > 1000) or (dice_num > 1000):
                            raise Exception('Maximum number of dice sides and rollable dice are 1000.')
                        space = ' '
                        result['visual'].append(space + '(')
                        result['equation'].append('(')
                        fate_dice = ''
                        current_die_results = ''
                        plus = ''
                        explode = True if dice.group(3) == '!' and int(dice.group(2)) > 1 else False

                        while dice_num > 0:
                            if sides in ['f','F']:
                                is_fate = True
                                use_ladder = True
                                current_fate_die = secrets.choice(list(fate_options.keys()))
                                current_die_results += plus + str(current_fate_die)
                                fate_dice += fate_options[current_fate_die] + ' '
                            else:
                                sides = int(sides)
                                last_roll = secrets.SystemRandom().randint(1,int(dice.group(2)))
                                current_die_results += plus + str(last_roll)
                            if not (explode and last_roll == sides):
                                dice_num -= 1
                            if len(plus) is 0: # Adds all results to result unless it is the first one
                                plus = ' + '
                        if is_fate:
                            is_fate = False
                            result['visual'].append(' ' + fate_dice)
                        else:
                            result['visual'].append(current_die_results)
                        result['equation'].append(current_die_results)
                        result['visual'].append(')')
                        result['equation'].append(')')
                    except AttributeError:
                        raise Exception('Invalid number of dice sides!')
                    
                else:
                    if item and (item in ['+','-','/','*',')','('] or int(item)):
                        result['visual'].append(' ')
                        result['visual'].append(item)
                        result['equation'].append(item)

        result['total'] = str(''.join(result['equation'])).replace(" ","")
        if bool(re.match('^[0-9+*/ ()-]+$', result['total'])):
            result['total'] = eval(result['total'])
        else:
            raise Exception('Request was not a valid equation!')

        print(' '.join(args) + ' = ' + ''.join(result['equation']) + ' = ' + str(result['total']))

        if use_ladder:
            # Set if final result is positive or negative
            sign = '+' if result['total'] > -1 else ''
            ladder_result = get_ladder(result['total'])
            result['total'] = sign + str(result['total']) + ' ' + ladder_result

        # Only show part of visual equation if bigger than 300 characters
        result['visual'] = ''.join(result['visual'])
        if len(result['visual']) > 275:
            result['visual'] = result['visual'][0:275] + ' . . . )'

        response = (f'@{username} rolled<b>{comment}</b>:\r\n{result["visual"]} =\r\n<b>{str(result["total"])}</b>')
        error = ''

    except Exception as e:
        response = f'@{username}: <b>Invalid equation!</b>\r\n'
        try:
            if (int(sides) > 1000) or (dice_num and dice_num > 1000):
                response += str(e) + '\r\n'
        except UnboundLocalError:
            pass
        response += ('Please use <a href="https://en.wikipedia.org/wiki/Dice_notation">dice notation</a>.\r\n' +
                     'For example: <code>3d6</code>, or <code>1d20+5</code>, or <code>d12</code>.\r\n\r\n'
                     )
        print(e)
        print(response)
        error = traceback.format_exc().replace('\r', '').replace('\n', '; ')

        #logfile.write('\r\n\r\n' + str(datetime.now()) + '======================================\r\n')
        #logfile.write('\tRESPONSE: ' + response.replace('\r', ' ').replace('\n', '') + '\r\n')
        #if len(error):
        #    logfile.write('\tERROR: ' + error + '\r\n')

    bot.send_message(chat_id=main_chat, text=response, parse_mode=ParseMode.HTML)


@main_group
def remindme(bot, update, args):
    username = update.message.from_user.username if update.message.from_user.username else update.message.from_user.first_name
    message = update.effective_message.text

    if (message.find(" to ") != -1) and (message.find(" that ") > message.find(" to ") or message.find(" that ") == -1):
        message = update.effective_message.text.replace(" to ", " that ", 1)
    
    str_args = message.split(" that ", 2)

    if len(str_args) != 2:
        bot.send_message(chat_id=main_chat,
                         text='Something went wrong while processing your reminder! Please try again!'
                              'Do follow the format: /remindme <time> <"that"/"to"> <reminder-text>.')

    reminder_time = ""
    reminder_message = ""
    
    # Add code here to connect to reminder database and time check
    
    bot.send_message(chat_id=main_chat,
                     parse_mode=ParseMode.MARKDOWN,
                     text='*New reminder added!* \r\n'
                          '*Reminded at:* {} *by* @{} \r\n'
                          '*Reminder:* {}'.format(reminder_time, username, reminder_message))


@main_group
def vote(bot, update):
    bot.send_message(chat_id=main_chat,
                     text='This command is still under development. Apologies for the inconvenience!')


# Disable the homepage route to prevent the bot from being shut down
"""
@app.route("/")
def home():
    return 'Nothing to see here, move along folks.'
"""


@app.route("/{}".format(BOT_TOKEN), methods=['GET', 'POST'])
def main():
    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Simple start function
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('stop', stop))
    dp.add_handler(CommandHandler('summon', summon))
    dp.add_handler(CommandHandler('help', start))
    dp.add_handler(CommandHandler('run', run))
    dp.add_handler(CommandHandler('track', track, pass_job_queue=True))
    dp.add_handler(CommandHandler('feelgood', feelgood))
    dp.add_handler(CommandHandler(['roll', 'r'], roll, pass_args=True))
    dp.add_handler(CommandHandler('rf', rf, pass_args=True))
    dp.add_handler(CommandHandler('remindme', remindme, pass_args=True))
    dp.add_handler(CommandHandler('vote', vote))

    # Log all errors
    dp.add_error_handler(error)
    
    updater.start_polling(timeout=0)
    
    # Webhook is not working yet, I will figure out a way to implement it later
    # updater.start_webhook(listen='0.0.0.0', port=PORT, url_path=BOT_TOKEN, cert='cert.pem', key='key.pem')
    # updater.bot.set_webhook(WEBHOOK_URL + "/" + BOT_TOKEN)
    
    return 'OK'


# For localhost testing, include this
"""
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
"""