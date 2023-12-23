import json 


def get_file_data():
    with open("data.json") as r:
        content = json.load(r)
    return content

def get_manga_data(title):
    content = get_file_data()
    for i in content['datas']:
        if i['title'] == title:
            return i
        
def save_file(content, filename):
    with open(filename, "w") as w:
        w.writelines(json.dumps(content))