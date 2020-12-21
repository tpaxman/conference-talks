"""
Downloads a file from a url in chunks
"""
import requests
import sys

# requires command line inputs for (1) the output file location and (2) the zip file data source
(output_file, url) = sys.argv[1:]

# get the file from its url
response = requests.get(url)

# write it in chunks (in case it's big)
with open(output_file, 'wb') as f:
    for chunk in response.iter_content(chunk_size=8192):
        f.write(chunk)
