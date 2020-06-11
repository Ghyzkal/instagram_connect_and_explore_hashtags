from graph_api_access import getCreds, doAPIcall
import sys
import json
import datetime


def getHashtagInfo( params ) :
	""" API Endpoint:
		https://graph.facebook.com/{graph-api-version}/ig_hashtag_search?user_id={user-id}&q={hashtag-name}&fields={fields}
	"""
	endpointParams = dict()
	endpointParams['user_id'] = params['instagram_account_id'] 
	endpointParams['q'] = params['hashtag_name']
	endpointParams['fields'] = 'id,name'
	endpointParams['access_token'] = params['access_token']

	url = params['endpoint_base'] + 'ig_hashtag_search'

	return doAPIcall( url, endpointParams, params['debug'] )

def getHashtagMedia( params ) :
	"""API Endpoints:
		https://graph.facebook.com/{graph-api-version}/{ig-hashtag-id}/top_media?user_id={user-id}&fields={fields}
		https://graph.facebook.com/{graph-api-version}/{ig-hashtag-id}/recent_media?user_id={user-id}&fields={fields}
	"""
	endpointParams = dict()
	endpointParams['user_id'] = params['instagram_account_id']
	endpointParams['fields'] = 'id,children,caption,comment_count,like_count,media_type,media_url,permalink,timestamp'
	endpointParams['access_token'] = params['access_token']

	url = params['endpoint_base'] + params['hashtag_id'] + '/' + params['type']

	return doAPIcall( url, endpointParams, params['debug'] )

def writeInFileTxt(data, file, type):
	d = str(data)
	with open(file, type) as outfile:
		outfile.write(d)

def writInFileJson(data, file, type) :
	with open(file, type) as outfile:
		json.dump(data, outfile, indent = 4)

def getFileName(type):
	ts = int(datetime.datetime.now().timestamp())
	txt = 'data' + type + 'Media{}.json'
	fileName  = txt.format(ts)

	writeInFileTxt(fileName, type + 'dataFileNames.txt', 'w')

	return fileName


fileNameTop = getFileName('Top')
fileNameRecent = getFileName('Recent')

words = ['harassment', 'abuse', 'domestic', 'violence', 'beat', 'accused', 'woman', 'creep', 'molestation', 'shame', 'illegal', 'report', 'justice', 'lockdown', 'victim']

writeInFileTxt('[', fileNameTop, 'a')
writeInFileTxt('[', fileNameRecent, 'a')

for hashtag in words :
	params = getCreds() 
	params['hashtag_name'] = hashtag 

	hashtagInfoResponse = getHashtagInfo( params ) 
	params['hashtag_id'] = hashtagInfoResponse['json_data']['data'][0]['id']; 

	print ("\nHashtag: " + hashtag) 

	params['type'] = 'top_media' # set call to get top media for hashtag
	hashtagTopMediaResponse = getHashtagMedia( params )
	writInFileJson(hashtagTopMediaResponse['json_data'], fileNameTop, 'a')
	writeInFileTxt(',', fileNameTop, 'a')

	params['type'] = 'recent_media' # set call to get recent media for hashtag
	hashtagRecentMediaResponse = getHashtagMedia( params )	
	writInFileJson(hashtagTopMediaResponse['json_data'], fileNameRecent, 'a')
	writeInFileTxt(',', fileNameRecent, 'a')
	
writeInFileTxt(']', fileNameTop, 'a')
writeInFileTxt(']', fileNameRecent, 'a')
