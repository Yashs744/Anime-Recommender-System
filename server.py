# Libraries (or Modules)
from flask import render_template
import connexion
import pandas as pd

# Application Interface
app = connexion.App(__name__, specification_dir = './')

# Read the 'swagger.yml' configuration file.
app.add_api('swagger.yml')

# Read the Dataset
df = pd.read_csv('data/cleaned_anime_data.csv', usecols = ['Anime_ID', 'Title'])

# URL Route to the Application at '/' i.e root
@app.route('/')
def home():
	'''
		return:
			Renders HTML Page ('home.html')
	'''
	return render_template('home.html')

# URL Route to the Application at '/availablle_anime'
@app.route('/available_animes')
def available_animes():
	'''
		return:
			Renders HTML Page ('home.html')
	'''
	with pd.option_context('display.max_colwidth', -1):
		output_html = df.to_html(na_rep = "")

	output_html = output_html.replace('<table border="1" class="dataframe">', '<table class = "table table-bordered">')
	output_html = output_html.replace('<thead>', '<thead class = "thead-dark">')
	output_html = output_html.replace('<tr style="text-align: right;">', '<tr>')
	output_html = output_html.replace('<th></th>', '<th>#</th>')

	return render_template('animes.html', tables=[output_html])

@app.route('/404')
def not_found():
	return render_template('404.html')

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8000, debug=True)
