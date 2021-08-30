
# DOWNLOAD BASE DATA
data/lds-scriptures.csv : src/download_scripture_references.py
	python $^ $@

data/general-conference-talk-references.txt : src/download_general_conference_citations.py
	python $^ $@

data/general-conference-talk-references.csv : src/parse_text.py data/general-conference-talk-references.txt
	python $^ $@

data/citations-clean.csv : src/merge_scripture_metadata.py data/general-conference-talk-references.csv data/lds-scriptures.csv
	python $^ $@

data/presidents.csv : src/import_presidents_data.py
	python $^ $@
