from flask import Flask, render_template, request
app = Flask(__name__)
@app.route('/account_info', methods=['GET', 'POST'])
def account_info():
    if request.method == 'POST':
        role = request.form['role']
        if role == 'student':
            year = request.form['year']
            major = request.form['major']
        else:
            teaching_field = request.form['teaching-field']
        # Save or process the data as needed
        # ...
    return render_template('account_info.html')

# if __name__ == "__main__":
#     app.run(debug=True)
