output/lds-scriptures.csv : src/download_lds_scriptures_raw_data.py
	python $< $@ https://raw.githubusercontent.com/beandog/lds-scriptures/master/csv/lds-scriptures.csv

