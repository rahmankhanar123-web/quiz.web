from flask import Flask, render_template, request

app = Flask(__name__)

# YOUR DATA SOURCE
quiz_data = [
    {"question": "What is the capital of India?", "options": ["Delhi", "Mumbai", "Chennai", "Kolkata"], "answer": "Delhi"},
    {"question": "Which planet is called the Red Planet?", "options": ["Earth", "Mars", "Jupiter", "Venus"], "answer": "Mars"},
    {"question": "Who invented Python?", "options": ["Guido van Rossum", "Elon Musk", "Bill Gates", "Mark Zuckerberg"], "answer": "Guido van Rossum"}
]

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/quiz')
def quiz_page():
    return render_template('index.html', quiz=quiz_data)

@app.route('/submit', methods=['POST'])
def submit():
    score = 0
    results = []
    
    # Get the time remaining from the hidden input in index.html
    try:
        time_left = int(request.form.get('time_remaining', 0))
    except:
        time_left = 0

    for i, q in enumerate(quiz_data):
        user_answer = request.form.get(str(i))
        is_correct = (user_answer == q["answer"])
        if is_correct:
            score += 1
        
        results.append({
            "question": q["question"],
            "all_options": q["options"],
            "user_answer": user_answer,
            "correct_answer": q["answer"],
            "is_correct": is_correct
        })

    # DYNAMIC PERFORMANCE COMMENTS
    if score == len(quiz_data) and time_left >= 15:
        performance_comment = "⚡ BLAZING! You're a Galaxy Genius!"
    elif score == len(quiz_data):
        performance_comment = "🌟 PERFECT! All targets neutralized."
    elif score >= (len(quiz_data) / 2):
        performance_comment = "👍 GOOD JOB! Mission Accomplished."
    else:
        performance_comment = "👨‍🚀 NEEDS IMPROVEMENT. Back to the academy!"

    return render_template('result.html', 
                           score=score, 
                           total=len(quiz_data), 
                           results=results, 
                           comment=performance_comment, 
                           time_left=time_left)

if __name__ == '__main__':
    app.run(debug=True)