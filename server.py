from flask import Flask, jsonify, request, abort
from flask_cors import CORS, cross_origin
from courseDAO import courseDAO

app = Flask(__name__, static_url_path='', static_folder='.')
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
@cross_origin()
def index():
    return "Welcome to the Course API!"

@app.route('/courses')
@cross_origin()
def getAll():
    results = courseDAO.getAll()
    return jsonify(results)

@app.route('/courses/<int:id>')
@cross_origin()
def findById(id):
    foundCourse = courseDAO.findByID(id)
    return jsonify(foundCourse)

@app.route('/courses', methods=['POST'])
@cross_origin()
def create():
    if not request.json:
        abort(400)
    course = {
        "CourseName": request.json['CourseName'],
        "StudentName": request.json['StudentName'],
        "Duration": request.json['Duration'],
    }
    added = courseDAO.create(course)      # call DAO to add course
    return jsonify(added)

@app.route('/courses/<int:id>', methods=['PUT'])
@cross_origin()
def update(id):
    try:
        found = courseDAO.findByID(id)
        if not found:
            abort(404)
        if not request.json:
            abort(400)
        reqJson = request.json
        
        if 'Duration' in reqJson:
            try:
                reqJson['Duration'] = int(reqJson['Duration'])  # change to int
            except ValueError:
                abort(400)

        if 'CourseName' in reqJson:
            found['CourseName'] = reqJson['CourseName']
        if 'StudentName' in reqJson:
            found['StudentName'] = reqJson['StudentName']
        if 'Duration' in reqJson:
            found['Duration'] = reqJson['Duration']

        courseDAO.update(id, found)             # call DAO to update course
        
        return jsonify(found)

    except Exception as e:
        print("Update Error:", e)  
        abort(500)

@app.route('/courses/<int:id>', methods=['DELETE'])
@cross_origin()                                       # allows to call from other domains
def delete(id):
    courseDAO.delete(id)                                # call DAO to delete
    return jsonify({"done": True})

if __name__ == '__main__':
    app.run(debug=True)
