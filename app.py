from flask import Flask, render_template, request, jsonify, session
from flask_debugtoolbar import DebugToolbarExtension
from boggle import Boggle
import random

app = Flask(__name__)

app.config['SECRET_KEY'] = "maybemabeline"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

boggle_game = Boggle()


@app.route('/')
def index():
    """
    Renders the main game page with a new Boggle board.

    Returns:
        rendered_template (str): The HTML content of the game page.
    """

    board = boggle_game.make_board()
    session['board'] = board
    return render_template('index.html', board=board)


total_plays = 0
highest_score = 0


@app.route('/check_word', methods=['POST'])
def check_word():
    """
    Checks if a submitted word is valid and present on the Boggle board.

    Args:
        None (uses data from AJAX request).

    Returns:
        JSON response indicating if the word is valid or not.
    """

    word = request.json['word'].upper()
    board = session['board']

    is_valid = boggle_game.check_valid_word(board, word)

    global total_plays, highest_score

    if is_valid:
        score = len(word)
        total_plays += 1
        if score > highest_score:
            highest_score = score

        return jsonify({"result": "ok", "score": score})
    else:
        return jsonify({"result": "not-on-board"})


@app.route('/update_stats', methods=['POST'])
def update_stats():
    """
    Updates the game statistics such as total plays and highest score.

    Args:
        None (uses data from AJAX request).

    Returns:
        JSON response confirming that the statistics have been updated.
    """

    global total_plays, highest_score

    score = request.json['score']
    total_plays += 1
    if score > highest_score:
        highest_score = score

    return jsonify({"result": "ok", "total_plays": total_plays, "highest_score": highest_score})
