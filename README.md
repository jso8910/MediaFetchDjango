# MediaFetch (Django edition for cs50 web final project)

## Steps to run:
- `$ pip install -r requirements.txt`
- `$ python3 manage.py makemigrations`
- `$ python3 manage.py migrate`
- `$ python3 manage.py runserver`

## Important information
So I already made this project (kind of). I made it in flask a while back (summer 2020) and I converted it to Django with new functionality. Only a couple functions are copied from the original.
1. The webscraper. There was no point rewriting that considering (unless I find a better idea) it is pretty straightforward
2. The graph maker functions. I remember that figuring out how to get the dates and stuff and making the usage graphs was really complicated first time around so I decided to copy the same function and modify it a tiny bit

## Detailed description
### API app
- api/views.py
  - The `ArticleSerializer` is to tell `drf_spectacular` what information is in each article in the list of the response for the documentation
  - The `NewsSerializer` is the actual serializer for the rest api endpoint (to be perfectly honest I feel like I am not using it right but it works for the documentation) and is used by `drf_spectacular`
  - The `News` API endpoint. The main backbone of the entire project. The main bulk of the lines of it is the detailed description of the parameters for (yet again) documentation. Then there is calling the funciton that scrapes Google News
- api/scraper.py
  - First in the file, it takes the parameters (excluding, requiring, etc) and converts them into the strings that Google News accepts as a search
  - Then, the URL is fomatted and retrieved.
  - The page is then parsed by BS4 and LXML for the specific classes
  - The response json is formulated and returned, which is the response of the `News` api endpoint
- api/urls.py
  - Completely basic except the documentation pages are added
- api/models.py
  - Queries are recorded in an object with all the needed fields so the graphs can be made in the mainsite app

### Main Site App
- mainsite/views.py
  - `logout`, `login_view`, `register`, and `index` are all self explanatory (though index only works if you are logged out, otherwise you are redirected to the dashboard)
  - The `timeList` function was created to convert a time into a list of date, month, and year
  - `allUsersSvg` and `yourUserSvg` are both essentially the same with the difference that `yourUserSvg` only selects queries from your user, not everyone. 
    - First, it gets a QuerySet of values in the Queries model
    - Next, it gets the date of the first and last values in the QuerySet
    - Then it creates the labels and populates the data and returns the svgs
  - Dashboard just selects a random example query and returns the rendered template along with the token
- mainsite/urls.py
  - All the paths from views.py
- mainsite/static/mainsite/styles.css
  - Some nice CSS!
- mainsite/templates/mainsite/layout.html
  - The layout of the page with bootstrap and the navbar
- mainsite/templates/mainsite/index.html
  - A minimal index page to tell people to sign up for the service
- mainsite/templates/mainsite/login.html and register.html
  - The register pages
- mainsite/templates/mainsite/dashboard.html
  - Displays the token and 10 articles that are retrieved with a fetch request plus the graphs. Flexboxes galore.

### Example app
- exampleapp/models.py
  - Simply a `Category` model which stores the user it belongs to and the content of the category
- exampleapp/views.py
  - There is a `delete` function to delete a `Category` of a certain id
  - There is an `add` function to add a new `Category` of a certain string for the category
  - There is an `index` function to render the index page of this exampleapp with the token passed to the template and the list of categories the user subscribes to
- exampleapp/urls.py
  - Basic `urls.py`
- exampleapp/static/exampleapp/styles.css
  - Basically the exact same styles as in `mainsite`
- exampleapp/templates/exampleapp/layout.html
  - Essentially the same layout as `mainsite` but with search
- exampleapp/templates/exampleapp/index.html
  - Shows the articles from the followed categories and allows you to add or remove them
  - The JavaScript wasn't written very well because I am still not very good at JS
- exampleapp/templates/exampleapp/search.html
  - Allows you to search news using advanced things (when the article was published, etc)
- MediaFetch/urls.py
  - Paths to the apps and for some reason something I needed for static to work
- MediaFetch/settings.py
  - Installed apps etc.
  
## Why my project meets the requirements
My project is clearly distinct from the other projects as, in other projects, a web scraper API was not created neither was a public facing API (for anyone to use other than for database manipulation) used. As well, it implements Django REST Framework and includes API docs as well as an example usage of the API.

Django is also in the backend and JS is used (not on every page but for quite a few) in the frontend of the project to dynamically load data from the API.