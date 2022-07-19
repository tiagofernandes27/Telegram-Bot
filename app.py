import random
import re
from flask import Flask, request, make_response
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
        bot.sendMessage(chat_id=chat_id, text=bot_welcome,reply_to_message_id=msg_id)
    else:
        try:
            if text == "/allcommands@cagado_de_fome_bot":
                allcommands = """
                    Aqui tens todos os comandos que pode utilizar\n
                    /gitcomment
                    /wiki
                    /make
                    /projects
                    /gitbranches
                    /application_security
                """
                bot.sendMessage(chat_id=chat_id, text=re.sub(' {2,}', '', allcommands), reply_to_message_id=msg_id)
            elif text == "/gitcomment@cagado_de_fome_bot":
                comment = """
                    * feat: add the amazing button
                    * fix: add missing parameter to service call
                      The error occurred because of <reasons>.
                    * build: release version 1.0.0
                    * build: update dependencies
                    * refactor: implement calculation method as recursion
                    * style: remove empty line
                    * revert: refactor: implement calculation method as recursion
                      This reverts commit 221d3ec6ffeead67cee8c730c4a15cf8dc84897a.
                    
                    All These examples can be found at: https://gist.github.com/qoomon/5dfcdf8eec66a051ecd85625518cfd13
                """
                bot.sendMessage(chat_id=chat_id, text=re.sub(' {2,}', '', comment), reply_to_message_id=msg_id)
            elif text == "/wiki@cagado_de_fome_bot":
                bot.sendMessage(chat_id=chat_id, text="https://caosdata.visualstudio.com/magiccupom-app/_wiki/wikis/magiccupom-app.wiki/2/Welcome-to-Magic-Cupom-APP")
            elif text == "/make@cagado_de_fome_bot":
                make = """
                    'make setup' - creates all the environment for the project, usually this command is inside API module
                    'make destroy' - destroy the environment for the project, usually this command is inside API module
                    'make up' - turn on cluster, this command is usually available inside API module
                    'make down' - turn off cluster, this command is usually available inside API module
                    'make debug' - you can debug your module inside the cluster
                    'make cleanup' - clean your module if something is wrong
                    'make add_dep' - add dependencies into the project without the need of overwrite requirements file
                    'make rm_dep' - remove dependencies into the project without the need of overwrite requirements file
                    'make logs' - shows the server activity within 10 minutes
                    'make minikube_set_memory [memory]' - changes the amount of memory of your cluster
                """
                bot.sendMessage(chat_id=chat_id, text=re.sub(' {2,}', '', make), reply_to_message_id=msg_id)
            elif text == "/projects@cagado_de_fome_bot":
                projects = "'gaia' - G.AI.A\n<https://caosdata.visualstudio.com/gaia-app>\n'gaiabmg' - Gaia For BMG\n<https://caosdata.visualstudio.com/gaiabmg-app>\n'magiccupom' - Magic Cupom\n<https://caosdata.visualstudio.com/magiccupom-app>\n'scutaai' - Scuta.AI\n<https://caosdata.visualstudio.com/scutaai-app>\n'countdown-cocacola' - Countdown to Holidays\n<https://caosdata.visualstudio.com/cokenft-app>'"
                bot.sendMessage(chat_id=chat_id, text=projects,
                                reply_to_message_id=msg_id)
            elif text == "/gitbranches@cagado_de_fome_bot":
                gitbranches = """
                    You have to always create your branch from 'DEVELOP' branch\n
                    In https://sprints.zoho.com/ you can see your tasks
                    The name of your branch is the Card ID inside zoho\n
                    OBS: Your branch has to follow some guidelines\n
                    * If the card type is an issue or bug your branch has to be named as: issue/<card_id>
                    * If the card type is a task or story your branch has to be named as: feature/<card_id>
                """
                bot.sendMessage(chat_id=chat_id, text=re.sub(' {2,}', '', gitbranches), reply_to_message_id=msg_id)
            elif text == "/application_security@cagado_de_fome_bot":
                security = """
                    We have this security manual to search for best pratices within application.
                    https://github.com/OWASP/wstg/tree/master/document
                """
                bot.sendMessage(chat_id=chat_id, text=security, reply_to_message_id=msg_id)
            else:
                pass

        except Exception:
            # if things went wrong
            bot.sendMessage(chat_id=chat_id, text="There was a problem in the name you used, please enter different name", reply_to_message_id=msg_id)
    return 'ok'

@app.route('/set_webhook', methods=['GET', 'POST'])
def set_webhook():
    s = bot.setWebhook('{URL}{HOOK}'.format(URL=URL, HOOK=TOKEN), allowed_updates=["callback_query", "message"])
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"

@app.route('/innovation/hooks/github', methods=['POST', 'GET'])
def innovation_hooks():
    data = request.get_json()

    message = ""
    if 'ref' in data:
        message = f"{data['pusher']['name']} pushed into {data['repository']['name']}\n\nDIFF URL: {data['compare']}"
    
    if 'action' in data and 'issue' in data and 'comment' in data:
        message = f"{data['sender']['login']} {data['action']} a comment in {data['repository']['full_name']}.\n\nIssue URL: {data['issue']['url']}\n\nComment URL: {data['comment']['url']}"
    
    if 'action' in data and 'issue' in data and 'comment' not in data:
        message = f"{data['sender']['login']} {data['action']} an issue in {data['repository']['full_name']}.\n\nIssue Name: {data['issue']['title']}\nIssue URL: {data['issue']['url']}"
    
    if 'pull_request' in data and 'review' not in data and 'thread' not in data and 'comment' not in data:
        message = f"{data['sender']['login']} {data['action']} a pull request in {data['repository']['full_name']}.\n\nPull Request URL: {data['pull_request']['url']}"

    if 'pull_request' in data and 'review' in data:
        message = f"{data['sender']['login']} {data['action']} a review in the pull request in {data['repository']['full_name']}.\n\nPull Request URL: {data['pull_request']['url']}"

    if 'pull_request' in data and 'comment' in data:
        message = f"{data['sender']['login']} {data['action']} commented in the pull request in {data['repository']['full_name']}.\n\nPull Request URL: {data['pull_request']['url']}\nComment URL: {data['comment']['url']}"

    if 'pull_request' in data and 'thread' in data:
        message = f"{data['sender']['login']} {data['action']} a thread in the pull request in {data['repository']['full_name']}.\n\nPull Request URL: {data['pull_request']['url']}"

    bot.send_message(chat_id=-1001328661879, text=message)

    return make_response({}, 200)

@app.route('/')
def index():
    return '.'

if __name__ == '__main__':
    app.run(threaded=True)
