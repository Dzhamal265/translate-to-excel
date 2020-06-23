import json
from functools import reduce
from pathlib import Path

import pandas as pd

paths = tuple(Path(__file__).parent.joinpath('translate').iterdir())

columns = tuple(map(lambda pth: str(pth).split('.')[0][-2:], paths))


def to_list(result, next_item):
    if isinstance(result, str):
        return (result, next_item)
    if isinstance(next_item, dict):
        return (*result, *tuple(sorted(next_item.values())))
    return (*result, next_item)


def main():
    df = pd.DataFrame()
    for i, path in enumerate(paths):
        with open(str(path)) as f:
            translate = json.load(f)
        translate = dict(map(lambda key: (key, translate[key]), sorted(translate.keys())))
        translate = reduce(to_list, tuple(translate.values()))
        column_value = pd.Series(translate)
        df.insert(column=columns[i], loc=i, value=column_value)
    df.to_excel('./export/translate-zuzan-website.xlsx')


if __name__ == '__main__':
    main()
