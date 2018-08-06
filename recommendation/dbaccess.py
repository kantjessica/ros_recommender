from SPARQLWrapper import SPARQLWrapper,JSON

def getDetailById(entity_id):
	sparql = SPARQLWrapper("http://localhost:7200/repositories/ros-model")
	query = """
	select ?dist  ?p ?o
	where { 
		graph ?dist
		{<""" + entity_id + """> ?p ?o}
	}"""
	sparql.setQuery(query)
	sparql.setReturnFormat(JSON)
	detailinfo = sparql.query().convert()
	return detailinfo['results']['bindings']


def getAllResultsFromDB():
	sparql = SPARQLWrapper("http://localhost:7200/repositories/ros-model")
	sparql.setQuery("""
	PREFIX ros-model: <http://ros-model/>
	PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
	select distinct ?pkg  
	where { 		
		   ?pkg rdf:type ros-model:Package.
	} limit 100
	""")
	sparql.setReturnFormat(JSON)
	results = sparql.query().convert()
	return results['results']['bindings']


def addIdsForEntities(entities):
	for index, entity in enumerate(entities):
		entity['id'] = index