# -*- encoding: utf-8 -*-
import json
import csv
from constants import  ( IPA_SYMBOLS, STRESS, COMMA, PERIOD, SYLLABLE, FMATRIX )


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
	ipa_symbol = force_unicode(ipa_symbol)
	ndx = IPA_DICT[ ipa_symbol ]
	fdict = {}
	for feature in FMATRIX:
		val = FMATRIX[ feature ][ndx]
		fdict[ feature ] = val
	output = { ipa_symbol : fdict }
	### more print magic here
	return output

def features( phon_trans, posfeatures=None, negfeatures=None ):
	if posfeatures:
		if negfeatures:
			data = find_plus( phon_trans, posfeatures )
			return find_minus(phon_trans, negfeatures, data_arg=data )
		else:
			return find_plus( phon_trans, posfeatures )
	else:
		return find_minus( phon_trans, negfeatures )

def find_plus( phon_trans, posfeatures ):
	assert type(posfeatures) == list, "posfeatures must be passed as list [ ] "
	ndx = len(posfeatures) - 1
	data = ''.join(phon_trans.tokens)
	while ndx >= 0:
		feature = posfeatures[ndx]
		n_data = _find_pos( feature, data )
		data = n_data
		ndx -= 1
	output = set( data )
	return output

def find_minus( phon_trans, negfeatures, data_arg=None ):
	assert type(negfeatures) == list, "negfeatures must be passed as list [ ] "
	ndx = len(negfeatures) - 1
	if data_arg:
		data = list(data_arg)
	else:
		data = ''.join(phon_trans.tokens)
	while ndx >= 0:
		feature = negfeatures[ndx]
		n_data = _find_neg( feature, data )
		data = n_data
		ndx -= 1
	output = set( data )
	return output

def find_pos( feature, data  ):
	"""
	Used in Features class to find positive features in the fmatrix.
	"""
	f_list = FMATRIX[ feature ]
	found = []
	for symbol in data:
		if symbol not in [ COMMA,PERIOD,STRESS,SYLLABLE ]:
			ndx = IPA_DICT[ symbol ]
			val = f_list[ ndx ]
			if val == "+":
				found.append( symbol )
	return found

def find_neg( feature, data ):
	"""
	Used in Features class to find negative features in the fmatrix.
	"""
	f_list = FMATRIX[ feature ]
	found = []
	for symbol in data:
		if symbol not in [ COMMA,PERIOD,STRESS,SYLLABLE ]:
			ndx = IPA_DICT[ symbol ]
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
	
def force_unicode(token):
	if type(token) == str:
		return token.decode('utf-8')
	else:
		return token
		
IPA_DICT = ipa_dict()

