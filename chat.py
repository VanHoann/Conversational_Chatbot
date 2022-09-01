from datetime import datetime

from flask import render_template, url_for, redirect, Blueprint, abort, request,jsonify
from flask_login import login_required, current_user

from models_database import db, Chat
from model import ConversationalChatbot

########################
# Load model
global model
model = ConversationalChatbot()


def change_mode(mode='rule-based'): # or 'ai'
    model.change_mode(mode)

def generate_answer(inp):
    output = model.generate_answer(inp.strip())
    return output

#########################

bp = Blueprint('chat', __name__)

@bp.route('/health')
def heath():
    return "Healthy"

@bp.route('/')
@login_required
def index():    
    chats = current_user.chats
    if len(chats) == 0:
        chat_getting_ML = Chat(content="Hello. Nice to meet you", user=current_user, message_from_bot=True, with_ML_model = True)
        chat_getting_rulebased = Chat(content="Hi there. How are you today?", user=current_user, message_from_bot=True, with_ML_model = False)
        db.session.add(chat_getting_ML)
        db.session.add(chat_getting_rulebased)
        db.session.commit()
    chats = current_user.chats
    return render_template('chat/index.html', chats=chats)

@bp.route('/chat', methods=('POST',))
@login_required
def create_chat():
    # text = request.form['text']
    data = eval(request.form['data'])
    text = data['content']
    if not text:
        return jsonify({"status":False,"chat_res":""})
    if data['with_ML_model'] == "true":
        ML_model = True
    else:
        ML_model = False
    chat = Chat(content=text, user=current_user, message_from_bot=False, with_ML_model=ML_model)
    db.session.add(chat)
    
    if ML_model:
        change_mode(mode='ai')
        res_content = generate_answer(text)
    else:
        change_mode(mode='rule-based')
        res_content = generate_answer(text)
    chat_res = Chat(content=res_content, user=current_user, message_from_bot=True, with_ML_model = ML_model)
    db.session.add(chat_res)

    db.session.commit()
    
    return jsonify({"status":True, "chat_res":res_content})
