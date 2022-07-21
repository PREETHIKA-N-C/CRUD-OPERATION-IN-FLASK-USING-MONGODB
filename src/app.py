from pathlib import Path

import pymongo
from flask import Flask, Blueprint, jsonify
from flask_cors import CORS
import logging
from src import app_config
from src.API_Routes.endpoints import api_routes

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s:%(levelname)s%:%(message)')
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)


def create_app():
    web_app = Flask(__name__, root_path=Path(__file__).parent)
    # web_app.config.from_object(app_config)   # Load Flask Configuration ()
    CORS(web_app)
    api_blueprint = Blueprint('api_blueprint', __name__)
    api_blueprint = api_routes(api_blueprint)
    web_app.register_blueprint(api_blueprint, url_prefix='/api')

    return web_app


app = create_app()

connection_str = "mongodb+srv://Preethika:Ha11yPo11er@cluster0.6vxyakq.mongodb.net/?retryWrites=true&w=majority"

client = pymongo.MongoClient(connection_str)

db = client.get_database('StrangerThingsDB')

character_collection = pymongo.collection.Collection(db, 'CharacterDetails')


@app.route('/read')
def read():
    characters = character_collection.find()
    output = [{'Character Name': character['Character Name'], 'Gender': character['Gender'],
               'Personality Type': character['Personality Type'], 'Real Name': character['Real Name'],
               'Born': character['Born'], 'Age': character['Age'],
               'Status': character['Status']} for character in characters]
    return jsonify(output)


@app.route('/read-with-filter')
def read_with_filter():
    filt = {'Personality Type': 'INFJ'}
    characters = character_collection.find(filt)
    output = [{'Character Name': character['Character Name'], 'Gender': character['Gender'],
               'Personality Type': character['Personality Type'], 'Real Name': character['Real Name'],
               'Born': character['Born'], 'Age': character['Age'],
               'Status': character['Status']} for character in characters]
    return jsonify(output)


@app.route('/create')
def create():
    new_character = {'Character Name': 'Nancy Wheeler', 'Gender': 'Female',
                     'Personality Type': 'ESTJ', 'Real Name': 'Natalia Dyer', 'Born': '1967', 'Age': '19',
                     'Status': 'Alive'}
    character_collection.insert_one(new_character)
    result = {'Result': 'Character Created Successfully!!'}
    return result


@app.route('/create-many')
def create_many():
    new_character1 = {'Character Name': 'Nancy Wheeler', 'Gender': 'Female',
                      'Personality Type': 'ESTJ', 'Real Name': 'Natalia Dyer', 'Born': '1967', 'Age': '18',
                      'Status': 'Alive'}
    new_character2 = {'Character Name': 'Nancy Wheeler', 'Gender': 'Female',
                      'Personality Type': 'ESTJ', 'Real Name': 'Natalia Dyer', 'Born': '1967', 'Age': '18',
                      'Status': 'Alive'}
    new_character3 = {'Character Name': 'Erica Sinclair', 'Gender': 'Female',
                      'Personality Type': 'ENTJ', 'Real Name': 'Priah Ferguson', 'Born': '1975', 'Age': '11',
                      'Status': 'Alive'}
    new_character4 = {'Character Name': 'Eleven', 'Gender': 'Female',
                      'Personality Type': 'ISFP', 'Real Name': ' Millie Bobby Brown', 'Born': '1971', 'Age': '14',
                      'Status': 'Alive'}
    new_character5 = {'Character Name': 'Micheal Wheeler', 'Gender': 'Male',
                      'Personality Type': 'ENFJ', 'Real Name': 'Finn Wolfhard', 'Born': '1971', 'Age': '14',
                      'Status': 'Alive'}
    new_character6 = {'Character Name': 'William Byers', 'Gender': 'Male',
                      'Personality Type': 'INFP', 'Real Name': 'Noah Schnapp', 'Born': '1971', 'Age': '14',
                      'Status': 'Alive'}
    new_character7 = {'Character Name': 'Dustin Henderson', 'Gender': 'Male',
                      'Personality Type': 'ENTP', 'Real Name': 'Gaten Matarazzo', 'Born': '1971', 'Age': '14',
                      'Status': 'Alive'}

    new_characters = [new_character1, new_character2, new_character3, new_character4,
                      new_character5, new_character6, new_character7]
    character_collection.insert_many(new_characters)
    result = {'Result': 'Characters Created Successfully!!'}
    return result


@app.route('/update')
def update():
    updated_character = {"$set": {'Age': '15'}}
    filt = {'Character Name': 'Suzie Bingham'}
    character_collection.update_one(filt, updated_character)
    result = {'Result': 'Character Updated Successfully!!'}
    return result


@app.route('/update-many')
def update_many():
    updated_character = {"$set": {'Age': '18'}}
    filt = {'Character Name': 'Nancy Wheeler'}
    character_collection.update_many(filt, updated_character)
    result = {'Result': 'Characters Updated Successfully!!'}
    return result


@app.route('/delete')
def delete():
    filt = {'Character Name': 'Erica Sinclair'}
    character_collection.delete_one(filt)
    result = {'Result': 'Character Deleted Successfully!!'}
    return result


@app.route('/delete-many')
def delete_many():
    filt = {'Character Name': 'Nancy Wheeler'}
    character_collection.delete_many(filt)
    result = {'Result': 'Characters Deleted Successfully!!'}
    return result


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
