# -*- encoding: utf-8 -*-
import json
import csv
from constants import  ( IPA_SYMBOLS, STRESS, COMMA, PERIOD, SYLLABLE )

### build json array for 
### perkins: -sp -ya -nomc and for words: -nospe
def write_fmatrix():
	f = open( "fmatrix.csv", "rb" )
	rows = csv.reader( f )
	
	feature_dict = {}

	for row in rows:
		temp_list = []
		feature = row[ 0 ]
		for ind in row[ 1: ]:
			temp_list.append( ind )
		feature_dict[feature] = temp_list

	feature_matrix = json.dumps( feature_dict )

	f.close()
	json_file = open( "fmatrix.json", "w" )
	json.dump( feature_matrix, json_file )

def build_fmatrix():
	f = open("fmatrix.json","r")
	feature_matrix = json.load(f)
	f.close()
	return json.loads(feature_matrix)


def get_features(ipa_symbol):
	sym_dict = ipa_dict()
	fmatrix = build_fmatrix()
	ndx = sym_dict[ ipa_symbol ]
	fdict = {}
	for feature in fmatrix:
		val = fmatrix[ feature ][ndx]
		fdict[ feature ] = val
	output = { ipa_symbol : fdict }
	### more print magic here
	print ipa_symbol
	return output

def find_features( phon_trans, posfeatures=None, negfeatures=None ):
	if posfeatures:
		if negfeatures:
			data = find_plus( phon_trans, posfeatures )
			return _red_find_minus(data, negfeatures )
		else:
			return find_plus( phon_trans, posfeatures )
	else:
		return find_minus( phon_trans, negfeatures )


def find_plus( phon_trans, posfeatures ):
	assert type(posfeatures) == list, "posfeatures must be passed as list [ ] "
	fmatrix = build_fmatrix()
	sym_dict = ipa_dict()
	ndx = len(posfeatures) - 1
	data = ''.join(phon_trans.tokens)
	while ndx >= 0:
		feature = posfeatures[ndx]
		n_data = _find_pos( feature, data, fmatrix, sym_dict )
		data = n_data
		print data
		ndx -= 1
	output = set(data)
	return output

def find_minus( phon_trans, negfeatures ):
	assert type(negfeatures) == list, "negfeatures must be passed as list [ ] "
	fmatrix = build_fmatrix()
	sym_dict = ipa_dict()
	ndx = len(negfeatures) - 1
	data = ''.join(phon_trans.tokens)
	while ndx >= 0:
		feature = negfeatures[ndx]
		n_data = _find_neg( feature, data, fmatrix, sym_dict )
		data = n_data
		
		ndx -= 1
	output = set(data)
	return output

def _red_find_minus( data, negfeatures ):
	data = list(data)

	fmatrix = build_fmatrix()
	sym_dict = ipa_dict()
	ndx = len(negfeatures) - 1
	while ndx >= 0:
		feature = negfeatures[ndx]
		n_data = _find_neg( feature, data, fmatrix, sym_dict )
		data = n_data
		
		ndx -= 1
	output = set(data)
	return output


def _find_pos( feature, data, fmatrix, sym_dict ):
	f_list = fmatrix[ feature ]
	found = []
	for symbol in data:
		if symbol.encode('utf-8') not in [ COMMA,PERIOD,STRESS,SYLLABLE ]:
			ndx = sym_dict[ symbol.encode('utf-8') ]
			val = f_list[ ndx ]
			if val == "+":
				found.append( symbol )
	return found

def _find_neg( feature, data, fmatrix, sym_dict ):
	COMMA = "|"
	PERIOD = "‖"
	STRESS = "ˈ"
	
	f_list = fmatrix[ feature ]
	found = []
	for symbol in data:
		if symbol.encode('utf-8') not in [ COMMA,PERIOD,STRESS,SYLLABLE ]:
			ndx = sym_dict[ symbol.encode('utf-8') ]
			val = f_list[ ndx ]
			if val == "-":
				found.append(symbol)
	return found	

def ipa_symbols():
	return IPA_SYMBOLS

def ipa_dict():
	ipa_dict = {}
	for ndx, symbol in enumerate( IPA_SYMBOLS ):
		ipa_dict[ symbol ] = ndx
	return ipa_dict 

	
