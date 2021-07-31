import simplejson as json
from flask import Flask, request, Response, redirect
from flask import render_template
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor

app = Flask(__name__, template_folder="templates")
mysql = MySQL(cursorclass=DictCursor)


@app.route('/', methods=['GET'])
def index():
    user = {'username': 'Michael'}
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM mlbPlayers')
    result = cursor.fetchall()
    return render_template('index.html', title='Home', user=user, players=result)


@app.route('/view/<int:player_id>', methods=['GET'])
def record_view(player_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM mlbPlayers WHERE id=%s', player_id)
    result = cursor.fetchall()
    return render_template('view.html', title='View Form', player=result[0])


@app.route('/edit/<int:player_id>', methods=['GET'])
def form_edit_get(player_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM mlbPlayers WHERE id=%s', player_id)
    result = cursor.fetchall()
    return render_template('edit.html', title='Edit Form', player=result[0])


@app.route('/edit/<int:player_id>', methods=['POST'])
def form_update_post(player_id):
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('plName'), request.form.get('plTeam'), request.form.get('plPosition'),
                 request.form.get('plHeight'), request.form.get('plWeight'),
                 request.form.get('plAge'), player_id)
    sql_update_query = """UPDATE mlbPlayers t SET t.plName = %s, t.plTeam = %s, t.plPosition = %s, t.plHeight = 
    %s, t.plWeight = %s, t.plAge = %s WHERE t.id = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/player/new', methods=['GET'])
def form_insert_get():
    return render_template('new.html', title='New MLB Player Form')


@app.route('/player/new', methods=['POST'])
def form_insert_post():
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('plName'), request.form.get('plTeam'), request.form.get('plPosition'),
                 request.form.get('plHeight'), request.form.get('plWeight'),
                 request.form.get('plAge'))
    sql_insert_query = """INSERT INTO mlbPlayers (plName,plTeam, plPosition, plHeight, plWeight,
                        plAge) VALUES (%s,%s, %s,%s, %s,%s)"""
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/delete/<int:player_id>', methods=['POST'])
def form_delete_post(player_id):
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM mlbPlayers WHERE id = %s """
    cursor.execute(sql_delete_query, player_id)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/api/v1/players', methods=['GET'])
def api_browse() -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM mlbPlayers')
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/players/<int:player_id>', methods=['GET'])
def api_retrieve(player_id) -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM mlbPlayers WHERE id=%s', player_id)
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/players/<int:player_id>', methods=['PUT'])
def api_edit(player_id) -> str:
    cursor = mysql.get_db().cursor()
    content = request.json
    inputData = (content['plName'], content['plTeam'], content['plPosition'],
                 content['plHeight'], content['plWeight'],
                 content['plAge'], player_id)
    sql_update_query = """UPDATE mlbPlayers t SET t.plName = %s, t.plTeam = %s, t.plPosition = %s, t.plHeight = 
        %s, t.plWeight = %s, t.plAge = %s WHERE t.id = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    resp = Response(status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/players', methods=['POST'])
def api_add() -> str:

    content = request.json

    cursor = mysql.get_db().cursor()
    inputData = (content['plName'], content['plTeam'], content['plPosition'],
                 content['plHeight'], content['plWeight'],
                 content['plAge'])
    sql_insert_query = """INSERT INTO mlbPlayers (plName,plTeam, plPosition, plHeight, plWeight,
                        plAge) VALUES (%s,%s, %s,%s, %s,%s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    resp = Response(status=201, mimetype='application/json')
    return resp


@app.route('/api/v1/players/<int:player_id>', methods=['DELETE'])
def api_delete(player_id) -> str:
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM mlbPlayers WHERE id = %s """
    cursor.execute(sql_delete_query, player_id)
    mysql.get_db().commit()
    resp = Response(status=200, mimetype='application/json')
    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
