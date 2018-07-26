from flask import Flask, request
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

try:
    from boto.s3.connection import S3Connection
    import os
    mongo_uri = S3Connection(os.environ['MONGODB_URI'])
except:
    from secrets import mongo_uri

application = Flask(__name__)

english_chatbot = ChatBot('Chatterbot',
                         storage_adapter = "chatterbot.storage.MongoDatabaseAdapter",
                         database = "heroku_zr537699",
                         database_uri = mongo_uri)
english_chatbot.set_trainer(ChatterBotCorpusTrainer)
english_chatbot.train("chatterbot.corpus.english")

@application.route("/")
def hello():
    return "<h1 style='color:blue'>Hello There!</h1>"

@application.route("/chat")
def chat():
    input = request.args.get('input')
    response = english_chatbot.get_response(input)
    return response.text

if __name__ == "__main__":
    application.run()