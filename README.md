# Market Research

This project aims at facilitating geo-targeted market research in France by fetching demographic data from the OpenDataSoft API (which relies on France's open data initiative: https://www.data.gouv.fr

## Getting Started

### Prerequisites

Make sure you have Python 3.6 installed or higher. Also make sure that you have api_keys granting access to Google Maps API. Specifically, it is necessary to have enabled: Google Places API for web and Geocoding API. More details can be found here: https://cloud.google.com/maps-platform/

### Installing

Open your terminal/command line in the relevant directory which will be the root directory for you project.

Run the following command in the terminal and the code will be copied to your machine in the directory.

```
git clone https://github.com/adrienlin/market-research
```

Make sure pip is up to date

```
python -m pip install --upgrade pip
```

Install all the requirements necessary to run the script

```
pip install -r requirements.txt
```

## Exectute the script

Open the market_sizing.py script, run it and answer all the questions (should be self-explanatory). Change the output filename if needed. It should drop the results file in your root directory.

### Results explanation

The results breaks down all the IRIS contained in the area researched, see the definition of IRIS here : https://www.insee.fr/fr/information/2017499 (the documentation is in French).
The different variables are the following : 
```
code_iris: the INSEE code of the IRIS
coordinates-long-lat: geo coordinates of the IRIS centroid
geo_shape: the geographical shape of the IRIS
input_adress: the address around which you have researched
median income: the median income within the IRIS (in €)
nom_iris: the name of the IRIS
population: population within the IRIS
population_1524: people between 15 and 24
population_15_more: people older than 15
population_2554: population between 25 and 54
population_5579: population between 55 and 79
population_80_more: population older than 80
population_men: nb of men
population_women: nb of women
```

The demographic data dates back to 2013.

## Authors

* **Adrien Lin**

## Acknowledgments

* Thanks so much to OpenDataSoft for making the open data easily accessible via API.
* Kudos to the Open Data Gouv initiative
