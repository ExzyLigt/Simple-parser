import datetime

import tablib
import ujson


def json_to_excel(json_f: str):

    xlsx_filename = str(datetime.datetime.now()) + ".xlsx"

    with open(xlsx_filename, "wb") as excel_file, open(json_f, "r") as json_file:
        json_ = ujson.load(json_file)

        headers = ["article"]
        headers.extend(["soputstvishiy tovar " + str(digit) for digit in range(1, 9)])

        data = [
            [k, *v]
            if len([k, *v]) == len(headers)
            else [k, *v] + [""] * (len(headers) - len([k, *v]))
            for k, v in json_.items()
        ]
        ds = tablib.Dataset(*data, headers=headers)
        excel_file.write(ds.export("xlsx"))


def dict_to_excel(d: dict[str, list[str]]):

    xlsx_filename = str(datetime.datetime.now()) + ".xlsx"

    with open(xlsx_filename, "wb") as excel_file:
        headers = ["article"]
        headers.extend(["soputstvishiy tovar " + str(digit) for digit in range(1, 9)])

        data = [
            [k, *v]
            if len([k, *v]) == len(headers)
            else [k, *v] + [""] * (len(headers) - len([k, *v]))
            for k, v in d.items()
        ]
        ds = tablib.Dataset(*data, headers=headers)
        excel_file.write(ds.export("xlsx"))
