from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from datetime import datetime

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)
db.init_app(app)

# ------------------ Routes ------------------

# GET /messages
@app.route('/messages', methods=['GET'])
def messages():
    messages = Message.query.order_by(Message.created_at.asc()).all()
    return make_response(jsonify([
        {
            "id": msg.id,
            "body": msg.body,
            "username": msg.username,
            "created_at": msg.created_at.isoformat(),
            "updated_at": msg.updated_at.isoformat()
        }
        for msg in messages
    ]), 200)

# POST /messages
@app.route('/messages', methods=['POST'])
def create_message():
    data = request.get_json()

    new_message = Message(
        body=data['body'],
        username=data['username'],
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    db.session.add(new_message)
    db.session.commit()

    return make_response(jsonify({
        "id": new_message.id,
        "body": new_message.body,
        "username": new_message.username,
        "created_at": new_message.created_at.isoformat(),
        "updated_at": new_message.updated_at.isoformat()
    }), 201)

# PATCH /messages/<id>
@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    message = Message.query.get_or_404(id)
    data = request.get_json()

    message.body = data.get('body', message.body)
    message.updated_at = datetime.utcnow()

    db.session.commit()

    return make_response(jsonify({
        "id": message.id,
        "body": message.body,
        "username": message.username,
        "created_at": message.created_at.isoformat(),
        "updated_at": message.updated_at.isoformat()
    }), 200)

# DELETE /messages/<id>
@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    message = Message.query.get_or_404(id)

    db.session.delete(message)
    db.session.commit()

    return make_response('', 204)

# --------------------------------------------

if __name__ == '__main__':
    app.run(port=5555)

