import sys
import requests
import pandas as pd


def main():
    outputfilename = sys.argv[1]
    table_columns_mapping = {'No.': 'num',
                             'Portrait': 'portrait',
                             'President of the Church': 'name',
                             'Birth': 'birth',
                             'Ordination': 'ordination',
                             'Death': 'death',
                             'Length': 'length'}

    # read in table from wikipedia
    url = "https://en.wikipedia.org/wiki/List_of_presidents_of_The_Church_of_Jesus_Christ_of_Latter-day_Saints"
    html = requests.get(url).content
    table = find_table_having_expected_columns(html, table_columns_mapping)

    # remove rows that are just description
    table = table[table['No.'].notna()]
    table = select_as(table, table_columns_mapping).drop(columns=['portrait', 'length'])

    # clean up date column where text is
    table.loc[lambda x: x['name'] == 'Joseph Smith', 'ordination'] = 'April 6, 1830'
    table.loc[lambda x: x.death.str.contains('Living'), 'death'] = ''

    # fix datatypes
    table[['birth', 'ordination', 'death']] = table[['birth', 'ordination', 'death']].apply(pd.to_datetime)
    table = table.astype({'num': int})
    table.to_csv(outputfilename, index=False)


def select_as(table: pd.DataFrame, columns_dict: dict) -> pd.DataFrame:
    assert set(columns_dict).issubset(table.columns), 'not all columns exist'
    return table.rename(columns=columns_dict).loc[:, list(columns_dict.values())]


def find_table_having_expected_columns(html, expected_columns):
    tables_list = pd.read_html(html)
    table = [x for x in tables_list if table_contains_columns(x, expected_columns)][0]
    return table


def table_contains_columns(table: pd.DataFrame, expected_columns_list: list) -> bool:
    return set(expected_columns_list).issubset(table.columns)


if __name__ == '__main__':
    main()