from flask import render_template
from . import genreTop

@genTop.route('/genres/<genre>')
def genre(genre):
    # here pass apprioprate list of game
    return render_template('genreTop.html', genre = genre), 200#then put here game_dict
    #with jinja loop you will unpack games to tags
