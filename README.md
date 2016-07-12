# Grailed.com Analysis
This is repository contains code related to the statistical and predictive
analysis we performed on Grailed.com. We hope you find some of these insightful, a lot of these
validate trends that are obvious to fashion/grailed hobbyists but there are some surprises
sprinkled in there.


We looked at various user, designer, and overall site statistics. We also built a simple 
item/designer recommender and clustered designers using collaborative filtering. We're currently
working on analyzing description text.

#### Authors
* Kenneth Vuong - [kennzoid@gmail.com](mailto:kennzoid@gmail.com)
* Vyom Shah - [admin@uniqlo.com](admin@uniqlo.com)

## What is Grailed?

Grailed is a (now) popular online marketplace for primarily designer menswear. Because of its niche community, the content was ideal for performing a fashion-centric data mining project (as opposed to something like eBay). The admins were also very supportive and allowed us to scrape their site at a reasonable pace. Both of us are also frequent users of the site and very familiar with its quirks.

## Notebooks
This is the most important part of the repo, check these out! We found the Github notebook viewer to be unsatisfactory, so we encourage viewers to use jupyter's nbviewer web app to view them instead (links below).

#### Site Analysis
[Notebook](http://nbviewer.jupyter.org/github/kennzoid/grailed-analysis/blob/master/notebooks/site_analysis.ipynb)

* Dataset Info
* Growth
* User Statistics
* Designer Statistics (check out the bump plot)
* Pricing Statistics (lowballing and retail)
* Miscellaneous Distributions

#### Collaborative Filtering
[Notebook](http://nbviewer.jupyter.org/github/kennzoid/grailed-analysis/blob/master/notebooks/collaborative_filtering.ipynb)

* Item recommendations using item-item collaborative filtering
* Designer recommendations using designer-designer collaborative filtering
* Designer clustering using agglomerative clustering (Pearson Correlation as distance)


#### Description Analysis (currently WIP)
[Notebook](https://github.com/kennzoid/grailed-analysis/blob/master/notebooks/description_analysis.ipynb)

* Predicting rate of sale using description features
* Identifying designer-specific language/terminology

## Scraper Code
A collection of small scripts we used to scrape the site. This includes the script for downloading JSON as well as the code we used to clean the data and create an SQLite database. We used SQLite to create the CSV files afterwards (those are used in the notebooks).

## Can I have the data?
Unfortunately we can't release the data we scraped.
