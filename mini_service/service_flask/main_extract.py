import sys

from extractField import extractField

def read_file():
	list_fields = ''
	databese_info={
             'localhost':'localhost',
             'user':'postgres',
             'pass':'',
             'db':'pqr_electricaribe'
}
	try:
		obj = extractField('/home/jhonex/document_e1/',databese_info)
		obj.organizeDocs()
		obj.cleanDocs()
		list_fields = obj.extractFields()
	except Exception as err:
          print(err)
	return list_fields
