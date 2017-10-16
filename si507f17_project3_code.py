from bs4 import BeautifulSoup
import unittest
import requests

#########
## Instr note: the outline comments will stay as suggestions, otherwise it's too difficult.
## Of course, it could be structured in an easier/neater way, and if a student decides to commit to that, that is OK.

## NOTE OF ADVICE:
## When you go to make your GitHub milestones, think pretty seriously about all the different parts and their requirements,
## and what you need to understand. Make sure you've asked your questions about Part 2 as much as you need to before Fall Break!


######### PART 0 #########

# Write your code for Part 0 here.
def print_alt_text(url):
    try:
        part0_html=open('gallery.html','r',encoding='utf-8')
        text=part0_html
    except:
        text=requests.get(url).text
        part0_html=open('gallery.html','w+',encoding='utf-8')
        part0_html.write(text)
    soup=BeautifulSoup(text,'html.parser')
    part0_html.close()     
    for img in soup.find('body').find_all('img'):
        if 'alt' in img.attrs:
            print(img['alt'])
        else:
            print('No alternative text provided!')
        print()
   
URL_gallery="http://newmantaylor.com/gallery.html"
print_alt_text(URL_gallery)
######### PART 1 #########

# Get the main page data...

# Try to get and cache main page data if not yet cached
# Result of a following try/except block should be that
# there exists a file nps_gov_data.html,
# and the html text saved in it is stored in a variable 
# that the rest of the program can access.

# We've provided comments to guide you through the complex try/except,
# but if you prefer to build up the code to do this scraping and caching yourself, that is OK.


# Get individual states' data...

# Result of a following try/except block should be that
# there exist 3 files -- arkansas_data.html, california_data.html, michigan_data.html
# and the HTML-formatted text stored in each one is available
# in a variable or data structure 
# that the rest of the program can access.

# TRY: 
# To open and read all 3 of the files

# But if you can't, EXCEPT:

# Create a BeautifulSoup instance of main page data 
# Access the unordered list with the states' dropdown

# Get a list of all the li (list elements) from the unordered list, using the BeautifulSoup find_all method

# Use a list comprehension or accumulation to get all of the 'href' attributes of the 'a' tag objects in each li,
# instead of the full li objects

# Filter the list of relative URLs you just got to include only the 3 you want: AR's, CA's, MI's,
# using the accumulator pattern & conditional statements


# Create 3 URLs to access data from by appending those 3 href values to the main part of the NPS url. Save each URL in a variable.


## To figure out what URLs you want to get data from (as if you weren't told initially)...
# As seen if you debug on the actual site.
# e.g. Maine parks URL is "http://www.nps.gov/state/me/index.htm",
# Michigan's is "http://www.nps.gov/state/mi/index.htm"
# -- so if you compare that to the values in those href attributes you just got... how can you build the full URLs?


# Finally, get the HTML data from each of these URLs, and save it in the variables you used in the try clause
# (Make sure they're the same variables you used in the try clause! Otherwise, all this code will run every time you run the program!)


# And then, write each set of data to a file so this won't have to run again.

def cache_pages_data(url_base):
    try:
        h=open('nps_gov_data.html','r',encoding='utf-8')
        text=h.read()
    except:
        text=requests.get(url_base).text
        h=open('nps_gov_data.html','w+',encoding='utf-8')
        h.write(text)
    soup=BeautifulSoup(text,'html.parser')
    h.close()
    li_list=soup.find('ul',class_='dropdown-menu SearchBar-keywordSearch').find_all('li',recursive=False)
    base='/'.join(url_base.split('/')[0:-1:1])
    print(base)
    full_href_list=[base+li.a['href'] for li in li_list if li.a.string == 'Arkansas' or \
                    li.a.string =='California' or li.a.string =='Michigan']

    name_dict={'ar':'arkansas_data.html','ca':'california_data.html','mi':'michigan_data.html'}
    for url_state in full_href_list:
        cache_name=name_dict.get(url_state.split('/')[-2])
        try:
            s=open(cache_name,'r',encoding='utf-8')
        except:
            print(url_state)
            text0=requests.get(url_state).text
            s=open(cache_name,'w+',encoding='utf-8')
            s.write(text0)
        s.close()

URL_NPS='https://www.nps.gov/index.htm'
cache_pages_data(URL_NPS)
######### PART 2 #########

## Before truly embarking on Part 2, we recommend you do a few things:

# - Create BeautifulSoup objects out of all the data you have access to in variables from Part 1
# - Do some investigation on those BeautifulSoup objects. What data do you have about each state? How is it organized in HTML?

# HINT: remember the method .prettify() on a BeautifulSoup object -- might be useful for your investigation!
# So, of course, might be .find or .find_all, etc...

# HINT: Remember that the data you saved is data that includes ALL of the parks/sites/etc in a certain state,
# but you want the class to represent just ONE park/site/monument/lakeshore.

# We have provided, in sample_html_of_park.html an HTML file that represents the HTML about 1 park.
# However, your code should rely upon HTML data about Michigan, Arkansas, and Califoria you saved and accessed in Part 1.

# However, to begin your investigation and begin to plan your class definition,
# you may want to open this file and create a BeautifulSoup instance of it to do investigation on.

# Remember that there are things you'll have to be careful about listed in the instructions
# -- e.g. if no type of park/site/monument is listed in input, one of your instance variables should have a None value...

## Define your class NationalSite here:
class NationalSite(object):
    def __init__(self,soup):
        self.location=soup.find('h4').string
        self.name=soup.find('h3').string
        type_tag=soup.find('h3').find_previous_sibling()
        assert(type_tag.name=='h2')
        if type_tag.string != '':
            self.type=type_tag.string
        else:
            self.type=None
        self.description=soup.find('p').string.strip()

        self.basic_info_url=soup.find('div',
                                      class_='col-md-12 col-sm-12 noPadding stateListLinks')\
                                      .ul.find_all('li',recursive=False)[1].a['href']

        print(self.basic_info_url)

    def __str__(self):
        return '{} | {}'.format(self.name,self.location)
        
    def get_mailing_address(self):
        try:
            h=open('{} basic info.html'.format(self.name),'r',encoding='utf-8')
            text.h.read()
        except:
            text=requests.get(self.basic_info_url).text
            h=open('{} basic info.html'.format(self.name),'w+',encoding='utf-8')
            h.write(text)
        soup=BeautifulSoup(text,'html.parser')
        h.close()
        span_list=soup.find('div',class_='physical-address').find('div',itemprop='address').find_all('span')
        splitted_addresses=[span.string for span in span_list if 'itemprop' not in span.attrs or span['itemprop']!='streetAddress']
        return '/'.join(splitted_addresses)

    def __contains__(self,key):
        return key in self.name
## Recommendation: to test the class, at various points, uncomment the following code and
# invoke some of the methods / check out the instance variables of the test instance saved in the variable sample_inst:
"""
f = open("alkatraze island.html",'r',encoding='utf-8')
soup_park_inst = BeautifulSoup(f.read(), 'html.parser') # an example of 1 BeautifulSoup instance to pass into your class
inst = NationalSite(soup_park_inst)
print(inst.location)
print(inst.name)
print(inst.type)
print(inst.description)
print(inst)
print(inst.get_mailing_address())
f.close()
"""

######### PART 3 #########

# Create lists of NationalSite objects for each state's parks.

# HINT: Get a Python list of all the HTML BeautifulSoup instances that represent each park, for each state.




##Code to help you test these out:
# for p in california_natl_sites:
# 	print(p)
# for a in arkansas_natl_sites:
# 	print(a)
# for m in michigan_natl_sites:
# 	print(m)



######### PART 4 #########

## Remember the hints / things you learned from Project 2 about writing CSV files from lists of objects!

## Note that running this step for ALL your data make take a minute or few to run
# -- so it's a good idea to test any methods/functions you write with just a little bit of data, so running the program will take less time!

## Also remember that IF you have None values that may occur, you might run into some problems and have to debug for where you need to put in some None value / error handling!

