import logging
import os
import pandas as pd
import sys as sys


def main(argv=None):
	"""
	Utilize Pandas library to read in both UNSD M49 country and area .csv file
	(tab delimited) as well as the UNESCO heritage site .csv file (tab delimited).
	Extract regions, sub-regions, intermediate regions, country and areas, and
	other column data.  Filter out duplicate values and NaN values and sort the
	series in alphabetical order. Write out each series to a .csv file for inspection.
	"""
	if argv is None:
		argv = sys.argv

	msg = [
		'Source file read {0}',
		'artist genders written to file {0}',
		'artist places written to file {0}',
		'artist roles written to file {0}',
		'artwork units written to file {0}'
	]

	# Setting logging format and default level
	logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)

	# Read in artist (tabbed separator)
	artist_csv = 'collection/artist_data.csv'
	artist_data_frame = read_csv(artist_csv, ',')
	logging.info(msg[0].format(os.path.abspath(artist_csv)))

	# Write genders to a .csv file.
	artist_gender = extract_filtered_series(artist_data_frame, 'gender')
	artist_gender_csv = 'collection/output/artist_gender.csv'
	write_series_to_csv(artist_gender, artist_gender_csv, '\t', False)
	logging.info(msg[1].format(os.path.abspath(artist_gender_csv)))

	# Write places to a .csv file.
	artist_place1 = extract_filtered_series(artist_data_frame, 'placeOfBirth')
	artist_place2 = extract_filtered_series(artist_data_frame, 'placeOfDeath')
	artist_place = artist_place1.append(artist_place2).drop_duplicates().dropna().sort_values()
	artist_place_csv = 'collection/output/artist_place.csv'
	write_series_to_csv(artist_place, artist_place_csv, '\t', False)
	logging.info(msg[2].format(os.path.abspath(artist_place_csv)))

	# Read in artwork (tabbed separator)
	artwork_csv = 'collection/artwork_data.csv'
	artwork_data_frame = read_csv(artwork_csv, ',')
	logging.info(msg[0].format(os.path.abspath(artwork_csv)))

	# Write roles to a .csv file.
	artist_role = extract_filtered_series(artwork_data_frame, 'artistRole')
	artist_role_csv = 'collection/output/artist_role.csv'
	write_series_to_csv(artist_role, artist_role_csv, '\t', False)
	logging.info(msg[3].format(os.path.abspath(artist_role_csv)))

	# Write roles to a .csv file.
	artwork_unit = extract_filtered_series(artwork_data_frame, 'units')
	artwork_unit_csv = 'collection/output/artwork_unit.csv'
	write_series_to_csv(artwork_unit, artwork_unit_csv, '\t', False)
	logging.info(msg[4].format(os.path.abspath(artwork_unit_csv)))


def extract_filtered_series(data_frame, column_name):
	"""
	Returns a filtered Panda Series one-dimensional ndarray from a targeted column.
	Duplicate values and NaN or blank values are dropped from the result set which is
	returned sorted (ascending).
	:param data_frame: Pandas DataFrame
	:param column_name: column name string
	:return: Panda Series one-dimensional ndarray
	"""
	return data_frame[column_name].drop_duplicates().dropna().sort_values()


def read_csv(path, delimiter=','):
	"""
	Utilize Pandas to read in *.csv file.
	:param path: file path
	:param delimiter: field delimiter
	:return: Pandas DataFrame
	"""
	return pd.read_csv(path, sep=delimiter, low_memory=False)


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