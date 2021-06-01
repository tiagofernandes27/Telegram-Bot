import re
from flask import Flask, request
import telegram
from telebot.credentials import bot_token, bot_user_name, URL

global bot
global TOKEN

TOKEN = bot_token
bot = telegram.Bot(token=TOKEN)
app = Flask(__name__)


@app.route('/{}'.format(TOKEN), methods=['POST'])
def respond():
    # retrieve the message in JSON and then transform it to Telegram object
    update = telegram.Update.de_json(request.get_json(force=True), bot)

    data = request.get_json()
    print(data)

    chat_id = data['message']['chat']['id']
    msg_id = data['message']['message_id']

    text = data['message']['text'] if 'text' in data['message'] else ''

    # the first time you chat with the bot AKA the welcoming message
    if text == "/start@cagado_de_fome_bot":
        # print the welcoming message
        bot_welcome = """
       Hello there!
       """
        # send the welcoming message
        bot.sendMessage(chat_id=chat_id, text=bot_welcome,
                        reply_to_message_id=msg_id)
    else:
        try:
            variations = [
                "dia",
                "bao",
                "bão"
            ]
            if (text.lower().__contains__("dia") and text.lower().__contains__("bom")) or text.lower() in variations:
                bot.send_photo(chat_id=chat_id, photo="https://imageproxy.ifunny.co/crop:x-20,resize:640x,quality:90x75/images/100f67b3b98cfc6c64bcefc82ce3424eeeeca1765397a63996e17d66701baad5_1.jpg",
                                reply_to_message_id=msg_id)
            if text == "/allcommands@cagado_de_fome_bot":
                allcommands = "Aqui tens todos os comandos que pode utilizar\n\n/gitcomment\n/wiki\n/make\n/projects\n/gitbranches"
                bot.sendMessage(chat_id=chat_id, text=allcommands,
                                reply_to_message_id=msg_id)
            elif text == "/gitcomment@cagado_de_fome_bot":
                comment = "* feat(shopping cart): add the amazing button\n* fix: add missing parameter to service call\n\n  The error occurred because of <reasons>.\n\n* build: release version 1.0.0\n* build: update dependencies\n* refactor: implement calculation method as recursion\n* style: remove empty line\n* revert: refactor: implement calculation method as recursion\n\n  This reverts commit 221d3ec6ffeead67cee8c730c4a15cf8dc84897a."
                bot.sendMessage(chat_id=chat_id, text=comment,
                                reply_to_message_id=msg_id)
            elif text == "/wiki@cagado_de_fome_bot":
                bot.sendMessage(
                    chat_id=chat_id, text="https://caosdata.visualstudio.com/magiccupom-app/_wiki/wikis/magiccupom-app.wiki/2/Welcome-to-Magic-Cupom-APP")
            elif text == "/make@cagado_de_fome_bot":
                make = "'make setup' - creates all the environment for the project, usually this command is inside API module\n'make destroy' - destroy the environment for the project, usually this command is inside API module\n'make up' - turn on cluster, this command is usually available inside API module\n'make down' - turn off cluster, this command is usually available inside API module\n'make debug' - you can debug your module inside the cluster\n'make cleanup' - clean your module if something is wrong\n'make add_dep' - add dependencies into the project without the need of overwrite requirements file\n'make rm_dep' - remove dependencies into the project without the need of overwrite requirements file\n'make logs' - shows the server activity within 10 minutes\n'make minikube_set_memory [memory]' - changes the amount of memory of your cluster"
                bot.sendMessage(chat_id=chat_id, text=make,
                                reply_to_message_id=msg_id)
            elif text == "/projects@cagado_de_fome_bot":
                projects = "'gaia' - G.AI.A\n<https://caosdata.visualstudio.com/gaia-app>\n'gaiabmg' - Gaia For BMG\n<https://caosdata.visualstudio.com/gaiabmg-app>\n'magiccupom' - Magic Cupom\n<https://caosdata.visualstudio.com/magiccupom-app>\n'scutaai' - Scuta.AI\n<https://caosdata.visualstudio.com/scutaai-app>"
                bot.sendMessage(chat_id=chat_id, text=projects,
                                reply_to_message_id=msg_id)
            elif text == "/gitbranches@cagado_de_fome_bot":
                gitbranches = "You have to always create your branch from 'DEVELOP' branch\n\nIn https://sprints.zoho.com/ you can see your tasks\nThe name of your branch is the Card ID inside zoho\n\nOBS: Your branch have to follow some guidelines\n\n* If the card type is an issue or bug your branch has to be named as: issue/<card_id>\n* If the card type is a task or story your branch has to be named as: feature/<card_id>\n    * remember that if your branch is a story, you can name it as the parent card id\n      and make all the child tasks inside this branch"
                bot.sendMessage(chat_id=chat_id, text=gitbranches,
                                reply_to_message_id=msg_id)
            else:
                pass

        except Exception:
            # if things went wrong
            bot.sendMessage(
                chat_id=chat_id, text="There was a problem in the name you used, please enter different name", reply_to_message_id=msg_id)
    return 'ok'


@app.route('/set_webhook', methods=['GET', 'POST'])
def set_webhook():
    s = bot.setWebhook('{URL}{HOOK}'.format(URL=URL, HOOK=TOKEN), allowed_updates=["callback_query", "message"])
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"


@app.route('/')
def index():
    return '.'


if __name__ == '__main__':
    app.run(threaded=True)
