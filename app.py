from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Ensure upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

SUBJECT_CODES = ['201', '202', '203', '204', '251', '252']
MAX_THEORY_MARKS = {'201': 75, '202': 75, '203': 75, '204': 75, '251': 50, '252': 50}
MAX_PRACTICAL_MARKS = {'201': 25, '202': 25, '203': 25, '204': 25, '251': 50, '252': 50}

def calculate_percentage_and_sgpa(marks):
    total_obtained = sum(marks.values())
    total_max = sum(MAX_THEORY_MARKS[code] + MAX_PRACTICAL_MARKS[code] for code in SUBJECT_CODES)
    percentage = (total_obtained / total_max) * 100

    # Simple SGPA calculation: Assuming SGPA out of 9.5, scaled from percentage
    sgpa = (percentage / 9.5)
    
    return round(percentage, 2), round(sgpa, 2)

@app.route('/', methods=['GET', 'POST'])
def index():
    error = None
    if request.method == 'POST':
        marks = {}
        for code in SUBJECT_CODES:
            theory_mark = request.form.get(f'theory_{code}', type=float, default=0)
            practical_mark = request.form.get(f'practical_{code}', type=float, default=0)
            # Validate marks within range
            if theory_mark < 0 or theory_mark > MAX_THEORY_MARKS[code]:
                error = f"Invalid theory marks for subject {code}. Max is {MAX_THEORY_MARKS[code]}."
                break
            if practical_mark < 0 or practical_mark > MAX_PRACTICAL_MARKS[code]:
                error = f"Invalid practical marks for subject {code}. Max is {MAX_PRACTICAL_MARKS[code]}."
                break
            marks[code+'_theory'] = theory_mark
            marks[code+'_practical'] = practical_mark

        if not error:
            percentage, sgpa = calculate_percentage_and_sgpa(marks)
            return render_template('result.html', percentage=percentage, sgpa=sgpa)

    return render_template('index.html', subject_codes=SUBJECT_CODES, max_theory=MAX_THEORY_MARKS, max_practical=MAX_PRACTICAL_MARKS, error=error)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'photo' not in request.files:
            return "No file part", 400
        file = request.files['photo']
        if file.filename == '':
            return "No selected file", 400
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        # Placeholder for AI analysis of the photo
        analysis_result = "Photo analysis feature coming soon."
        return render_template('upload_result.html', result=analysis_result)
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)
