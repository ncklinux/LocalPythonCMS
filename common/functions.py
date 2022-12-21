import re
import hashlib


class Functions(object):
    def sha256(self, string):
        return hashlib.sha256(string.encode("utf-8"), usedforsecurity=True).hexdigest()

    def validateEmail(self, string):
        if not re.fullmatch(r"[^@]+@[^@]+\.[^@]+", string):
            return False
        return True
