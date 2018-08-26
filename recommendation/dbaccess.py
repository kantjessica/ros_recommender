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


def getAllResultsFromDB(keywords, theType, distribution):
	if(theType == 'Both'):
		typesentence = '?enti ?p ?o.'
	else:
		typesentence = '?enti a ros-model:'+theType+'.'
	if(distribution == 'All'):
		distsentence = '?g'
	else:
		distsentence = 'ros-model:'+distribution
	sparql = SPARQLWrapper("http://localhost:7200/repositories/ros-model")
	query = """
	PREFIX : <http://www.ontotext.com/connectors/lucene#>
	PREFIX inst: <http://www.ontotext.com/connectors/lucene/instance#>
	PREFIX ros-model: <http://ros-model/>
	PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
	SELECT  distinct ?enti
	where{
		?search a inst:repos_pkg_index;
		:query \"""" + keywords + '";' + """
		:entities ?enti.
		graph """ + distsentence + """ {

	""" + typesentence + """
		}
	}
	"""
	print(query)
	sparql.setQuery(query)
	sparql.setReturnFormat(JSON)
	results = sparql.query().convert()
	#print(results)
	return results['results']['bindings']

def addIdsForEntities(entities):
	for index, entity in enumerate(entities):
		entity['id'] = index

def getOtherPackages(entity_id):
	sparql = SPARQLWrapper("http://localhost:7200/repositories/ros-model")
	query = """
	PREFIX ros-model: <http://ros-model/>
	PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
	select ?reposname ?pname ?g
	where{
	graph ?g{
	<"""+entity_id+"""> a ros-model:Package.
	?repos a ros-model:Repository;
		ros-model:hasRelease ?rl;
		rdfs:label ?reposname.
	?rl ros-model:hasPackage <"""+entity_id+""">;
		ros-model:hasPackage ?p.
		?p ros-model:Name ?pname.
	filter(?p != <"""+entity_id+""">).
	}}"""
	#print(query)
	sparql.setQuery(query)
	sparql.setReturnFormat(JSON)
	detailinfo = sparql.query().convert()
	return detailinfo['results']['bindings']

def getAllPackagesInRepo(entity_id):
	sparql = SPARQLWrapper("http://localhost:7200/repositories/ros-model")
	query = """
	PREFIX ros-model: <http://ros-model/>
	PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
	select ?reposname ?pname ?g
	where {
		graph ?g{
			<"""+entity_id+"""> a ros-model:Repository;
			rdfs:label ?reposname;
			ros-model:hasRelease ?rl.
			?rl ros-model:hasPackage ?pkg.
			?pkg ros-model:Name ?pname.
		}
	}
	"""
	sparql.setQuery(query)
	sparql.setReturnFormat(JSON)
	detailinfo = sparql.query().convert()
	return detailinfo['results']['bindings']

def getAllTags():
	sparql = SPARQLWrapper("http://localhost:7200/repositories/ros-model")
	query = """
	PREFIX ros-model: <http://ros-model/>
	select distinct ?t
	{
		?uc a ros-model:Usecase;
		ros-model:Tag ?t.
	}
	"""
	sparql.setQuery(query)
	sparql.setReturnFormat(JSON)
	results = sparql.query().convert()
	return results['results']['bindings']