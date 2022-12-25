import os
import re
import hashlib


class Functions(object):
    def sha256(self, string):
        return hashlib.sha256(string.encode("utf-8"), usedforsecurity=True).hexdigest()

    def validateEmail(self, string):
        if not re.fullmatch(r"[^@]+@[^@]+\.[^@]+", string):
            return False
        return True

    def getCountryCodesFromLocales(self):
        directory = "locales"
        fileFormat = "*.yml"
        languages = []
        for item in os.listdir(directory):
            if item.endswith(fileFormat[1:]):
                languages.append(re.split("[.]", str(item))[-2])
        return languages
