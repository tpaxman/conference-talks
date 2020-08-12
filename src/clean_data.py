import json
import pandas as pd
import re

# USE THIS: https://pypi.org/project/python-scriptures/
# USE THIS: https://github.com/eliranwong/bible-verse-parser/blob/master/BibleBooks.py



def read_citation_data(talknum):
    with open(f'data/talk_{talknum}.json', 'r', encoding='utf-8') as f:
        print(f'loaded-{talknum}')
        return json.load(f)

citation_data = [read_citation_data(x) for x in range(1, 8460) if x not in range(1825, 2000)]

df = pd.DataFrame(citation_data)
df_ex = df.explode('citations')
df_ex = df_ex.dropna()
df_ex['book'] = [re.sub(r'((\d+\s)?[\w|&]+\.?)\s\d+:?.*', r'\1', x) for x in df_ex.citations]

