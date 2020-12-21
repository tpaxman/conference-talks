
# MAIN MAKE COMMANDS ========================================================================
.PHONY = rawdata
rawdata : output/lds-scriptures.csv output/book-ids.csv


# 1. DOWNLOAD THE RAW DATA ====================================================================

output/lds-scriptures.csv : src/download_url_file.py
	python $< $@ https://raw.githubusercontent.com/beandog/lds-scriptures/master/csv/lds-scriptures.csv

output/book-ids.csv : src/get_book_ids.py
	python $< $@
