# Ytpak Video analyses
*Auther : Atique Ur Rehman*

### This is a tutorial on scrapping data using [Scrapy](https://scrapy.org/). Scrapy was used to scrap data about videos from a video content providing website [YTPAK](https://www.ytpak.com/).
- First an initial search was made with a specific title, in our case "The kapil sharma Show"
- All the videos in the result were visited
- For each visited video, all the data including likes, views and comments were scrapped
- Then the suggessions of this visited video were visited recursively.

### Spiders
- **ytpak_spider.py** for scrapping all the meta data.
- **ytpak_connections_spider.py** for sugession related data.

### Data
I ended up with two datasets from these spiders :
- First with the comments, likes, views and date
- Second with a list of videos and next suggested video

### Analyses (ytpak_analyses.ipynb)
I have conducted three different analyses for just proof of concept
- Plot of No. of views VS No. of likes 
- Plot of the popularity of "Tha kapil sharma show" with time
- Plot of the sugesstion graph of the videos with hop counts(how far it was from original video). Using this graph we can visualize
    - How suggessions span to very different class of videos, and can take you places
    - How the related videos are clusstered with only < 10 hops, after that irrelevent videos starts
    - The diversity in the sugession algorithnm
    
**Note:** I do not claing any of this data to be mine, it was scrapped for academic purposes only. Ytpak website have a *robots.txt* file the which on this day *5 March, 2017* reads:
```
User-agent: *
Allow: /

Sitemap: https://www.ytpak.com/sitemap_index.php
```
Which means the website allows the scrapping of all the content.
The code is released under MIT license, a copy of the license can be found in the root folder.

### Libraries required
The dollowing libraries were used in the project all of with can be installed using the conda command of [anaconda](www.continuum.io) or with pip.
- Pandas (0.18.1)
- Numpy (1.11.1)
- Matplotlib (1.5.1)
- Plotly (1.12.9)
- Networkx (1.11)
- Scrapy (1.1.1)

### Usage
- For executing ipython notebook execute the following command from the root directory, which will open the ipython interface, from there simple click on the notebbok named "ytpak_analyses.ipynb".
```
ipython notebook
```
- For running spiders, run the following command :
```
scrapy runspider <spider name> -o <output file name>
```
#### P.S : For hover effect on the graph eigther run the complete notebook with data, or download the html version and open in browser.
