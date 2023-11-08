import pickle
import os
from Tag import Tag
import shutil
import cv2

with open("people", 'rb') as fp:
    people = pickle.load(fp)

all_names = []
all_names_print = []


# record names

for item in people:
    name = item["name"].split(", ")
    name.reverse()
    name_dir ="_".join(i for i in name)
    name_print = " ".join(i for i in name)
    isDir = os.path.isdir(name_dir)
    if not isDir:
        os.mkdir(name_dir)
    all_names.append(name_dir)
    all_names_print.append(name_print)

# record ids

all_ids = os.listdir("../images/Headshot")

# index

if not os.path.isdir("all"):
    os.mkdir('all')
else:
    shutil.rmtree('all')
    os.mkdir('all')

for i, name in enumerate(all_names):
    print(i, name)
    id = people[i]['id']

    # print(id)

    correct_id = None
    for _id in all_ids:
        if _id.startswith(id):
            correct_id = _id

    # print(correct_id)

    if correct_id.endswith(".jp2"):
        # print(correct_id)
        url = "../images/Headshot/" + correct_id
        new_url = url[:-4] + ".png"
        image = cv2.imread(url)
        cv2.imwrite(new_url, image)
        correct_id = correct_id[:-4] + ".png"

    if " " in correct_id:
        correct_id = correct_id.split(" ")
        correct_id ="\ ".join(i for i in correct_id)

    if "(" in correct_id:
        correct_id = correct_id.split("(")
        correct_id ="\(".join(i for i in correct_id)

    if ")" in correct_id:
        correct_id = correct_id.split(")")
        correct_id ="\)".join(i for i in correct_id)

    ## make a joint index

    with Tag('li') as li:
        with Tag('a', attrib={'class': 'visually-hidden', 'href': '/participants/'+str(all_names[i])}) as a:
            a.text = all_names_print[i]
        with Tag('a', attrib={'class': 'speaker', 'href': '/participants/'+str(all_names[i])}) as a:
            with Tag('div', attrib={'role': 'presentation', 'class': 'speaker-img', 'style': 'background-image: url(/images/Headshot/{});'.format(correct_id)}) as div:
                div.text=""
            with Tag('div', attrib={'class': 'info'}):
                with Tag('strong', attrib={'class': 'speaker-name'}) as strong:
                    strong.text = all_names_print[i]
                with Tag('div', attrib={'class': 'speaker-company'}) as div:
                    div.text = people[i]['institute']
                with Tag('span', attrib={'class': 'speaker-company'}) as span:
                    span.text = people[i]['area']

    li.write('all/{}.html'.format(str(name)))

    ## for each people, make a separate folder

    with Tag('main') as main:
        with Tag('div', attrib={'class': 'hero'}):
            with Tag('br') as br:
                br.text = ""
            with Tag('br') as br:
                br.text = ""
            with Tag('header'):
                with Tag('div', attrib={'class': 'speaker-img', 'style': 'background-image: url(/images/Headshot/{});'.format(correct_id)}) as div:
                    div.text=""
                with Tag('div'):
                    with Tag('h1') as h1:
                        h1.text = all_names_print[i]
                    with Tag('ul', attrib={'class': 'socials'}):
                        with Tag('li') as li:
                            with Tag('b') as b:
                                b.text = 'Position: '
                            with Tag('a') as a:
                                a.text = people[i]['position'] + "   "
                            with Tag('b') as b:
                                b.text = 'Institution: '
                            with Tag('a') as a:
                                a.text = people[i]['institute']
        with Tag('section', attrib={'class': 'speaker'}):
            with Tag('header'):
                with Tag('h2'):
                    with Tag('b') as b:
                        b.text = people[i]['title']
            with Tag('div', attrib={'classs': 'hero'}):
                with Tag('br') as br:
                    br.text = ""
                with Tag('h3', attrib={'id': 'eligibility'}):
                    with Tag('b') as b:
                        b.text = 'Research Abstract:'
                with Tag('p') as p:
                    p.text = people[i]['research']
                with Tag('h3', attrib={'id': 'eligibility'}):
                    with Tag('b') as b:
                        b.text = 'Bio:'
                with Tag('p') as p:
                    p.text = people[i]['bio']
    main.write('temp.html')

    folder_index = "{}/index.html".format(name)
    with open(folder_index, 'w') as f:
        header = open('header.html', 'r').read()
        main = open('temp.html', 'r').read()
        footer = open('footer.html', 'r').read()
        f.write(str(header)+'\n'+str(main)+'\n'+str(footer))
    f.close() 