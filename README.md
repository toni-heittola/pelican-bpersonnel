Pelican-bpersonnel - Personnel listings for Pelican
===================================================

`pelican-bpersonnel` is an open source Pelican plugin to produce personnel listings from yaml data structures. The plugin is developed to be used with Markdown content and Bootstrap 3 based template. 

**Author**

Toni Heittola (toni.heittola@gmail.com), [GitHub](https://github.com/toni-heittola), [Home page](http://www.cs.tut.fi/~heittolt/)

Installation instructions
=========================

## Requirements

**bs4** is required. To ensure that all external modules are installed, run:

    pip install -r requirements.txt

**bs4** (BeautifulSoup) for parsing HTML content

    pip install beautifulsoup4

## Pelican installation

Make sure you include [Bootstrap](http://getbootstrap.com/) in your template.

Make sure the directory where the plugin was installed is set in `pelicanconf.py`. For example if you installed in `plugins/pelican-bpersonnel`, add:

    PLUGIN_PATHS = ['plugins']

Enable `pelican-bpersonnel` with:

    PLUGINS = ['pelican-bpersonnel']

Insert personnel list or panel into the page template:
 
    {% if page.bpersonnel %}
        {{ page.bpersonnel }}
    {% endif %}

Insert personnel list or panel into the article template:

    {% if article.bpersonnel %}
        {{ article.bpersonnel }}
    {% endif %}

Usage
=====

Personnel listing generation is triggered for the page either by setting BPERSONNEL metadata for the content (page or article) or using `<div>` with class `bpersonnel` or `bpersonnel-item`. 

Layouts

- **bpersonnel**, personnel listing  
- **bpersonnel-item**, individual personnel information card

There is two layout modes available for both of these: `panel` and `list`. 

## Personnel registry

Registry has two parts: 
    - **`personnel`** containing basic information of each person
    - **`sets`**, list of person assigned to the set and extra information to override basic information 

Example yaml-file:

    personnel:
      - firstname: Test
        lastname: Person1
        email: test.person@foo.bar
        homepage: http://www.test.person.hompage.com
        scholar: 
        affiliation_title: University X
        affiliation_abbreviation: UX
        affiliation_department: 
        affiliation_url:
         
        photo: images/face.jpg
      - firstname: Test
        lastname: Person2
        email: test.person@foo.bar
        homepage: http://www.test.person.hompage.com
        scholar: 
        affiliation:
          - title: University X1
            abbreviation: UX1
            department: 
            url:
          - title: University X2
            abbreviation: UX2
            department: 
            url:          
               
        photo: images/face.jpg
        responsibilities: reading
        
    sets:
      set1:
        - firstname: Test
          lastname: Person1
          responsibilities: writing
          photo: images/face1.jpg
        - firstname: Test
          lastname: Person2
          responsibilities: reading
          photo: images/face2.jpg
          main: true
      set2:
        - firstname: Test
          lastname: Person1
          responsibilities: walking
          coordinator_list: Walking,/walking          

Fields having values in sets (other than firstname and lastname) will override personnel fields. Fields ending with `_list` are converted into list of links. Format for these fields `[title1],[link1];[title2],[link2]`

The default templates support following fields:

- `firstname`
- `lastname`
- `email`
- `homepage`, homepage url
- `scholar`, google scholar link
- `affiliation_title`
- `affiliation_abbreviation`
- `affiliation_department`
- `affiliation_url`
- `affiliation`, dict with fields `title`, `abbreviation`, `department`, `url`
- `photo`, link profile image, use 1:1 aspect ratio
- `responsibilities`
- `coordinator_list`
- `main`, if set true person is highlighted

## Parameters

The parameters can be set in global, and content level. Globally set parameters are are first overwritten content meta data, and finally with div parameters.

### Global parameters

Parameters for the plugin can be set in `pelicanconf.py' with following parameters:

| Parameter                 | Type      | Default       | Description  |
|---------------------------|-----------|---------------|--------------|
| BPERSONNEL_SOURCE         | String    |  | YAML-file to contain personnel registry, see example format above. |
| BPERSONNEL_TEMPLATE       | Dict of Jinja2 templates |  | Two templates can be set for panel and list  |
| BPERSONNEL_ITEM_TEMPLATE  | Dict of Jinja2 templates |  | Two templates can be set for panel and list  |
| BPERSONNEL_PERSON_ITEM_TEMPLATE  | Jinja2 template |  | Template for person information card  |
| BPERSONNEL_PANEL_COLOR          | String    | panel-primary |  CSS class used to color the panel template in the default template. Possible values: panel-default, panel-primary, panel-success, panel-info, panel-warning, panel-danger |
| BPERSONNEL_HEADER               | String    | Content       | Header text  |
| BPERSONNEL_SORT              | Boolean    | False       | Sorting of the listing based on lastname,firstname  |
| BPERSONNEL_DEBUG_PROCESSING | Boolean    | False  | Show extra information in when run with `DEBUG=1` |

### Content wise parameters

| Parameter                 | Example value     | Description  |
|---------------------------|-----------|--------------|
| BPERSONNEL                | True      | Enable bpersonnel listing for the page | 
| BPERSONNEL_SOURCE         | content/data/personnel.yaml | Personnel registry file |
| BPERSONNEL_SET            | set1 | Personnel set used, if empty full personnel is used.   |
| BPERSONNEL_MODE           | panel | Layout type, panel or list |
| BPERSONNEL_PANEL_COLOR    | panel-info | CSS class used to color the panel template in the default template. Possible values: panel-default, panel-primary, panel-success, panel-info, panel-warning, panel-danger |
| BPERSONNEL_HEADER         | Personnel | Header text  |
| BPERSONNEL_FIELDS         | email, photo, affiliation | comma separated list of field to be shown |
| BPERSONNEL_SORT        | True | Sorting of the listing based on lastname,firstname |

Example:

    Title: Test page
    Date: 2017-01-05 10:20
    Category: test
    Slug: test-page
    Author: Test Person
    bpersonnel: True
    bpersonnel_set: set1
    bpersonnel_header: People
    bpersonnel_fields: affiliation, email, photo
    
Personnel listing is available in template in variable `page.bpersonnel` or `article.bpersonnel`
   
### Div wise parameters

Valid for `<div>` classes `bpersonnel` and `bpersonnel-item`:

| Parameter                 | Example value     | Description  |
|---------------------------|-------------|--------------|
| data-source               | content/data/personnel.yaml | Personnel registry file
| data-set                  | set1        | Personnel set used, if empty full personnel is used.  |
| data-mode                 | panel       | Layout type, panel or list |
| data-header               | Personnel   | Header text |
| data-panel-color          | panel-info | CSS class used to color the panel template in the default template. Possible values: panel-default, panel-primary, panel-success, panel-info, panel-warning, panel-danger |
| data-fields               | email, photo, affiliation | comma separated list of field to be shown |
| data-sort                 | True | Sorting of the listing based on lastname,firstname |

Valid for `bpersonnel-item`:

| Parameter                 | Example value     | Description  |
|---------------------------|-------------|--------------|
| data-firstname            | David | First name of person to be shown |
| data-lastname            | Last | last name of person to be shown | 

Example listing:

    <div class="bpersonnel" data-source="content/data/personnel.yaml" data-set="set1" data-fields="responsibilities, affiliation, email, homepage, photo"></div>
    
Example of personnel cards   

    Title: Test page
    Date: 2017-01-05 10:20
    Category: test
    Slug: test-page
    Author: Test Person
    bpersonnel_header: People
    bpersonnel_fields: affiliation, email, photo
    bpersonnel_source: content/data/personnel.yaml
    <div class="bpersonnel-card" data-person-firstname="Test" data-person-lastname="Person"></div>