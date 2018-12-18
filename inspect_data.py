import logging
import os
import pandas as pd
import sys as sys
import json


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
		'artwork units written to file {0}',
		'artwork subject relationship written to file {0}',
		'subject level 0 written to file {0}',
		'subject level 1 written to file {0}',
		'subject level 2 written to file {0}'
	]

	# Setting logging format and default level
	logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)

	# Read in artist
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

	# Read in artwork
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

	# artwork_json_dir = 'collection/artworks'
	# artwork_subject_csv = 'collection/output/artwork_subject.csv'
	# gci(artwork_json_dir)
	# logging.info(msg[5].format(os.path.abspath(artwork_subject_csv)))

	# Read in subject_level_0
	subject_0_json = 'collection/processed/subjects/level0list.json'
	subject_0_list = read_json(subject_0_json)
	data = {"id":[], "name":[], "parent_id":[]}
	for subject in subject_0_list:
		data["id"].append(subject["id"])
		data["name"].append(subject["name"])
		data["parent_id"].append('')
	subject_0 = pd.DataFrame(data)
	logging.info(msg[0].format(os.path.abspath(subject_0_json)))

	# Write subject_level_0 to a .csv file.
	subject_csv = 'collection/output/subject.csv'
	write_series_to_csv(subject_0, subject_csv, '\t', False)
	logging.info(msg[6].format(os.path.abspath(subject_csv)))

	# Read in subject_level_1
	subject_1_json = 'collection/processed/subjects/level1list.json'
	subject_1_list = read_json(subject_1_json)
	data = {"id":[], "name":[], "parent_id":[]}
	for subject in subject_1_list:
		data["id"].append(subject["id"])
		data["name"].append(subject["name"])
		data["parent_id"].append(subject["parent0"])
	subject_1 = pd.DataFrame(data)
	logging.info(msg[0].format(os.path.abspath(subject_1_json)))

	# Write subject_level_1 to a .csv file.
	subject_csv = 'collection/output/subject.csv'
	write_series_to_csv(subject_1, subject_csv, '\t', False, 'a', False)
	logging.info(msg[7].format(os.path.abspath(subject_csv)))

	# Read in subject_level_2
	subject_2_json = 'collection/processed/subjects/level2list.json'
	subject_2_list = read_json(subject_2_json)
	data = {"id":[], "name":[], "parent_id":[]}
	for subject in subject_2_list:
		data["id"].append(subject["id"])
		data["name"].append(subject["name"])
		data["parent_id"].append(subject["parent1"])
	subject_2 = pd.DataFrame(data)
	logging.info(msg[0].format(os.path.abspath(subject_2_json)))

	# Write subject_level_2 to a .csv file.
	subject_csv = 'collection/output/subject.csv'
	write_series_to_csv(subject_2, subject_csv, '\t', False, 'a', False)
	logging.info(msg[8].format(os.path.abspath(subject_csv)))
	


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


def write_series_to_csv(series, path, delimiter=',', row_name=True, mode='w', header=True):
	"""
	Write Pandas DataFrame to a *.csv file.
	:param series: Pandas one dimensional ndarray
	:param path: file path
	:param delimiter: field delimiter
	:param row_name: include row name boolean
	"""
	series.to_csv(path, sep=delimiter, index=row_name, mode=mode, header=header)

def gci(filepath):
	files = os.listdir(filepath)
	data = {"accession_number":[], "subject_id":[], "subject_name":[]}
	for fi in files:
		fi_d = os.path.join(filepath,fi)            
		if os.path.isdir(fi_d):
			gci(fi_d)                  
		else:			
			with open(fi_d,"r") as f:
				load_dict = json.load(f)
				accession_number = load_dict["acno"]
				try:
					subjects_level0 = load_dict["subjects"]["children"]
					for subject_level0 in subjects_level0:
						subjects_level1 = subject_level0["children"]
						for subject_level1 in subjects_level1:
							subjects_level2 = subject_level1["children"]
							for subject_level2 in subjects_level2:
								data["accession_number"].append(accession_number)
								data["subject_id"].append(subject_level2["id"])
								data["subject_name"].append(subject_level2["name"])
				except:
					pass
	row = pd.DataFrame(data)
	row.to_csv('collection/output/artwork_subject.csv', sep='\t', index=False, mode='a', header=False)

def read_json(path):
	"""
	Utilize json to read in *.json file.
	:param path: file path
	:return: dictionary or list
	"""
	with open(path,"r") as f:
		result = json.load(f)
	return result

if __name__ == '__main__':
	sys.exit(main())