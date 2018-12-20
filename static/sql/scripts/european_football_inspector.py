import chardet
import logging
import os
import pandas as pd
import sys as sys


def main(argv=None):
	"""
	Utilize Pandas library to read meta_movie.csv file
	:param argv:
	:return:
	"""

	if argv is None:
		argv = sys.argv

	msg = [
		'Player source file encoding detected = {0}',
		'Player source file trimmed version written to file {0}',
		'Player_Attr source file encoding detected = {0}',
		'Player_Attr source file trimmed version written to file {0}',
		'Team_Attr source file encoding detected = {0}',
		'Team_Attr source file trimmed version written to file {0}',
		'Match source file encoding detected = {0}',
		'Match source file trimmed version written to file {0}'
	]

	# Setting logging format and default level
	logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)

	# Check source file encoding
	player_in = os.path.join('csv', 'Player.csv')
	encoding = find_encoding(player_in)
	logging.info(msg[0].format(encoding))

	# Read in source with correct encoding and remove whitespace.
	players = read_csv(player_in, encoding, ',')
	players_trimmed = trim_columns(players)

	attributes = extract_filtered_series(players_trimmed,
		[
			'player_name',
			'birthday',
			'height',
			'weight',
			'player_api_id'
		]
	)
	attributess_out = os.path.join('output', 'players_trimmed.csv')
	write_series_to_csv(attributes, attributess_out, ',', False)
	logging.info(msg[1].format(os.path.abspath(attributess_out)))

	# Check source file encoding
	attr_in = os.path.join('csv', 'Player_Attributes.csv')
	encoding = find_encoding(attr_in)
	logging.info(msg[2].format(encoding))

	# Read in source with correct encoding and remove whitespace.
	player_attrs = read_csv(attr_in, encoding, ',')
	player_attrs_trimmed = trim_columns(player_attrs)

	all_attrs = extract_filtered_series(player_attrs_trimmed,
		[
			'player_api_id',
			'overall_rating',
			'potential',
			'preferred_foot',
			'crossing',
			'finishing',
			'heading_accuracy',
			'short_passing',
			'volleys',
			'marking',
			'standing_tackle',
			'sliding_tackle',
			'gk_diving',
			'gk_handling',
			'gk_kicking',
			'gk_positioning',
			'gk_reflexes'
		]
	)
	all_attrs_out = os.path.join('output', 'players_attrs_trimmed.csv')
	write_series_to_csv(all_attrs, all_attrs_out, ',', False)
	logging.info(msg[3].format(os.path.abspath(all_attrs_out)))

	# Check source file encoding
	attr_in = os.path.join('csv', 'Team_Attributes.csv')
	encoding = find_encoding(attr_in)
	logging.info(msg[4].format(encoding))

	# Read in source with correct encoding and remove whitespace.
	player_attrs = read_csv(attr_in, encoding, ',')
	player_attrs_trimmed = trim_columns(player_attrs)

	all_attrs = extract_filtered_series(player_attrs_trimmed,
		[
			'team_api_id',
			'buildUpPlaySpeed',
			'buildUpPlayPassing',
			'chanceCreationPassing',
			'chanceCreationCrossing',
			'chanceCreationShooting',
			'defencePressure',
			'defenceAggression',
			'defenceTeamWidth'
		]
	)
	all_attrs_out = os.path.join('output', 'team_attrs_trimmed.csv')
	write_series_to_csv(all_attrs, all_attrs_out, ',', False)
	logging.info(msg[5].format(os.path.abspath(all_attrs_out)))

	# Check source file encoding
	attr_in = os.path.join('csv', 'Match.csv')
	encoding = find_encoding(attr_in)
	logging.info(msg[6].format(encoding))

	# Read in source with correct encoding and remove whitespace.
	player_attrs = read_csv(attr_in, encoding, ',')
	player_attrs_trimmed = trim_columns(player_attrs)

	all_attrs = extract_filtered_series(player_attrs_trimmed,
		[
			'id',
			'season',
			'date',
			'home_team_goal',
			'away_team_goal'
		]
	)
	all_attrs_out = os.path.join('output', 'match_trimmed.csv')
	write_series_to_csv(all_attrs, all_attrs_out, ',', False)
	logging.info(msg[7].format(os.path.abspath(all_attrs_out)))

	all_attrs = extract_filtered_series(player_attrs_trimmed,
		[
			'id',
			'home_team_api_id',
			'away_team_api_id',
			'home_player_1',
			'home_player_2',
			'home_player_3',
			'home_player_4',
			'home_player_5',
			'home_player_6',
			'home_player_7',
			'home_player_8',
			'home_player_9',
			'home_player_10',
			'home_player_11',
			'away_player_1',
			'away_player_2',
			'away_player_3',
			'away_player_4',
			'away_player_5',
			'away_player_6',
			'away_player_7',
			'away_player_8',
			'away_player_9',
			'away_player_10',
			'away_player_11'
		]
	)
	all_attrs_out = os.path.join('output', 'match_squad_trimmed.csv')
	write_series_to_csv(all_attrs, all_attrs_out, ',', False)
	logging.info(msg[7].format(os.path.abspath(all_attrs_out)))



def extract_filtered_series(data_frame, column_list, drop_rule='all'):
	"""
	Returns a filtered Panda Series one-dimensional ndarray from a targeted column.
	Duplicate values and NaN or blank values are dropped from the result set which is
	returned sorted (ascending).
	:param data_frame: Pandas DataFrame
	:param column_list: list of columns
	:param drop_rule: dropna rule
	:return: Panda Series one-dimensional ndarray
	"""

	return data_frame[column_list].drop_duplicates().dropna(axis=0, how=drop_rule).sort_values(
		column_list)
	# return data_frame[column_list].str.strip().drop_duplicates().dropna().sort_values()


def find_encoding(fname):
	r_file = open(fname, 'rb').read()
	result = chardet.detect(r_file)
	charenc = result['encoding']
	return charenc


def read_csv(path, encoding, delimiter=','):
	"""
	Utilize Pandas to read in *.csv file.
	:param path: file path
	:param delimiter: field delimiter
	:return: Pandas DataFrame
	"""

	# UnicodeDecodeError: 'utf-8' codec can't decode byte 0x96 in position 450: invalid start byte
	# return pd.read_csv(path, sep=delimiter, encoding='utf-8', engine='python')

	return pd.read_csv(path, sep=delimiter, encoding=encoding, engine='python')
	# return pd.read_csv(path, sep=delimiter, engine='python')


def trim_columns(data_frame):
	"""
	:param data_frame:
	:return: trimmed data frame
	"""

	trim = lambda x: x.strip() if type(x) is str else x
	return data_frame.applymap(trim)


def write_series_to_csv(series, path, delimiter=',', row_name=True):
	"""
	Write Pandas DataFrame to a *.csv file.
	:param series: Pandas one dimensional ndarray
	:param path: file path
	:param delimiter: field delimiter
	:param row_name: include row name boolean
	"""

	series.to_csv(path, sep=delimiter, index=row_name)


if __name__ == '__main__':
	sys.exit(main())