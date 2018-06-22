from haversine import haversine
import requests
import pandas as pds
import pprint as pp
import time

def replace_stuff(string):
    string = string.strip()
    string = string.replace('&', '%26')
    string = string.replace("'", "%27")
    string = string.replace(' ', '+')
    return (string)

def fetch(dept): # fetch IRIS polygons within selected departments
    list_raw=[]
    url = "https://data.opendatasoft.com/api/records/1.0/search/?dataset=contours-iris-2016-epci%40public&rows=-1&facet=code_dept&refine.code_dept=" + dept
    response = requests.get(url)
    data = response.json()
    #store centroids, 'code_iris' and geo shape in array
    for i in range(len(data['records'])):
        try:
            list_raw.append(dict([('coordinates-long-lat',data['records'][i]['geometry']['coordinates']),('code_iris',data['records'][i]['fields']['code_iris']),('nom_iris',data['records'][i]['fields']['nom_iris']),('geo_shape',data['records'][i]['fields']['geo_shape'])]))
        except KeyError:
            pass
    return(list_raw)


def fetchincome(code_iris): #fetches income data for the relevant IRIS polygon
    url_dem = "https://data.opendatasoft.com/api/records/1.0/search/?dataset=base-iris-sur-les-revenus-declares%40public&rows=-1&sort=dec_med13&facet=iris&refine.iris="
    response_dem = requests.get(url_dem + code_iris)
    data_dem = response_dem.json()
    try:
        income=dict([('median_income',data_dem['records'][0]['fields']['dec_med13'])])
    except IndexError:
        income=''
    return(income)


def fetchage(code_iris): #fetches age data for the relevant IRI polygons
    url_dem = "https://public.opendatasoft.com/api/records/1.0/search/?dataset=france-donnees-population-a-liris&rows=-1&refine.dciris="
    response_dem = requests.get(url_dem + code_iris)
    data_age = response_dem.json()
    try:
        agedata=dict([('population',data_age['records'][0]['fields']['p10_pop']),('population_men',data_age['records'][0]['fields']['p10_poph']),('population_women',data_age['records'][0]['fields']['p10_popf']),('population_15_more',data_age['records'][0]['fields']['p10_popmen15p']),('population_1524',data_age['records'][0]['fields']['p10_popmen1524']),('population_2554',data_age['records'][0]['fields']['p10_popmen2554']),('population_5579',data_age['records'][0]['fields']['p10_popmen5579']),('population_80_more',data_age['records'][0]['fields']['p10_popmen80p'])])
    except IndexError:
        agedata=dict([('population',''),('population_men',''),('population_women',''),('population_15_more',''),('population_1524',''),('population_2554',''),('population_5579',''),('population_80_more','')])
    return(agedata)

def geocode_address(address,api_key):
    formatted_address = replace_stuff(address)
    url = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + formatted_address + '&key=' + api_key
    response = requests.get(url)
    data = response.json()
    try:
        geo_data = data['results'][0]['geometry']['location']
    except Exception:
        geo_data = ''
    return(geo_data)

def market_data(address,api_key,dept,radius):
    coord_data = geocode_address(address,api_key)
    coord_lat = coord_data['lat']
    coord_lng = coord_data['lng']
    coord = (float(coord_lat),float(coord_lng))
    iris_data = fetch(str(dept))
    results = []
    for i in range(len(iris_data)):
        centroid_lat = iris_data[i]['coordinates-long-lat'][1]
        centroid_lng = iris_data[i]['coordinates-long-lat'][0]
        centroid_coord = (float(centroid_lat),float(centroid_lng))
        if haversine(centroid_coord,coord) <= float(radius):
            results.append(iris_data[i])
    final_results = []
    for j in range(len(results)):
        x = {'input_address': address}
        age = fetchage(str(results[j]['code_iris']))
        income = fetchincome(str(results[j]['code_iris']))
        result = results[j]
        dict = {}
        dict.update(x)
        dict.update(result)
        dict.update(age)
        dict.update(income)
        final_results.append(dict)
    return(final_results)




department = input('Quel département ? (xx) ')
address = input('Quelle adresse ? ')
radius = input('Dans un rayon de cb de km souhaitez vous regarder ? ')
api_key = input('Entrez votre api_key Google Maps : ')

rez = market_data(address,api_key,department,radius)
df = pds.DataFrame(rez)
df.to_csv('results_rue_des_nouettes')


