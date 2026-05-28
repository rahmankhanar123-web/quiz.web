from flask import Flask, render_template, request

app = Flask(__name__)

quiz = [
    {
        "question": "What is the capital of India?",
        "options": ["Delhi", "Mumbai", "Chennai", "Kolkata"],
        "answer": "Delhi"
    },
    {
        "question": "Which planet is called the Red Planet?",
        "options": ["Earth", "Mars", "Jupiter", "Venus"],
        "answer": "Mars"
    },
    {
        "question": "Who invented Python?",
        "options": [
            "Guido van Rossum",
            "Elon Musk",
            "Bill Gates",
            "Mark Zuckerberg"
        ],
        "answer": "Guido van Rossum"
    }
]

@app.route('/')
def home():
    return render_template('index.html', quiz=quiz)

@app.route('/submit', methods=['POST'])
def submit():

    score = 0

    for q in quiz:

        user_answer = request.form.get(q["question"])

        if user_answer == q["answer"]:
            score += 1

    return render_template(
        'result.html',
        score=score,
        total=len(quiz)
    )
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)