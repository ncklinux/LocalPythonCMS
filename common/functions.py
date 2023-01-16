import os
import re
import hashlib
import pandas as pd
import country_converter as coco


class Functions(object):
    def sha256(self, string):
        return hashlib.sha256(string.encode("utf-8"), usedforsecurity=True).hexdigest()

    def validate_email(self, string):
        if not re.fullmatch(
            r"(^[a-zA-Z0-9'_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", string
        ):
            return False
        return True

    def get_country_codes_from_locales(self):
        directory = "locales"
        file_format = "*.yml"
        languages = []
        for item in os.listdir(directory):
            if item.endswith(file_format[1:]):
                languages.append(re.split("[.]", str(item))[-2])
        return languages

    def combo_box_data_frame(
        self,
        usage,
        column_value_name,
        column_value_items,
        column_display_and_default_name,
        column_default_value,
    ):
        data = pd.DataFrame(
            {
                column_value_name: column_value_items,
            }
        )
        if usage == "language":
            data[column_display_and_default_name] = data[column_value_name].apply(
                lambda x: coco.convert(names=x, to="name_short", not_found=None)
            )
        default = pd.DataFrame(
            {
                column_value_name: [""],
                column_display_and_default_name: [column_default_value],
            }
        )
        data = pd.concat(
            [default, data],
            ignore_index=True,
            sort=False,
        )
        return data
