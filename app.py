# from chatbot import create_app
# app = create_app()


from flask import Flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SECRET_KEY'] = 'yoursecretkey'
# app.register_error_handler(404, handle_404)
from models_database import db 
db.init_app(app)

import auth, chat
app.register_blueprint(auth.bp)
app.register_blueprint(chat.bp)
auth.login_manager.init_app(app)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=4651, debug=True)