"""
Downloads all scripture data in .zip format from the Nephi Project
"""
import requests
import sys

# requires command line inputs for (1) the output file location and (2) the zip file data source
(output_file, url) = sys.argv[1:]
response = requests.get(url)

# write it in chunks (too big otherwise)
with open(output_file, 'wb') as f:
    for chunk in response.iter_content(chunk_size=8192):
        f.write(chunk)
