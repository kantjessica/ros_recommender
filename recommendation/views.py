from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from . import dbaccess
from .forms import SearchForm

def detail(request, entity_id):
	full_entity_id = "http://"+entity_id
	#print(full_entity_id)
	detailinfo = dbaccess.getDetailById(full_entity_id)
	#print(detailinfo)
	context = {
		"detailinfo": detailinfo
	}
	template = loader.get_template('recommendation/detail.html')
	return HttpResponse(template.render(context, request))

def index(request):
	if request.method == 'POST':
		form = SearchForm(request.POST)
		#print(form)
		if form.is_valid():
			print(form.cleaned_data['keywords'])
			keyword = form.cleaned_data['keywords']
			entities = dbaccess.getAllResultsFromDB()
			dbaccess.addIdsForEntities(entities)
			template = loader.get_template('recommendation/index.html')
			context = {
				"entities": entities
			}
			return HttpResponse(template.render(context, request))
	else:
		form = SearchForm()
	return render(request, 'recommendation/index.html',{'form': form})