"""This is going to be your wallet. Here you can do several things:
- Generate a new address (public and private key). You are going
to use this address (public key) to send or receive any transactions. You can
have as many addresses as you wish, but keep in mind that if you
lose its credential data, you will not be able to retrieve it.

- Send coins to another address
- Retrieve the entire blockchain and check your balance

If this is your first time using this script don't forget to generate
a new address and edit miner config file with it (only if you are
going to mine).

Timestamp in hashed message. When you send your transaction it will be received
by several nodes. If any node mine a block, your transaction will get added to the
blockchain but other nodes still will have it pending. If any node see that your
transaction with same timestamp was added, they should remove it from the
node_pending_transactions list to avoid it get processed more than 1 time.
"""

import os
import time
import requests
import time
import base64

try:
    import mydss
    dss = mydss
    alg_name = dss.name
    alg_bit = dss.bit
except:
    import ecdsa
    dss = ecdsa
    alg_name = 'ecdsa'
    alg_bit = '256'

header_written = False
_timed = False
_profd = False
_port = 5000

def _write_time(alg, func, bit, etime):
    global header_written
    if not header_written and not os.path.getsize('time.csv') > 0:
        with open('time.csv', 'a') as __fd__:
            __fd__.write('alg;func;bit;time\n')
            header_written = True
    with open('time.csv', 'a') as __fd__:
        __fd__.write(f'{alg};{func};{bit};{etime}\n')


def _profile_timings():
    if _profd:
        keys = {
                'p1_pub': '',
                'p1_prv': '',
                'p2_pub': '',
                'p2_prv': ''
                }
        p1_prv, p1_pub = generate_ECDSA_keys(ret=True)
        p2_prv, p2_pub = generate_ECDSA_keys(ret=True)
        # Send for p1 to p2 100 money
        send_transaction(p1_pub, p1_prv, p2_pub, 100)
        check_transactions()


def wallet():
    response = None
    while response not in ["1", "2", "3"]:
        response = input("""What do you want to do?
        1. Generate new wallet
        2. Send coins to another wallet
        3. Check transactions\n""")
    if response == "1":
        # Generate new wallet
        print("""=========================================\n
IMPORTANT: save this credentials or you won't be able to recover your wallet\n
=========================================\n""")
        generate_ECDSA_keys()
    elif response == "2":
        addr_from = input("From: introduce your wallet address (public key)\n")
        private_key = input("Introduce your private key\n")
        addr_to = input("To: introduce destination wallet address\n")
        amount = input("Amount: number stating how much do you want to send\n")
        print("=========================================\n\n")
        print("Is everything correct?\n")
        print("From: {0}\nPrivate Key: {1}\nTo: {2}\nAmount: {3}\n".format(addr_from, private_key, addr_to, amount))
        response = input("y/n\n")
        if response.lower() == "y":
            send_transaction(addr_from, private_key, addr_to, amount)
    else:  # Will always occur when response == 3.
        check_transactions()


def send_transaction(addr_from, private_key, addr_to, amount):
    """Sends your transaction to different nodes. Once any of the nodes manage
    to mine a block, your transaction will be added to the blockchain. Despite
    that, there is a low chance your transaction gets canceled due to other nodes
    having a longer chain. So make sure your transaction is deep into the chain
    before claiming it as approved!
    """
     # For fast debugging REMOVE LATER
     # private_key="181f2448fa4636315032e15bb9cbc3053e10ed062ab0b2680a37cd8cb51f53f2"
     # amount="3000"
     # addr_from="SD5IZAuFixM3PTmkm5ShvLm1tbDNOmVlG7tg6F5r7VHxPNWkNKbzZfa+JdKmfBAIhWs9UKnQLOOL1U+R3WxcsQ=="
     # addr_to="SD5IZAuFixM3PTmkm5ShvLm1tbDNOmVlG7tg6F5r7VHxPNWkNKbzZfa+JdKmfBAIhWs9UKnQLOOL1U+R3WxcsQ=="

    if len(private_key) == 64 or dss.name == 'gost':
        signature, message = sign_ECDSA_msg(private_key)
        url = f'http://localhost:{_port}/txion'
        payload = {"from": addr_from,
                   "to": addr_to,
                   "amount": amount,
                   "signature": signature.decode(),
                   "message": message}
        headers = {"Content-Type": "application/json"}

        res = requests.post(url, json=payload, headers=headers)
        print(res.text)
    else:
        print("Wrong address or key length! Verify and try again.")


def check_transactions():
    """Retrieve the entire blockchain. With this you can check your
    wallets balance. If the blockchain is to long, it may take some time to load.
    """
    res = requests.get(f'http://localhost:{_port}/blocks')
    print(res.text)


def generate_ECDSA_keys(ret=False):
    """This function takes care of creating your private and public (your address) keys.
    It's very important you don't lose any of them or those wallets will be lost
    forever. If someone else get access to your private key, you risk losing your coins.

    private_key: str
    public_ley: base64 (to make it shorter)
    """

    if _timed:
        t1 = time.time()

    try:
        sk = dss.SigningKey.generate(curve=dss.SECP256k1)   # this is your sign (private key)
    except:
        sk = dss.SigningKey().generate()   # this is your sign (private key)

    try:
        private_key = sk.to_string().hex()  # convert your private key to hex
    except:
        private_key = sk.to_string()  # convert your private key to hex

    vk = sk.get_verifying_key()  # this is your verification key (public key)
    try:
        public_key = vk.to_string().hex()
    except:
        public_key = sk.to_string(pub=True)


    if _timed:
        t2 = time.time()
        _write_time(alg_name, 'Key pair generation', alg_bit, t2-t1)

    # we are going to encode the public key to make it shorter
    try:
        public_key = base64.b64encode(bytes.fromhex(public_key.decode()))
    except:
        public_key = base64.b64encode(bytes.fromhex(public_key))

    if ret:
        return private_key, public_key.decode()

    filename = input("Write the name of your new address: ") + ".txt"

    with open(filename, "w") as f:
        f.write("Private key: {0}\nWallet address / Public key: {1}".format(private_key, public_key.decode()))
    print("Your new address and private key are now in the file {0}".format(filename))


def sign_ECDSA_msg(private_key):
    """Sign the message to be sent
    private_key: must be hex

    return
    signature: base64 (to make it shorter)
    message: str
    """
    # Get timestamp, round it, make it into a string and encode it to bytes
    message = str(round(time.time()))
    bmessage = message.encode()

    if _timed:
        t1 = time.time()

    try:
        sk = dss.SigningKey.from_string(bytes.fromhex(private_key), curve=dss.SECP256k1)
    except:
        sk = dss.SigningKey().from_string(str(private_key))
    signed = sk.sign(bmessage)

    if _timed:
        t2 = time.time()
        _write_time(alg_name, 'Signing message', alg_bit, t2-t1)

    signature = base64.b64encode(signed)
    return signature, message


if __name__ == '__main__':
    print("""       =========================================\n
        SIMPLE COIN v1.0.0 - BLOCKCHAIN SYSTEM\n
       =========================================\n\n
        You can find more help at: https://github.com/cosme12/SimpleCoin\n
        Make sure you are using the latest version or you may end in
        a parallel chain.\n\n\n""")
    wallet()
    input("Press ENTER to exit...")
