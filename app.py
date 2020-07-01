from flask import Flask, request, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_heroku import Heroku
import io

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://surmjujkumvble:08c239b6a4ae6a91bd956875471c8061c6d39ef83a867149062b960a18a0cc53@ec2-3-216-129-140.compute-1.amazonaws.com:5432/dfnl5s8ru5887v"

db = SQLAlchemy(app)
ma = Marshmallow(app)

heroku = Heroku(app)
CORS(app)


class File(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(), nullable = False)
    file_type = db.Column(db.String(), nullable = False)
    data = db.Column(db.LargeBinary, nullable=False)

    def __init__(self, name, file_type, data):
        self.name = name
        self.file_type = file_type
        self.data = data

class FileSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'file_type')

file_schema = FileSchema()
files_schema = FileSchema(many = True)


@app.route('/file/add', methods =['POST'])
def add_file():
    name = request.form.get('name')
    file_type = request.form.get('type')
    data = request.files.get('data')

    new_file = File(name, file_type, data.read())
    db.session.add(new_file)
    db.session.commit()

    return jsonify('File added success!')

@app.route('/file/get/data', methods = ['GET'])
def get_file_data():
    file_data = db.session.query(File).all()
    return jsonify(files_schema.dump(file_data))

@app.route('/file/get/<id>', methods = ['GET'])
def get_file(id):
    file_data = db.session.query(File).filter(File.id == id).first()
    return send_file(io.BytesIO(file_data.data), attachment_filename=file_data.name, mimetype=file_data.file_type)


@app.route('/file/delete/<id>', methods = ['DELETE'])
def delete_file(id):
    file_data = db.session.query(File).filter(File.id == id).first()
    db.session.delete(file_data)
    db.session.commit()
    return jsonify('file delete success!')



if __name__ == '__main__':
    app.run(debug = True)