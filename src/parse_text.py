import re
import sys
import pandas as pd


def main():
    (raw_text_input_filename, clean_data_output_filename) = sys.argv[1:]
    rawtext = read_in_raw_text(raw_text_input_filename)
    df = extract_text_to_dataframe(rawtext)
    df['scripture_numbers'] = df['raw_scripture'].apply(extract_scripture_numbers_from_scripture_reference)
    df['book_name'] = df['raw_scripture'].apply(extract_book_name_from_scripture_reference)
    df['chapter'] = df['scripture_numbers'].apply(extract_chapter_from_scripture_numbers)
    df['verse_nums_list'] = df.scripture_numbers.apply(extract_verses_list_from_scripture_numbers)
    df = df.explode('verse_nums_list').rename(columns={'verse_nums_list': 'verse'})
    df['year'] = df['raw_talk_reference'].apply(extract_year_from_raw_talk_reference)
    df['month'] = df['raw_talk_reference'].apply(extract_month_from_raw_talk_reference)
    df['talk_pagenum'] = df['raw_talk_reference'].apply(extract_talk_pagenum_from_raw_talk_reference)
    df['speaker'] = df['raw_talk_reference'].apply(extract_speaker_from_raw_talk_reference)
    df = df[['book_name', 'chapter', 'verse', 'speaker', 'year', 'month', 'talk_title']]
    df.to_csv(clean_data_output_filename, index=False)


def read_in_raw_text(filename: str) -> str:
    with open(filename, 'r', encoding='utf-8') as f:
        rawtext = f.read()
    return rawtext


def extract_text_to_dataframe(rawtext: str) -> pd.DataFrame:
    lines = [a.split(' ; ') for a in rawtext.split('\n')]
    raw_column_data = [x[-4:] for x in lines]
    df = pd.DataFrame(raw_column_data, columns=['raw_scripture', 'scripture_citation_url', 'raw_talk_reference', 'talk_title'])
    df = df[df['raw_scripture'] != '']
    return df


# SCRIPTURE REFERENCE PARSING:
def parse_scripture_reference(raw_scripture: str, part_type: str) -> str:
    parts = {'book_name': '', 'scripture_numbers': ''}
    assert part_type in parts, f"part_type must be either {' or '.join(parts)}"
    if ':' in raw_scripture:
        word_chunks = raw_scripture.split()
        parts['book_name'] = ' '.join(word_chunks[:-1])
        parts['scripture_numbers'] = word_chunks[-1]
    else:
        parts['book_name'] = raw_scripture
        parts['scripture_numbers'] = ''
    return parts[part_type]


def extract_scripture_numbers_from_scripture_reference(raw_scripture: str) -> str:
    return parse_scripture_reference(raw_scripture, 'scripture_numbers')


def extract_book_name_from_scripture_reference(raw_scripture: str) -> str:
    return parse_scripture_reference(raw_scripture, 'book_name')


def extract_chapter_from_scripture_numbers(scripture_numbers: str) -> int:
    if scripture_numbers:
        chapter = int(scripture_numbers.split(':')[0])
    else:
        chapter = 1
    return chapter


def extract_verses_list_from_scripture_numbers(scripture_numbers: str) -> list:
    if scripture_numbers:
        rawverses = scripture_numbers.split(':')[-1]
        comma_split = rawverses.split(',')
        clean_nums = []
        for x in comma_split:
            hyphen_split = x.split('-')
            if len(hyphen_split) == 1:
                num = [int(x)]
            else:
                num = list(range(int(hyphen_split[0]), int(hyphen_split[1]) + 1))
            clean_nums.append(num)
        flat_list = [item for sublist in clean_nums for item in sublist]
        return flat_list
    else:
        return [1]


# TALK REFERENCE PARSING
def extract_year_from_raw_talk_reference(raw_talk_reference: str) -> int:
    year_string = re.sub(r'^(\d{4}).*', r'\1', raw_talk_reference)
    year = int(year_string)
    return year


def extract_month_from_raw_talk_reference(raw_talk_reference: str) -> str:
    month_initial = re.sub(r'^\d{4}-([O|A]).*', r'\1', raw_talk_reference)
    return month_initial


def extract_talk_pagenum_from_raw_talk_reference(raw_talk_reference: str) -> int:
    pagenum_str = re.sub(r'^\d{4}-[O|A]:(\d+).*', r'\1', raw_talk_reference)
    pagenum = int(pagenum_str)
    return pagenum


def extract_speaker_from_raw_talk_reference(raw_talk_reference: str) -> str:
    talk_reference_parts = raw_talk_reference.split(', ', maxsplit=1)
    speaker = talk_reference_parts[-1]
    return speaker


if __name__ == '__main__':
    main()
