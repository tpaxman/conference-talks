import sys
import pandas as pd


def main():
    (citations_table_filepath, scriptures_table_filepath, outputfilename) = sys.argv[1:]
    citations_table = pd.read_csv(citations_table_filepath)
    books_table = import_books_metadata(scriptures_table_filepath)
    full_table = add_books_details_to_citations(citations_table, books_table)
    columns_order = ['volume_id', 'book_id', 'volume_title', 'book_title', 'chapter', 'verse', 'speaker', 'year', 'month', 'talk_title']
    final_table = full_table[columns_order]
    final_table.to_csv(outputfilename, index=False)


def import_books_metadata(scriptures_table_filepath: str) -> pd.DataFrame:
    df = pd.read_csv(scriptures_table_filepath)
    df = df[['book_short_title', 'book_id', 'book_title', 'volume_id', 'volume_title']]
    df = df.drop_duplicates()
    df = df.reset_index(drop=True)
    return df


def add_books_details_to_citations(citations_table: pd.DataFrame, books_table: pd.DataFrame) -> pd.DataFrame:
    citations_table['book_short_title'] = citations_table.book_name.replace(
        {"JS—H": "JS-H", "JS—M": "JS-M", "Song": "Song."})
    full_table = citations_table.merge(books_table)
    return full_table


if __name__ == '__main__':
    main()
