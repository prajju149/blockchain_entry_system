import hashlib
import hmac
import json
import time


class Blockchain:
    """
    Simple file-backed blockchain with HMAC signature for tamper evidence.
    Each block: {index, timestamp, data, prev_hash, hash, signature}
    """

    def __init__(self, path, secret_key):
        self.path = path
        self.secret_key = secret_key.encode() if isinstance(secret_key, str) else secret_key
        try:
            with open(self.path, 'r') as f:
                self.chain = json.load(f)
        except:
            self.chain = []

    def _hash_block(self, block):
        b = dict(block)
        b.pop('hash', None)
        b.pop('signature', None)
        block_str = json.dumps(b, sort_keys=True).encode()
        return hashlib.sha256(block_str).hexdigest()

    def _sign(self, block_hash):
        return hmac.new(self.secret_key, block_hash.encode(), hashlib.sha256).hexdigest()

    def add_block(self, data):
        prev_hash = self.chain[-1]['hash'] if self.chain else '0' * 64
        block = {'index': len(self.chain), 'timestamp': time.time(), 'data': data, 'prev_hash': prev_hash}
        block['hash'] = self._hash_block(block)
        block['signature'] = self._sign(block['hash'])
        self.chain.append(block)
        self._save()
        return block

    def _save(self):
        with open(self.path, 'w') as f:
            json.dump(self.chain, f, indent=2)

    def load_chain(self):
        return self.chain

    def verify(self):
        for i, b in enumerate(self.chain):
            sig = b.get('signature')
            h = b.get('hash')
            if self._hash_block(b) != h:
                return False, f'hash mismatch at {i}'
            if self._sign(h) != sig:
                return False, f'signature mismatch at {i}'
            if i > 0 and b.get('prev_hash') != self.chain[i-1].get('hash'):
                return False, f'prev_hash mismatch at {i}'
        return True, 'ok'
