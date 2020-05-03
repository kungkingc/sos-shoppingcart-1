
# -----------------------------------------------------------------------------------------------
# Import
# -----------------------------------------------------------------------------------------------
from flask import Flask, render_template, request, json
from flask.json import JSONEncoder
from flask_sqlalchemy import SQLAlchemy
# -----------------------------------------------------------------------------------------------


# -----------------------------------------------------------------------------------------------
# Database / Flask Setup
# -----------------------------------------------------------------------------------------------
app = Flask(__name__)

ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456@localhost/shopping_cart'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://etenqytsjeoypx:ebb1a5d71cc102c5e4ad94bf6734be94253db5b2499022e9a4d1fd5bddcdec60@ec2-52-87-135-240.compute-1.amazonaws.com:5432/d2iqpd7aouh4hr'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
# -----------------------------------------------------------------------------------------------



# -----------------------------------------------------------------------------------------------
class Cart_table(db.Model):
    # -------------------------------------------------------------------------------------------
    __tablename__ = 'shopping_cart'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)
    quantity = db.Column(db.Integer)
    complete = db.Column(db.Boolean())
    # -------------------------------------------------------------------------------------------
    def __init__(self, user_id, product_id, quantity, complete):
        self.user_id = user_id
        self.product_id = product_id
        self.quantity = quantity
        self.complete = complete
    # -------------------------------------------------------------------------------------------
    def trans_serialize(self):
        return {
            'cart_id': self.cart_id,
            'user_id': self.user_id, 
            'product_id': self.product_id,
            'quantity': self.quantity,
            'complete': self.complete
        }
    # -------------------------------------------------------------------------------------------
    def serialize(self):
        return {'user_id':self.user_id,'product_id':self.product_id,'quantity':self.quantity,'complete':self.complete}
    # -------------------------------------------------------------------------------------------

 


   
@app.route('/')
def index():
    return render_template('APItest.html')


# -----------------------------------------------------------------------------------------------
# Add product to cart
# -----------------------------------------------------------------------------------------------
@app.route('/api/v1/transactions', methods=['POST'])
def add_transaction():
    
    data = request.get_json()
    
    user_id = data['user_id']
    product_id = data ['product_id']
    quantity = data['quantity']
    complete = False
    
    data = Cart_table(user_id,product_id,quantity,complete)
    db.session.add(data)
    db.session.commit()
    return "Item has been added to the cart"
# -----------------------------------------------------------------------------------------------


# -----------------------------------------------------------------------------------------------
# Remove product to cart
'''
@app.route('/api/v1/transactions', methods=['POST'])
def remove_transaction():
    
    data = request.get_json()
    
    user_id = data['user_id']
    product_id = data ['product_id']
    #quantity = data['quantity']
    complete = False
    
    
    data = Cart_table(user_id,product_id,quantity,complete)
    
    db.session.add(data)
    db.session.commit()
    
    return "Item Has Been Removed From The Cart"
 '''
# -----------------------------------------------------------------------------------------------



# -----------------------------------------------------------------------------------------------




        
#<---- todo ------>
        
# checkout  query all transaction of given user_id and change complete to TRUE
@app.route('/api/v1/checkout', methods=['POST'])
def checkout():
    data = request.get_json()
    user_id = data['user_id']
    current_transactions = db.session.query(Cart_table).filter(Cart_table.user_id == user_id, Cart_table.complete.is_(False))
    
    if current_transactions.count() == 0:
        return "There is no active transaction for this user"
        
    transaction = db.session.query(Cart_table).filter(Cart_table.user_id == user_id).update({'complete' : True})
    
    db.session.commit()
    return "Checkout success"

    
#show active transaction (send all transaction(complete = FALSE) of given id) return in JSON format
@app.route('/api/v1/users/<id>/current_transaction', methods=['GET'])
def current_transaction(id):
    data = request.get_json()
    user_id = id
    current_transactions = db.session.query(Cart_table).filter(Cart_table.user_id == user_id, Cart_table.complete.is_(False))
    if current_transactions.count() == 0:
        return "There is no active transaction for this user"
    
    data = []
    for i in current_transactions:
        data_set = {"user_id" : i.user_id, "product_id": i.product_id, "quantity": i.quantity}
        data.append(data_set)
    json_format = json.dumps(data)
    print(json_format)
    return json_format

        
#show active transaction (send all transaction(complete = TRUE) of given id) return in JSON format
@app.route('/api/v1/users/<id>/history_transaction', methods=['GET'])
def history_transaction(id):
    data = request.get_json()
    user_id = id
    history_transaction = db.session.query(Cart_table).filter(Cart_table.user_id == 'user_id',Cart_table.complete.is_(True))
    return jsonify(current=[e.trans_serialize() for e in history_transaction])

# -----------------------------------------------------------------------------------------------

    current_transactions = db.session.query(Cart_table).filter(Cart_table.user_id == user_id, Cart_table.complete.is_(True))
    if current_transactions.count() == 0:
        return "There is no past transaction for this user"
    
    data = []
    for i in current_transactions:
        data_set = {"user_id" : i.user_id, "product_id": i.product_id, "quantity": i.quantity}
        data.append(data_set)
    json_format = json.dumps(data)
    print(json_format)
    return json_format
  
if __name__ == '__main__':
    app.run()
# -----------------------------------------------------------------------------------------------
