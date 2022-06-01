
# caching.py
# LRU Cache implementation for Random Data Generator

from hashlib import md5

LRU_DEFAULT_SIZE = 100

class LRUCache:
    def __init__(self, maxsize:int = LRU_DEFAULT_SIZE):
        self.memstore = {}
        self.keyref = []
        self.maxsize = maxsize

    def set(self, key:str, data):
        """
        Stores data against a key
        """
        keyhash = md5(key.lower().encode('utf-8')).hexdigest()
        # if key exists, remove the keyhash from its current position
        self._remove_keyhash_if_exists(keyhash)
        # add it to the most recent
        self.keyref.insert(0, keyhash)
        self.memstore[keyhash] = data
        # remove old unused keyhash
        self._remove_lru()
        
    def get(self, key:str):
        """
        Get data against a key
        """
        keyhash = md5(key.lower().encode('utf-8')).hexdigest()
        # remove the keyhash from its current position
        self._remove_keyhash_if_exists(keyhash)
        # add it to the most recent
        self.keyref.insert(0, keyhash)
        return self.memstore.get(keyhash)

    def exists(self, key:str):
        """
        Check if a key exists
        """
        keyhash = md5(key.lower().encode('utf-8')).hexdigest()
        if keyhash in self.keyref:
            return True
        return False

    def _remove_lru(self):
        while len(self.keyref) > self.maxsize:
            keyhash = self.keyref.pop()
            self.memstore.pop(keyhash, 'Key Error')
    
    def _remove_keyhash_if_exists(self, keyhash):
        """
        Removes keyhash from the current position in the keyref
        """
        if keyhash in self.keyref:
            self.keyref.remove(keyhash)





