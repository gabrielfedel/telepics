import configparser

from telegram.ext import Updater, CommandHandler
from epics import caget, PV


class BotEPICS():
    def __init__(self):
        self.pvs_dict = {}

    def cmd_caget (self, bot, update):
        pv_name = update["message"]["text"].split(" ")[1]
        value = caget(pv_name)
        update.message.reply_text(
            'PV {} Value {}'.format(pv_name, value))

    def hello(self, bot, update):
        update.message.reply_text(
            'Hello {}'.format(update.message.from_user.first_name))

    def cmd_camonitor(self, bot, update):
        pv_name = update["message"]["text"].split(" ")[1]
        if pv_name not in self.pvs_dict.keys():
            self.pvs_dict[pv_name] = PV(pv_name)
            self.pvs_dict[pv_name].add_callback(
                lambda *args, **kw: self.update_callback(update, *args, **kw))

    def update_callback(self, update=None, pvname=None, value=None, char_value=None, **kw):
        update.message.reply_text(
            'PV {} Value {}'.format(pvname, value))


if __name__ == '__main__':
    # load configs
    config = configparser.ConfigParser()
    config.read('config.ini')
    key = config['DEFAULT']['KEY']

    updater = Updater(key)

    bot = BotEPICS()

    updater.dispatcher.add_handler(CommandHandler('hello', bot.hello))
    updater.dispatcher.add_handler(CommandHandler('caget', bot.cmd_caget))
    updater.dispatcher.add_handler(CommandHandler('camonitor', bot.cmd_camonitor))

    updater.start_polling()
    updater.idle()
