import csv,os

def getSimilarItems(name):
	default_similar_item_threshold = 47
	core_package_list = ['catkin','ros_core','ros_base','robot','desktop','desktop_full']
	result = []
	with open(os.path.dirname(os.path.abspath(__file__))+'/lda_75_cosine_top50.csv','r') as csvfile:
		readCSV = csv.reader(csvfile, delimiter=',')
		for row in readCSV:
			if row[0] == name:
				for i in range(1, default_similar_item_threshold):
					if row[i].find(name) == -1 and row[i][row[i].find('\'')+1:row[i].rfind('\'')] not in core_package_list:
						similar_item_dict = dict(name=row[i][row[i].find('\'')+1:row[i].rfind('\'')],score=row[i][row[i].find(',')+1:-1])
						result.append(similar_item_dict)
				break
	return result