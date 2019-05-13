import os
import time
import hashlib
import json
import requests
import base64
from datetime import datetime
from flask import Flask, request
from multiprocessing import Process, Pipe
from werkzeug.serving import run_simple

try:
    import mydss
    dss = mydss
    if hasattr(dss, 'name') and hasattr(dss, 'bit'):
        alg_name = dss.name
        alg_bit = dss.bit
        try:
            from mydss import mydss
            dss = mydss
        except:
            dss = mydss
except:
    import ecdsa
    dss = ecdsa
    alg_name = 'ecdsa'
    alg_bit = '256'

try:
    import myhashing
    hashing = myhashing
    if hasattr(hashing, 'name') and hasattr(hashing, 'bit'):
        hash_name = hashing.name
        hash_bit = hashing.bit
        try:
            from myhashing import myhashing
            hashing = myhashing
        except:
            hashing = myhashing
except:
    hashing = hashlib.sha256
    hash_name = 'sha256'
    hash_bit = '256'

##============================
# MINER CONFIG
##============================

# Write your generated adress here. All coins mined will go to this address
MINER_ADDRESS = "q3nf394hjg-random-miner-address-34nf3i4nflkn3oi"

# Write your node url or ip. If you are running it localhost use default
_port = 5000
MINER_NODE_URL = f"http://localhost:{_port}"

# Store the url data of every other node in the network
# so that we can communicate with them
PEER_NODES = []
##============================

a, b = Pipe()
header_written = False
to_reload = False
_timed = False
_profd = False


def _write_time(alg, func, bit, etime):
    global header_written
    time_file = '/home/coldmind/tmp/gsl/time_profile_1.csv'
    if not os.path.exists(time_file) or (not header_written and not os.path.getsize(time_file) > 0):
        with open(time_file, 'a') as __fd__:
            __fd__.write('alg;func;bit;time\n')
            header_written = True
    with open(time_file, 'a') as __fd__:
        __fd__.write(f'{alg};{func};{bit};{etime}\n')


class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        """Returns a new Block object. Each block is "chained" to its previous
        by calling its unique hash.

        Args:
            index (int): Block number.
            timestamp (int): Block creation timestamp.
            data (str): Data to be sent.
            previous_hash(str): String representing previous block unique hash.

        Attrib:
            index (int): Block number.
            timestamp (int): Block creation timestamp.
            data (str): Data to be sent.
            previous_hash(str): String representing previous block unique hash.
            hash(str): Current block unique hash.

        """
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.hash_block()

    def hash_block(self):
        """Creates the unique hash for the block. It uses sha256 or given hashing algorithm."""
        if _timed:
            t1 = time.time()
        hasher = hashing()
        hasher.update((str(self.index) + str(self.timestamp) + str(self.data) + str(self.previous_hash)).encode('utf-8'))
        hexxx = hasher.hexdigest()
        if _timed:
            t2 = time.time()
            _write_time(hash_name, 'Hash value computing', hash_bit, t2-t1)
        return hexxx


def create_genesis_block():
    """To create each block, it needs the hash of the previous one. First
    block has no previous, so it must be created manually (with index zero
     and arbitrary previous hash)"""
    return Block(0, time.time(), {
        "proof-of-work": 9,
        "transactions": None},
        "0")


# Node's blockchain copy
BLOCKCHAIN = [create_genesis_block()]

""" Stores the transactions that this node has in a list.
If the node you sent the transaction adds a block
it will get accepted, but there is a chance it gets
discarded and your transaction goes back as if it was never
processed"""
NODE_PENDING_TRANSACTIONS = []


def proof_of_work(last_proof, blockchain):
    if _timed:
        t1 = time.time()
    # Creates a variable that we will use to find our next proof of work
    incrementer = last_proof + 1
    # Keep incrementing the incrementer until it's equal to a number divisible by 9
    # and the proof of work of the previous block in the chain
    start_time = time.time()
    while not (incrementer % 7919 == 0 and incrementer % last_proof == 0):
        incrementer += 1
        # Check if any node found the solution every 60 seconds
        if int((time.time()-start_time) % 60) == 0:
            # If any other node got the proof, stop searching
            new_blockchain = consensus(blockchain)
            if new_blockchain:
                # (False: another node got proof first, new blockchain)
                return False, new_blockchain
    # Once that number is found, we can return it as a proof of our work
    if _timed:
        t2 = time.time()
        _write_time(hash_name, 'Proof of Work', hash_bit, t2-t1)
    return incrementer, blockchain


def mine(a, blockchain, node_pending_transactions):
    BLOCKCHAIN = blockchain
    NODE_PENDING_TRANSACTIONS = node_pending_transactions
    while True:
        """Mining is the only way that new coins can be created.
        In order to prevent too many coins to be created, the process
        is slowed down by a proof of work algorithm.
        """

        if _timed:
            t1 = time.time()
        # Get the last proof of work
        last_block = BLOCKCHAIN[len(BLOCKCHAIN) - 1]
        last_proof = last_block.data['proof-of-work']
        # Find the proof of work for the current block being mined
        # Note: The program will hang here until a new proof of work is found
        proof = proof_of_work(last_proof, BLOCKCHAIN)
        # If we didn't guess the proof, start mining again
        if not proof[0]:
            # Update blockchain and save it to file
            BLOCKCHAIN = proof[1]
            a.send(BLOCKCHAIN)
            continue
        else:
            # Once we find a valid proof of work, we know we can mine a block so
            # ...we reward the miner by adding a transaction
            # First we load all pending transactions sent to the node server
            NODE_PENDING_TRANSACTIONS = requests.get(MINER_NODE_URL + "/txion?update=" + MINER_ADDRESS).content
            NODE_PENDING_TRANSACTIONS = json.loads(NODE_PENDING_TRANSACTIONS)
            # Then we add the mining reward
            NODE_PENDING_TRANSACTIONS.append({
                "from": "network",
                "to": MINER_ADDRESS,
                "amount": 1})
            # Now we can gather the data needed to create the new block
            new_block_data = {
                "proof-of-work": proof[0],
                "transactions": list(NODE_PENDING_TRANSACTIONS)
            }
            new_block_index = last_block.index + 1
            new_block_timestamp = time.time()
            last_block_hash = last_block.hash
            # Empty transaction list
            NODE_PENDING_TRANSACTIONS = []
            # Now create the new block
            mined_block = Block(new_block_index, new_block_timestamp, new_block_data, last_block_hash)
            BLOCKCHAIN.append(mined_block)
            # Let the client know this node mined a block
            try:
                print(json.dumps({
                  "index": new_block_index,
                  "timestamp": str(new_block_timestamp),
                  "data": new_block_data,
                  "hash": last_block_hash.decode()
                }) + "\n")
            except:
                print(json.dumps({
                  "index": new_block_index,
                  "timestamp": str(new_block_timestamp),
                  "data": new_block_data,
                  "hash": last_block_hash
                }) + "\n")
            a.send(BLOCKCHAIN)
            requests.get(MINER_NODE_URL + "/blocks?update=" + MINER_ADDRESS)
            if _timed:
                t2 = time.time()
                _write_time(hash_name, 'Mining one block', hash_bit, t2-t1)


def find_new_chains():
    # Get the blockchains of every other node
    other_chains = []
    for node_url in PEER_NODES:
        # Get their chains using a GET request
        block = requests.get(node_url + "/blocks").content
        # Convert the JSON object to a Python dictionary
        block = json.loads(block)
        # Verify other node block is correct
        validated = validate_blockchain(block)
        if validated:
            # Add it to our list
            other_chains.append(block)
    return other_chains


def consensus(blockchain):
    # Get the blocks from other nodes
    other_chains = find_new_chains()
    # If our chain isn't longest, then we store the longest chain
    BLOCKCHAIN = blockchain
    longest_chain = BLOCKCHAIN
    for chain in other_chains:
        if len(longest_chain) < len(chain):
            longest_chain = chain
    # If the longest chain wasn't ours, then we set our chain to the longest
    if longest_chain == BLOCKCHAIN:
        # Keep searching for proof
        return False
    else:
        # Give up searching proof, update chain and start over again
        BLOCKCHAIN = longest_chain
        return BLOCKCHAIN


def validate_blockchain(block):
    """Validate the submitted chain. If hashes are not correct, return false
    block(str): json
    """
    return True


def validate_signature(public_key, signature, message):
    """Verifies if the signature is correct. This is used to prove
    it's you (and not someone else) trying to do a transaction with your
    address. Called when a user tries to submit a new transaction.
    """
    if _timed:
        t1 = time.time()
    try:
        if hasattr(dss, 'name'):
            if dss.name == 'gost':
                public_key = base64.b64decode(public_key)
        else:
            public_key = (base64.b64decode(public_key)).hex()
    except:
        pass
    signature = base64.b64decode(signature)
    try:
        print(public_key)
        print(type(public_key))
        vk = dss.VerifyingKey().from_string(public_key)
    except:
        curve = dss.SECP256k1
        vk = dss.VerifyingKey.from_string(bytes.fromhex(public_key), curve=curve)

    # Try changing into an if/else statement as except is too broad.
    try:
        res = vk.verify(signature, message.encode())
        if _timed:
            t2 = time.time()
            _write_time(alg_name, 'Verifying signature', alg_bit, t2-t1)
        return res
    except:
        return False


def welcome_msg():
    # print("""       =========================================\n
    #     SIMPLE COIN v1.0.0 - BLOCKCHAIN SYSTEM\n
    #    =========================================\n\n
    #     You can find more help at: https://github.com/cosme12/SimpleCoin\n
    #     Make sure you are using the latest version or you may end in
    #     a parallel chain.\n\n\n""")
    pass


def get_app():
    app = Flask(__name__)
    now = datetime.now()

    @app.route('/')
    def index():
        return f'hello, the app started at %s' % now

    @app.route('/reload')
    def reload():
        global to_reload
        to_reload = True
        return 'reloaded'

    @app.route('/blocks', methods=['GET'])
    def get_blocks():
        # Load current blockchain. Only you should update your blockchain
        if request.args.get("update") == MINER_ADDRESS:
            global BLOCKCHAIN
            BLOCKCHAIN = b.recv()
        chain_to_send = BLOCKCHAIN
        # Converts our blocks into dictionaries so we can send them as json objects later
        chain_to_send_json = []
        for block in chain_to_send:
            try:
                block = {
                    "index": str(block.index),
                    "timestamp": str(block.timestamp),
                    "data": str(block.data),
                    "hash": block.hash.decode()
                }
            except:
                block = {
                    "index": str(block.index),
                    "timestamp": str(block.timestamp),
                    "data": str(block.data),
                    "hash": block.hash
                }
            chain_to_send_json.append(block)

        # Send our chain to whomever requested it
        chain_to_send = json.dumps(chain_to_send_json)
        return chain_to_send

    @app.route('/txion', methods=['GET', 'POST'])
    def transaction():
        """Each transaction sent to this node gets validated and submitted.
        Then it waits to be added to the blockchain. Transactions only move
        coins, they don't create it.
        """
        if request.method == 'POST':
            # On each new POST request, we extract the transaction data
            new_txion = request.get_json()
            # Then we add the transaction to our list
            if validate_signature(new_txion['from'], new_txion['signature'], new_txion['message']):
                NODE_PENDING_TRANSACTIONS.append(new_txion)
                # Because the transaction was successfully
                # submitted, we log it to our console
                print("New transaction")
                print("FROM: {0}".format(new_txion['from']))
                print("TO: {0}".format(new_txion['to']))
                print("AMOUNT: {0}\n".format(new_txion['amount']))
                # Then we let the client know it worked out
                return "Transaction submission successful\n"
            else:
                return "Transaction submission failed. Wrong signature\n"
        # Send pending transactions to the mining process
        elif request.method == 'GET' and request.args.get("update") == MINER_ADDRESS:
            pending = json.dumps(NODE_PENDING_TRANSACTIONS)
            # Empty transaction list
            NODE_PENDING_TRANSACTIONS[:] = []
            return pending

    return app


class AppReloader(object):
    def __init__(self, create_app):
        self.create_app = create_app
        self.app = create_app()

    def get_application(self):
        global to_reload
        if to_reload:
            self.app = self.create_app()
            to_reload = False

        return self.app

    def __call__(self, environ, start_response):
        app = self.get_application()
        return app(environ, start_response)


def profd_run():
    welcome_msg()
    # Start mining
    p1 = Process(target=mine, args=(a, BLOCKCHAIN, NODE_PENDING_TRANSACTIONS))
    p1.start()
    # Start server to receive transactions

    kwargs = {
            'use_reloader': False,
            'use_debugger': True,
            'use_evalex': True
            }
    app = AppReloader(get_app)
    p2 = Process(target=run_simple, args=('localhost', 5000, app), kwargs=kwargs)
    p2.start()


def full_run():
    if _profd:
        profd_run()
    else:
        welcome_msg()
        node = get_app()
        # Start mining
        p1 = Process(target=mine, args=(a, BLOCKCHAIN, NODE_PENDING_TRANSACTIONS))
        p1.start()
        # Start server to receive transactions
        p2 = Process(target=node.run(), args=b)
        p2.start()


if __name__ == '__main__':
    full_run()
