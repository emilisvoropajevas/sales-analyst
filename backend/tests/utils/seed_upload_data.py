from io import BytesIO
import json
#3 files -> file size too big, wrong content type, -> returns formatted file

#Big file 1 byte over 5Mb
big_file = BytesIO(b"x" * (5 * 1024 * 1024 + 1))

json_file = json.dumps('{"hello": "i", "am": "the", "wrong": "file", "file": "type"}').encode("utf-8")
# .txt file for wrong content type

# Test CSV file