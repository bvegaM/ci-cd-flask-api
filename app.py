## app.py
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import fields

app = Flask(__name__)
ma = Marshmallow(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://flaskuser:Bs1JdlZ0ZvRgWwRsvOikSQrUBKa80LlU@dpg-cndqlbun7f5s73bmod7g-a.oregon-postgres.render.com/dbsum'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Sum(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    num1 = db.Column(db.Integer, nullable=False)
    num2 = db.Column(db.Integer, nullable=False)
    result = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Sum {self.id}: {self.num1} + {self.num2} = {self.result}>'

# Crear el esquema SumSchema
    
class SumSchema(ma.Schema):
    id = fields.Integer()
    num1 = fields.Integer()
    num2 = fields.Integer()
    result = fields.Integer()

sums_schema = SumSchema(many=True)  


@app.route('/sum', methods=['GET'])
def find_all():
    sums= db.session.execute(db.select(Sum)).scalars()
    return sums_schema.jsonify(sums), 200


@app.route('/sum', methods=['POST'])
def sum():
    data = request.get_json()
    num1 = data['num1']
    num2 = data['num2']
    result = num1 + num2

    # Guardar el resultado en la tabla Sum
    sum_entry = Sum(num1=num1, num2=num2, result=result)
    db.session.add(sum_entry)
    db.session.commit()

    return jsonify({'result': result})

with app.app_context():
        db.drop_all()
        db.create_all()