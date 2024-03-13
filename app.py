import os
from extension import app, pg_host
from flask import jsonify, make_response, session, request
from dotenv import load_dotenv
load_dotenv()
from db_reqs import *
import smtplib
create_tables()
from json import loads


@app.route('/api/auth/entrance', methods=['POST'])
def auth_login():
    resp = dict(request.form)
    username = resp['username']
    password = resp['password']
    token = check_entrance(username, password)
    if token:
        return make_response({'token': token}, 200)
    else:
        return make_response({'reason': 'Неверный логин или пароль'}, 401)


@app.route('/api/auth/register', methods=['POST'])
def auth_register():
    resp = dict(request.form)
    username = resp['username']
    password = resp['password']
    region = resp['region']
    mail = resp['email']
    avatar = resp['avatar']
    token = add_user(username, password, region, mail, avatar)
    if token:
        return make_response({'token': token}, 200)
    else:
        return make_response({'reason': 'Пользователь с таким username уже существует'}, 409)


@app.route('/api/auth/generateConfirmationCode', methods=['POST'])
def confirm_email():
    resp = dict(request.form)
    token = resp['token']
    decoded_token = check_token(token)
    if decoded_token:
        generate_confirmation_code(decoded_token)
        return 200
    else:
        return make_response({'reason': 'Недействительный токен'}, 403)


@app.route('/api/auth/sendConfirmationCode', methods=['POST'])
def send_confirmation_code():
    resp = dict(request.form)
    token = resp['token']
    decoded_token = check_token(token)
    if decoded_token:
        send_confirm_email(decoded_token)
        return make_response({'status': 'Success 200'}, 200)
    else:
        return make_response({'reason': 'Недействительный токен'}, 403)


@app.route('/api/auth/checkConfirmationCode', methods=['POST'])
def check_confirm_code():
    resp = dict(request.form)
    token = resp['token']
    confirm_code = resp['confirmationCode']
    decoded_token = check_token(token)
    if decoded_token:
        if check_confirmation_code(decoded_token, confirm_code):
            return 200
        else:
            return make_response({'reason': 'Неверный код либо срок действия кода истек'}, 400)
    else:
        return make_response({'reason': 'Недействительный токен'}, 403)


@app.route('/api/media/add', methods=['POST'])
def add_media():
    resp = dict(request.form)
    token = resp['token']
    decoded_token = check_token(token)
    if decoded_token:
        file = resp['file']
        title = resp['title']
        tags = loads(resp['tags'])
        metadata = loads(resp['metadata'])
        coords = resp['coordinates']
        username_id = decoded_token['id']
        if 'gallery_id' in resp:
            gallery_id = resp['gallery_id']
            if check_access_gallery(username_id, gallery_id):
                add_media_to_gallery(file, tags, metadata, coords, title, username_id, gallery_id)
            else:
                return make_response({'reason': "У пользователя нет доступа к данной галерее"}, 403)
        else:
            album_id = resp['album_id']
            if check_access_album(username_id, album_id):
                add_media_to_album(file, tags, metadata, coords, title, username_id, album_id)
            else:
                return make_response({'reason': "У пользователя нет доступа к данному альбому"}, 403)
        return make_response({'status': 'Success 200'}, 200)
    else:
        return make_response({'reason': 'Недействительный токен'}, 403)


@app.route('/api/media/createAlbum', methods=['POST'])
def create_album():
    resp = dict(request.form)
    token = resp['token']
    decoded_token = check_token(token)
    if decoded_token:
        username_id = resp['username_id']
        title = resp['title']
        isPublic = resp['isPublic']
        if isPublic == 'true':
            isPublic = True
        else:
            isPublic = False
        add_album_to_db(username_id, title, isPublic)
        return make_response({'status': 'Success 200'}, 201)
    else:
        return make_response({'reason': 'Недействительный токен'}, 403)


@app.route('/api/media/addUserToAlbum', methods=['POST'])
def add_user_to_album():
    resp = dict(request.form)
    token = resp['token']
    decoded_token = check_token(token)
    if decoded_token:
        author = decoded_token['id']
        album_id = resp['album_id']
        user_id = resp['user_id']
        if add_user_to_album_db(author, album_id, user_id):
            return make_response({'status': 'Success 200'}, 200)
        else:
            return make_response({'reason': 'У вас нет доступа к этому альбому'}, 403)
    else:
        return make_response({'reason': 'Недействительный токен'}, 403)


if __name__ == '__main__':
    app.run(host=os.getenv('SERVER_HOST'), port=os.getenv('SERVER_PORT'))
