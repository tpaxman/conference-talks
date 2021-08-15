
# DOWNLOAD BASE DATA
data/lds-scriptures.csv : src/download_scripture_references.py
	python $^ $@

data/general-conference-talk-references.txt : src/download_general_conference_citations.py
	python $^ $@
