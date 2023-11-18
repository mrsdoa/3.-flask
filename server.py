from sqlite3 import IntegrityError

import flask
from flask import jsonify
from flask.views import MethodView
from flask import request, Response
from pydantic import ValidationError
from schema import CreateAdvertisement

from models import Advertisement, Session
import psycopg2
#объект класса
app = flask.Flask('app')

#создаём свой класс ошибок
class HttpError(Exception):
    def __init__(self, status_code: int, description: str):
        self.status_code = status_code
        self.description = description

#функция обработки ошибок, которая принимает экземпляр класса ошибки
@app.errorhandler(HttpError)
def error_handler(error):
    response = jsonify({'error': error.description})
    response.status_code = error.status_code
    return response

def validate(model, data):
    try:
        return model.model_validate(data).model_dump(exclude_unset=True)
    except ValidationError as err:
        error = err.errors()[0]
        error.pop('ctx', None)
        raise HttpError(status_code=400, error)

@app.before_request
def before_request():
    session = Session()
    request.session = session

#для закрытия сессии
@app.after_request
def after_request(response: Response):
    request.session.close()
    return response

#функция для избавления от копипаста ошибки
def get_advertisement(advertisement_id:int, session):
    advertisement = session.get(Advertisement, advertisement_id)
    if advertisement is None:
        raise HttpError(status_code=404, description='user not found')
    return advertisement

def add_advertisement(advertisement: Advertisement):
    try:
        request.session.add(advertisement)
        request.session.commit()
    except IntegrityError:
        raise HttpError(status_code=409, description='advertisement already exists')
    return advertisement

class AdvertisementView(MethodView):

    @property
    def session(self) -> Session:
        return request.session

    def get(self, advertisement_id: int):
        advertisement = get_advertisement(advertisement_id)
        return jsonify({'id': advertisement.id, 'titile': advertisement.title, 'description': advertisement.description, 'owner': advertisement.owner, 'registration_time': advertisement.created_time.isoformat()})

    def post(self):
        user_request = validate(CreateAdvertisement, request.json)
        if 'title' not in user_request and 'description' not in user_request:
            raise HttpError(status_code=400, description='title and description is required')
        new_advertisement = Advertisement(**user_request)
        new_advertisement = add_advertisement(new_advertisement)
        return jsonify({'id': new_advertisement.id})

    def patch(self, advertisement_id: int):
        user_request = request.json
        advertisement = get_advertisement(advertisement_id)
        for key, value in user_request.items():
            setattr(advertisement, key, value)
        advertisement = add_advertisement(advertisement)
        # self.session.commit()
        return jsonify({'id': advertisement.id, 'titile': advertisement.title, 'description': advertisement.description, 'owner': advertisement.owner, 'registration_time': advertisement.created_time.isoformat()})
    def delete(self, advertisement_id: int):
        advertisement = get_advertisement(advertisement_id)
        self.session.delete(advertisement)
        self.session.commit()
        return jsonify({'status': 'ok'})

advertisement_view = AdvertisementView.as_view('advertisement_view')

app.add_url_rule('/advertisement/<int:advertisement_id', view_func=advertisement_view, methods=['GET', 'PATCH', 'DELETE'])
app.add_url_rule('/advertisement', view_func=advertisement_view, methods=['POST'])

if __name__ == '__main__':
    app.run(debug=True)
