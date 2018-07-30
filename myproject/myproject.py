from flask import Flask, request, send_from_directory
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

try:
    import os
    mongo_uri = os.environ['MONGODB_URI']
except:
    from secrets import mongo_uri

application = Flask(__name__, static_folder="static")

english_chatbot = ChatBot('Chatterbot',
                         storage_adapter = "chatterbot.storage.MongoDatabaseAdapter",
                         database = "heroku_zr537699",
                         database_uri = mongo_uri)
#english_chatbot.set_trainer(ChatterBotCorpusTrainer)
#train = english_chatbot.train
#train("chatterbot.corpus.english")

@application.route('/', defaults={'path': 'index.html'})
@application.route("/<path:path>")
def static_files(path):
    return send_from_directory('static',path)

@application.route("/chat")
def chat():
    input = request.args.get('input')
    response = english_chatbot.get_response(input)
    return response.text

if __name__ == "__main__":
    application.run()