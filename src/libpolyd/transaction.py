import json

from eth_keys.datatypes import PrivateKey
from web3 import Web3


class Transaction(object):
    def __init__(self):
        self.content = {}

    def sign(self, key_bytes):
        key = PrivateKey(key_bytes)
        content = self.build_message(key.public_key)
        result = {
            'author': key.public_key.to_checksum_address(),
            'raw_transaction': content,
            'signature': key.sign_msg_hash(Web3.keccak(text=content)),
        }
        # very confused where this data goes, but trying this for now
        result.update(self.content)
        result['metadata'] = {}
        return result

    def build_message(self, pubkey):
        body = {
            'name': 'libpolyd',
            'from': pubkey.to_checksum_address(),
            'author': pubkey.to_checksum_address(),
            'data': self.content
        }

        return json.dumps(body)


class Assertion(Transaction):
    def __init__(self, guid, verdict, bid, metadata):
        super().__init__()

        self.content = {
            'guid': guid,
            'verdict': verdict,
            'bid': bid,
            'metadata': metadata,
        }
