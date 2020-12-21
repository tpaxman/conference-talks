output/lds-scriptures.csv : src/download_file_from_url.py
	python $< $@ https://raw.githubusercontent.com/beandog/lds-scriptures/master/csv/lds-scriptures.csv


'output/book_urls.csv',
