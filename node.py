from flask import Flask, jsonify, request, send_from_directory
from wallet import Wallet
from flask_cors import CORS
from blockchain import Blockchain

app = Flask(__name__)
# wallet.create_keys()
CORS(app)
# Get Routes


@app.route('/', methods=['GET'])
def get_node_ui():
    return send_from_directory('ui', 'node.html')


@app.route('/network', methods=['GET'])
def get_network_ui():
    return send_from_directory('ui', 'network.html')


@app.route('/nodes', methods=['GET'])
def get_nodes():
    all_nodes = blockchain.get_all_nodes()
    response = {
        'all_nodes': all_nodes
    }
    return jsonify(response), 200


@app.route('/walette', methods=['GET'])
def load_keys():
    if wallet.load_keys():
        global blockchain
        blockchain = Blockchain(wallet.public_key, port)
        response = {
            'public_key': wallet.public_key,
            'private_key': wallet.private_key,
            'funds': blockchain.get_balence()
        }
        return jsonify(response), 201
    else:
        response = {'message': 'loading the keys failed !'}
        return jsonify(response), 500


@app.route('/balance', methods=['GET'])
def get_balence():
    balance = blockchain.get_balence()
    if balance != None:
        response = {
            'message': 'fetching balance succeded ',
            'funds': balance
        }
        return jsonify(response), 200
    else:
        response = {
            'message': 'Loading balance failed !',
            'wallet_set_up': wallet.public_key != None
        }
        return jsonify(response), 500


@app.route('/chain', methods=['GET'])
def get_chain():
    chain_snapshot = blockchain.chain
    dict_chain = [block.__dict__.copy() for block in chain_snapshot]
    for dict_block in dict_chain:
        dict_block['transactions'] = [tx.__dict__.copy()
                                      for tx in dict_block['transactions']]
    return jsonify(dict_chain), 200


@app.route('/transactions', methods=['GET'])
def get_transaction():
    transactions = blockchain.get_open_transactions()
    dict_transactions = [tx.__dict__ for tx in transactions]
    # response = {
    #     'message' : 'fetched transactions seuccessfuly !',
    #     'transactions' : dict_transactions
    # }
    return jsonify(dict_transactions), 200


# Post Routes


@app.route('/mine', methods=['POST'])
def mine():
    print(blockchain.resolve_conflits)
    if blockchain.resolve_conflits: 
        response = {
            'messsage':'resolve conflict first, block not added'
        }
        return jsonify(response) , 409      
    block = blockchain.mine_block()
    if block != None:
        dict_block = block.__dict__.copy()
        dict_block['transactions'] = [
            tx.__dict__ for tx in dict_block['transactions']]
        # Succée
        response = {
            'message': 'block added successfuly',
            'block': dict_block,
            'funds': blockchain.get_balence()
        }
        return jsonify(response), 201
    else:
        # Echéc
        response = {
            'message': 'adding block failed',
            'wallet_set_up': wallet.public_key != None,
            'funds': blockchain.get_balence()
        }
        return jsonify(response), 500


@app.route('/node', methods=['POST'])
def add_node():
    values = request.get_json()
    if not values:
        response = {
            'message': 'No Data'
        }
        return jsonify(response), 500
    if 'node' not in values:
        response = {
            'message': 'No node data found'
        }
        return jsonify(response), 500
    node = values['node']
    blockchain.add_peer_node(node)
    response = {
        'message': 'node added successfuly',
        'all_nodes': blockchain.get_all_nodes()
    }
    return jsonify(response), 201


@app.route('/transaction', methods=['POST'])
def add_transaction():
    print('staaaarts')
    if wallet.public_key == None:
        response = {
            'message': "no walette set up"
        }
        return jsonify(response), 400
    values = request.get_json()
    if not values:
        response = {
            'message': 'No data found'
        }
        return jsonify(response), 500
    required_fields = ['recipient', 'amount']
    if not all(field in values for field in required_fields):
        response = {
            'message': 'required data is missing'
        }
        return jsonify(response),
    recipient = values['recipient']
    amount = values['amount']
    signature = wallet.sign_transaction(wallet.public_key, recipient, amount)
    success = blockchain.add_transaction(
        recipient, wallet.public_key, signature, amount)
    if success:
        response = {
            'message': "successfuly added transaction",
            'transaction': {
                'sender': wallet.public_key,
                'recipient': recipient,
                'amount': amount,
                'signature': signature
            },
            'funds': blockchain.get_balence()
        }
        return jsonify(response), 201

    else:
        response = {
            'message': 'creating transaction failed',
        }
        return jsonify(response), 500


@app.route('/walette', methods=['POST'])
def create_keys():
    wallet.create_keys()
    if wallet.save_to_file():
        global blockchain
        blockchain = Blockchain(wallet.public_key, port)
        response = {
            'public_key': wallet.public_key,
            'private_key': wallet.private_key,
            'funds': blockchain.get_balence()
        }
        return jsonify(response), 201
    else:
        response = {'message': 'saving the keys failed !'}
        return jsonify(response), 500


@app.route('/broadcast-transaction', methods=['POST'])
def broadcast_transaction():
    values = request.get_json()
    if not values:
        response = {
            'message': 'No data found'
        }
        return jsonify(response), 500
    required = ['sender', 'recipient', 'amount', 'signature']
    if not all([key in values for key in required]):
        response = {
            'message': 'some data is missing'
        }
        return jsonify(response), 400
    success = blockchain.add_transaction(
        values['recipient'], values['sender'], values['signature'], values['amount'], is_reciving=True)
    if success:
        response = {
            'message': "successfuly added transaction",
            'transaction': {
                'sender': values['sender'],
                'recipient': values['recipient'],
                'amount': values['amount'],
                'signature': values['signature']
            }
        }
        return jsonify(response), 200
    else:
        response = {
            'message': 'creating transaction failed',
        }
        return jsonify(response), 500


@app.route('/broadcast-block', methods=['POST'])
def broadcast_block():
    values = request.get_json()
    if not values:
        response = {
            'message': 'No data found'
        }
        return jsonify(response), 400
    if 'block' not in values:
        response = {
            'message': 'block data is missing'
        }
        return jsonify(response), 400

    block = values['block']
    if block['index'] == blockchain.chain[-1].index + 1:
        if blockchain.add_block(block): 
            print('block_added')
            response = {
                'message':'block added!', 
            }
            return jsonify(response) , 201
        else: 
            print('block not added')
            response = {
                'message':'block seems invalid !'
            }
            return jsonify(response) , 409
    elif block['index'] > blockchain.chain[-1].index:
        print(str(block['index']) , str(blockchain.chain[-1].index))
        response = {
            'message': 'blockchain seems to different to the local blockchain'
        }
        blockchain.resolve_conflits = True
        return jsonify(response), 200
    else:
        response = {
            'message': 'blockchain seems to be shorter, block not edit'
        }
        return jsonify(response), 409
        # status code 409 means that the data sent is invalid


@app.route('/resolve-conflicts', methods=['POST'])
def resolve_conflicts():
    replaced = blockchain.resolve()
    if replaced:
        response= {
            'message':'Chain replaced'
        }
    else:
        response ={
            'message':'Local chain capted'
        }
    return jsonify(response) , 200

# DELETE Routes

@app.route('/node/<node_url>', methods=['DELETE'])
def remove_node(node_url):
    if node_url == '' or node_url == None:
        response = {
            'message': "No Node found"
        }
        return jsonify(response), 500
    blockchain.remove_peer_node(node_url)
    response = {
        'message': 'Node removed',
        'all_nodes': blockchain.get_all_nodes()
    }
    return jsonify(response), 200


if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-p', '--port', type=int, default=5000)
    args = parser.parse_args()
    port = args.port
    wallet = Wallet(port)
    blockchain = Blockchain(wallet.public_key, port)
    app.run(host='0.0.0.0', port=port)
