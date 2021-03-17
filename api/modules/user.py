from flask import Blueprint, Response,request
from database.models import User
from modules.controllers import user as user_logic
from mongoengine import  DoesNotExist

user = Blueprint('user', __name__)

@user.route('/api/user/<chat_id>', methods=['GET'])
def get_user(chat_id):
    try:
        user = User.objects().get(chat_id=chat_id).to_json()
    except DoesNotExist:
        return Response(None, mimetype="application/json", status=201)
    return Response(user, mimetype="application/json", status=200)

@user.route('/api/user', methods=['POST'])
def create_user():
    body = request.get_json()
    user = User(**body).save()
    id = user.id
    return {'id': str(id)}, 200

@user.route('/api/user/<chat_id>', methods=['PATCH'])
def edit_user(chat_id):
   user = User.objects().get(chat_id=chat_id)
   body = request.get_json()
   user.update(**body)
   return Response(user.to_json(), mimetype="application/json", status=200)       

@user.route('/api/user/<chat_id>', methods=['DELETE'])
def delete_user(chat_id):
    user_logic.delete_user(chat_id)
    return { "status": "ok"  }