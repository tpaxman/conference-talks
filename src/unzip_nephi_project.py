import sys
import zipfile

input_file = 'output/raw-nephi-project-data.zip'
output_dir = 'output'

(input_file, output_dir) = sys.argv[1:]
with zipfile.ZipFile(input_file, 'r') as z:
    z.extractall(output_dir)