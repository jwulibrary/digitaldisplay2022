from app import app

from flask import render_template, jsonify

from app import tools


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html',
                           hours=tools.get_hours(),
                           book=tools.get_book(),
                           announcement=tools.get_announcement(),
                           database=tools.get_database(),
                           poster_img=tools.get_poster(),
                            poster_img2=tools.get_poster2()
                            # video=tools.get_video()
                            )



@app.route('/messages/<libraryname>')
def make_message(libraryname):
    message = tools.get_message(libraryname)
    return jsonify(message)



@app.route('/books')
def make_book():
    book = tools.get_book()
    return jsonify(book)

@app.route('/databases')
def make_database():
    database = tools.get_database()
    return jsonify(database)


@app.route('/posters')
def make_poster():
    poster = tools.get_poster()
    return jsonify(poster)


@app.route('/posters2')
def make_poster2():
    poster = tools.get_poster2()
    return jsonify(poster)







# @app.route('/databases2')
# def make_database2():
#     database = tools.get_database2()
#     return jsonify(database)
