import json
import sys


from extractField import extractField

def main(json_params):
	list_fields = ''
	try:
		obj = extractField(json_params)
		obj.organizeDocs()
		obj.cleanDocs()
		list_fields = obj.extractFields()
	except Exception as err:
          print(err)
	print(list_fields)
main(sys.argv[1])