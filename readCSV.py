import pandas as pd
import vincent
import csv



scores = {'player': scores}

for row in scorefile:
	scores[row[0]] = [row[1]:]
	

df = pd.read_csv('weekscores.csv', index_col=0)

# line graph

lines = vincent.Line(df)
# print lines.data[0].values[0]


lines.axis_titles(x='WEEKS', y='SCORE')
lines.legend(title='Player')
lines.to_json('line.html',html_out=True,html_path='line_template.html')

# stacked bar

stack = vincent.StackedBar(df)

stack.to_json('stack.html', html_out=True, html_path='stack_template.html')
