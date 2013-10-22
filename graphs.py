import vincent
import csv
import pandas as pd
import numpy as np

x = open('results.csv')
reader = csv.reader(x)

scores = {}

for row in reader:
	scores[row[0]] = [row[1], row[2], row[3], row[4], row[5],row[6]]
	
df = pd.DataFrame(scores, index=range(1,7))


line = vincent.Line(df)
line.axis_titles(x='WEEKS', y='SCORE')
line.legend(title='Player')
line.to_json('line.html',html_out=True,html_path='line_template.html')

