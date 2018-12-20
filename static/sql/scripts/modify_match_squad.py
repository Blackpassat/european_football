import csv
import sys,os

file2 = open('./output/match_squad_modified.csv', 'w')

match_id = []
home_team = []
away_team = []
player = []
with open('./output/match_squad_trimmed.csv') as csv_file:
	csv_reader = csv.reader(csv_file, delimiter=',')
	next(csv_reader, None)
	for row in csv_reader:
		match_id.append(row[0])
		home_team.append(row[1])
		away_team.append(row[2])
		for i in range(22):
			player.append(row[3+i])

with open('./output/match_squad_modified.csv', mode='w') as csv_file:
	csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	for i in range(len(match_id)):

		for j in range(11):
			csv_writer.writerow([match_id[i], home_team[i], '1', player[i*22+j]])
		for j in range(11):
			csv_writer.writerow([match_id[i], away_team[i], '0', player[i*22+j+11]])
