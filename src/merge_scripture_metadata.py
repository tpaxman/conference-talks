import sys
import pandas as pd


def main():
    (citations_table_filepath, scriptures_table_filepath, outputfilename) = sys.argv[1:]
    citations_table = pd.read_csv(citations_table_filepath)
    scriptures_table = pd.read_csv(scriptures_table_filepath)
    final_view = citations_table.merge(scriptures_table, how='left',
                                       on=['book_short_title', 'chapter_number', 'verse_number'])
    final_view = final_view[['verse_title', 'book_title', 'volume_title', 'chapter_number', 'verse_number',
                             'scripture_text', 'talk_speaker', 'talk_year', 'talk_session', 'talk_title',
                             'volume_id', 'book_id', 'chapter_id', 'verse_id']]
    final_view.to_csv(outputfilename, index=False)


if __name__ == '__main__':
    main()
