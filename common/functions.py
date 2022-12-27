import os
import re
import hashlib
import pandas as pd
import country_converter as coco


class Functions(object):
    def sha256(self, string):
        return hashlib.sha256(string.encode("utf-8"), usedforsecurity=True).hexdigest()

    def validateEmail(self, string):
        if not re.fullmatch(
            r"(^[a-zA-Z0-9'_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", string
        ):
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

    def comboBoxDataFrame(
        self,
        usage,
        columnValueName,
        columnValueItems,
        columnDisplayAndDefaultName,
        columnDefaultValue,
    ):
        data = pd.DataFrame(
            {
                columnValueName: columnValueItems,
            }
        )
        if usage == "language":
            data[columnDisplayAndDefaultName] = data[columnValueName].apply(
                lambda x: coco.convert(names=x, to="name_short", not_found=None)
            )
        default = pd.DataFrame(
            {
                columnValueName: [""],
                columnDisplayAndDefaultName: [columnDefaultValue],
            }
        )
        data = pd.concat(
            [default, data],
            ignore_index=True,
            sort=False,
        )

        return data
