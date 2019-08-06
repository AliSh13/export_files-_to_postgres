from flask import Flask, make_response, request, render_template
import main

app = Flask(__name__)


@app.route('/')
def form():
    return render_template('form.html')

@app.route('/transform', methods=["POST"])
def transform_view():
    path_to_file = request.files['data_file']
    format = request.form['format']
    table_name = request.form['table_name']
    index = False
    if request.form.get('index'):
        index = True
    sheet = 1
    if request.form.get('sheet'):
        sheet = int(request.form['sheet'])
    columns_names = []
    if request.form.get('columns_names'):
        names = request.form['columns_names']
        columns_names = names.split(',')
    rename_column = {}
    if request.form.get('rename_column'):
        rename_column = {request.form['rename_column']}
    if not path_to_file:
        return "No file"

    main.main(path_to_file, format, table_name, index, sheet,
             columns_names, rename_column)
    return render_template('form.html')

if __name__ == '__main__':
    app.run(debug=True)
