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
import sys
import time
import requests
import time
import base64

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

header_written = False
_timed = False
_profd = False
_port = 5000


def _write_time(alg, func, bit, etime):
    global header_written
    time_file = '/home/coldmind/tmp/gsl/time_profile_1.csv'
    if not header_written and not os.path.getsize(time_file) > 0:
        with open(time_file, 'a') as __fd__:
            __fd__.write('alg;func;bit;time\n')
            header_written = True
    with open(time_file, 'a') as __fd__:
        __fd__.write(f'{alg};{func};{bit};{etime}\n')


def _profile_timings():
    if _profd:
        keys = {
                'p1_pub': '',
                'p1_prv': '',
                'p2_pub': '',
                'p2_prv': ''
                }
        p1_prv, p1_pub = generate_keys(ret=True)
        p2_prv, p2_pub = generate_keys(ret=True)
        print(f'sending from {p1_pub} \n to \n{p2_pub}\nusing\np1_prv')
        # Send for p1 to p2 100 money
        #
        _perform_transaction(p1_pub, p1_prv, p2_pub, 100)
        check_transactions()


def _perform_transaction(from_, prv_key, addr_to, amount):
    try:
        len_prv = len(prv_key)
    except:
        len_prv = len(str(prv_key))

    if dss.name == 'gost' or len_prv == 64:
        signature, message = _sign_msg(prv_key)
        url = f'http://localhost:{_port}/mycoin'
        payload = {'from': from_,
                   'to': addr_to,
                   'amount': amount,
                   'signature': signature.decode(),
                   'message': message}
        headers = {'Content-Type': 'application/json'}

        res = requests.post(url, json=payload, headers=headers)
        print(res.text)
    else:
        print('Wrong address or key length! Verify and try again.')


def check_transactions():
    # Gets whole blockchain
    res = requests.get(f'http://localhost:{_port}/blocks')
    print(res.text)


def generate_keys(ret=False):
    if _timed:
        t1 = time.time()

    try:
        singningkey = dss.SigningKey.generate(curve=dss.SECP256k1)
    except:
        singningkey = dss.SigningKey().generate()

    try:
        private_key = singningkey.to_string().hex()
    except:
        private_key = singningkey.to_string()

    vk = singningkey.get_verifying_key()
    try:
        public_key = vk.to_string().hex()
    except:
        public_key = singningkey.to_string(pub=True)


    if _timed:
        t2 = time.time()
        _write_time(alg_name, 'Key pair generation', alg_bit, t2-t1)

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


def _sign_msg(private_key):
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


def provide_options():
    response = None
    while response not in ['1', '2', '3']:
        response = input(
            """
            Which action would you like to take?
            1. Generate new wallet
            2. Send coins to another wallet
            3. View transactions\n
            """)
    if response == '1':
        print("""=========================================\n
IMPORTANT: save this credentials or you won't be able to recover your wallet\n
=========================================\n""")
        generate_keys()
    elif response == '2':
        addr_from = input('From: introduce your wallet address (public key)\n')
        private_key = input('Introduce your private key\n')
        addr_to = input('To: introduce destination wallet address\n')
        amount = input('Amount: number stating how much do you want to send\n')
        print('=========================================\n\n')
        print('Is everything correct?\n')
        print('From: {0}\nPrivate Key: {1}\nTo: {2}\nAmount: {3}\n'.format(addr_from, private_key, addr_to, amount))
        response = input('y/n\n')
        if response.lower() == 'y':
            _perform_transaction(addr_from, private_key, addr_to, amount)
    else:
        check_transactions()


if __name__ == '__main__':
    # print("""       =========================================\n
    #     Build using source code from and so more help at: https://github.com/cosme12/SimpleCoin\n
    #      ======================================""")
    #
    if _profd:
        _profile_timings()
        sys.exit()
    provide_options()
    torepeat = input('Repeat? Would you like one more action? (Y/[N])')
    while torepeat.lower() in ['y', 'yes', 'da']:
        provide_options()
    print('Exiting..')

# EOF
