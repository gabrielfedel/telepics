import configparser

from telegram.ext import Updater, CommandHandler
from epics import caget


class BotEPICS():
    def __init__(self):
        pass

    def cmd_caget (self, bot, update):
        pv_name = update["message"]["text"].split(" ")[1]
        value = caget(pv_name)
        update.message.reply_text(
            'PV {} Value {}'.format(pv_name, value))

    def hello(self, bot, update):
        update.message.reply_text(
            'Hello {}'.format(update.message.from_user.first_name))


if __name__ == '__main__':
    # load configs
    config = configparser.ConfigParser()
    config.read('config.ini')
    key = config['DEFAULT']['KEY']

    updater = Updater(key)

    bot = BotEPICS()

    updater.dispatcher.add_handler(CommandHandler('hello', bot.hello))
    updater.dispatcher.add_handler(CommandHandler('caget', bot.cmd_caget))

    updater.start_polling()
    updater.idle()
