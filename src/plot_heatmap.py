import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

data = pd.read_csv('data/citations-clean.csv')
scrips = pd.read_csv('data/lds-scriptures.csv')


def get_num_refs_for_speaker(data, speaker, column_to_count):
    new_count_name = rename_count_column(column_to_count)
    return (data
            .query(f"talk_speaker == '{speaker}'")
            .value_counts(column_to_count)
            .rename(new_count_name)
            .reset_index())


def merge_num_refs_to_scrips(num_refs, scrips, column_to_merge, column_to_display, column_to_plot):
    scrips_unique = scrips[[column_to_display, column_to_merge]].drop_duplicates()
    m = scrips_unique.merge(num_refs, on=column_to_merge, how='left').fillna({column_to_plot: 0})
    plot_data = m.sort_values(column_to_merge).set_index(column_to_display)[column_to_plot].to_frame()
    return plot_data


def rename_count_column(column_name):
    return column_name + '_count'


num_refs = get_num_refs_for_speaker(data=data, speaker='David A. Bednar', column_to_count='verse_id')
plot_data = merge_num_refs_to_scrips(num_refs=num_refs, scrips=scrips, column_to_merge='verse_id',
                                     column_to_display='verse_title', column_to_plot='verse_id_count')

scrips['chapter_title'] = scrips.book_title + ' ' + scrips.chapter_number.astype(str)

def make_a_plot(data, scrips, speaker, col_to_count, col_to_display, cmap):
    fig = plt.figure()
    col_to_plot = rename_count_column(col_to_count)
    num_refs = get_num_refs_for_speaker(data=data, speaker=speaker, column_to_count=col_to_count)
    plot_data = merge_num_refs_to_scrips(num_refs=num_refs, scrips=scrips, column_to_merge=col_to_count,
                                         column_to_display=col_to_display, column_to_plot=col_to_plot)
    g = sns.heatmap(plot_data, cmap=cmap, xticklabels=True, yticklabels=True).set_title(speaker)
    return g

def easy_plot(speaker, level):
    make_a_plot(data=data, scrips=scrips, speaker=speaker, col_to_count=level+'_id', col_to_display=level+'_title', cmap='Reds')

def easy_volume_plot(speaker):
    easy_plot(speaker=speaker, level='volume')

def easy_book_plot(speaker):
    easy_plot(speaker=speaker, level='book')
