from flask import Flask, request
import flask
import json
import file_buffer

app = Flask(__name__)
#A enlever => a des fins de tests en local (cors policy déclanchée car même origine)
app.config['CORS_HEADERS'] = 'Content-Type'



def filter_by_name(search_string):
    # fonction de filtre sur les titres dans les données, retourne l'objet
    data = file_buffer.get_file_data()
    ret = []
    for i in data['datas']:
        if search_string.lower() in i['title'].lower():
            ret.append(i)
    return ret 

def update_manga_data(title, new_datas):
    # Tentative non fonctionnelle de modifier le fichier json => Fonctionne pas
    content = file_buffer.get_file_data()
    for i in content['datas']:
        if i['title'] == title:
            i['list'] = new_datas['list']
            i['title'] = new_datas['title']
            i['url'] = new_datas['url']
            i['current'] = new_datas['current']
            file_buffer.save_file(content)
            return 200
    
# route principale pr tous les mangas
@app.route("/mangas", methods=["GET"])
def mangas():
    response = flask.jsonify(message=file_buffer.get_file_data())
    response.headers.add('Access-Control-Allow-Origin', "*")
    return response

# route secondaire pour rechercher par titre
@app.route('/manga/<title>', methods=["GET", "POST", "UPDATE", "DELETE"])
def manga(title):
        
    response = flask.jsonify(message=filter_by_name(title))
    response.headers.add('Access-Control-Allow-Origin', "*")
    return response

# route tertiaire pour ajouter des mangas dans la liste
@app.route('/add/manga', methods=["POST"])
def add_manga():
    data = dict(request.args)
    print("post request data: ", data)
    old_data = file_buffer.get_file_data()
    if filter_by_name(data['title']):
        response = flask.jsonify(message='Data already existing in DB, please check title.')
        return response
    else:
        old_data["datas"].append({"title": data['title'], "url": data['url'], "current": data['current']})
        file_buffer.save_file(content=old_data, filename='data2.json')
        response = flask.jsonify(message='Data added successfully')
        response.status = 200
        return response