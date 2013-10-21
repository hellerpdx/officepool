import vincent
import csv
import pandas as pd
import numpy as np

x = open('results.csv')
reader = csv.reader(x)

names = []
week1 = []
week2 = []
week3 = []
week4 = []
week5 = []
week6 = []
scores = {}

for row in reader:
	# names.append(row[0])
	# week1.append(row[1])
	# week2.append(row[2])
	# week3.append(row[3])
	# week4.append(row[4])
	# week5.append(row[5])
	# week6.append(row[6])
	scores[row[0]] = [row[1], row[2], row[3], row[4], row[5],row[6]]
	
#Dicts of iterables
# scores1 = {'Bob':[65,87,43],'Joe':[4,98,64],'Mary':[55,87,9]}
# 
df = pd.DataFrame(scores, index=range(1,7))


line = vincent.Line(df)
line.axis_titles(x='WEEKS', y='SCORE')
line.legend(title='Player')
line.to_json('line.html',html_out=True,html_path='line_template.html')

