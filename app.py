from flask import Flask, render_template, request, redirect, url_for
import csv
import os

app = Flask(__name__)

# Home route
@app.route('/')
def home():
    return render_template('index.html')  # Corrected template path

# Form route: supports GET (to display) and POST (to submit)
@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        # collect form data
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        value = request.form.get('value', '').strip()
        # after POST, redirect to GET with query params so GET shows submitted data
        return redirect(url_for('form', name=name, email=email, value=value))

    # GET: fetch any submitted data from query params
    submitted = None
    if 'name' in request.args:
        submitted = {
            'name': request.args.get('name', ''),
            'email': request.args.get('email', ''),
            'value': request.args.get('value', '')
        }
    return render_template('form.html', submitted=submitted)

# Data route: reads data.csv and displays as table
@app.route('/data')
def data():
    csv_path = os.path.join(app.root_path, 'data.csv')
    rows = []
    headers = []
    try:
        with open(csv_path, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            for i, row in enumerate(reader):
                if i == 0:
                    headers = row
                else:
                    rows.append(row)
    except FileNotFoundError:
        headers = ['Error']
        rows = [['data.csv not found in project root']]

    return render_template('data.html', headers=headers, rows=rows)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)