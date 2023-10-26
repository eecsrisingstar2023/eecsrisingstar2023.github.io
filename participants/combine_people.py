import os
import re

def sorted_alphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(data, key=alphanum_key)

dir_lists = os.listdir('./all/')
dir_lists = sorted_alphanumeric(dir_lists)
print(dir_lists)

all_html = []
for i, dir in enumerate(dir_lists):
    path = os.path.join('./all/', dir)
    html = open(path, 'r')
    all_html.append(html.read())

if os.path.exists('combine.html'):
    os.remove('combine.html')

with open('combine.html', 'a') as f:
    for html in all_html:
        f.write(str(html)+'\n')
f.close()