from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from . import dbaccess,io
from .forms import SearchForm

def detail(request, entity_id):
	full_entity_id = "http://"+entity_id
	print('##'+full_entity_id)
	detailinfo = dbaccess.getDetailById(full_entity_id)
	eid = entity_id[entity_id.rfind('/')+1:]
	if 'Package' in entity_id:
		similar_items = io.getSimilarItems(eid)
		packages = dbaccess.getOtherPackages(full_entity_id);
		#print(packages)
		context = {
			"entity_id": eid,
			"similar_items": similar_items,
			"packages": packages,
			"detailinfo": detailinfo
		}
		template = loader.get_template('recommendation/detail.html')
		return HttpResponse(template.render(context, request))
	elif 'Repository' in entity_id:
		packages = dbaccess.getAllPackagesInRepo(full_entity_id);
		context = {
			"entity_id": eid,
			"packages": packages,
			"detailinfo": detailinfo
		}
		template = loader.get_template('recommendation/detail.html')
		return HttpResponse(template.render(context, request))

def index(request):
	if request.method == 'POST':
		#print(request.POST)
		form = SearchForm(request.POST)
		if form.is_valid():
			keywords = form.cleaned_data['keywords']
			theType = form.cleaned_data['types']
			distribution = form.cleaned_data['distribution']
			entities = dbaccess.getAllResultsFromDB(keywords, theType, distribution)
			dbaccess.addIdsForEntities(entities)
			context = {
				"tags": dbaccess.getAllTags(),
				"entities": entities,
				"form": form
			}
			return render(request, 'recommendation/index.html',context)
		else:
			if 'tag' in request.POST:
				keywords = '*'+request.POST['tag']+'*'
			print(keywords)
			entities = dbaccess.getAllResultsFromDB(keywords, 'Package', 'All')
			dbaccess.addIdsForEntities(entities)
			context = {
				"tags": dbaccess.getAllTags(),
				"entities": entities,
				"form": form
			}
	else:
		context = {
				"tags": dbaccess.getAllTags(),
				"form": SearchForm()
			}
	return render(request, 'recommendation/index.html',context)