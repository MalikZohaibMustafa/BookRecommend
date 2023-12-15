import pandas as pd
import numpy as np
import pickle
from flask import Flask, render_template, request, redirect, url_for
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

# Load the pickled 'score' and 'table' data
with open('score.pkl', 'rb') as score_file:
    score = pickle.load(score_file)

with open('table.pkl', 'rb') as table_file:
    table = pickle.load(table_file)

def book_ML(name):
    recommendation = []
    index = np.where(table.index == name)[0][0]
    dis = sorted(list(enumerate(score[index])), key=lambda x: x[1], reverse=True)[1:10]
    for i in dis:
        recommendation.append(table.index[i[0]])
    return recommendation


@app.route('/recommendations/<book_title>', methods=['GET'])
def recommendations(book_title):
    recommendations = book_ML(book_title)
    return {"recommendations": recommendations, "user_input": book_title}

    return render_template('recommendations.html', book_title=book_title, recommendations=recommendations)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
