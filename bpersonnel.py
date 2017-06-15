# -*- coding: utf-8 -*-
"""
Personnel listings -- BPERSONNEL
================================
Author: Toni Heittola (toni.heittola@gmail.com)

"""

import os
import logging
import copy
from bs4 import BeautifulSoup
from jinja2 import Template
from pelican import signals, contents
import yaml
import collections

logger = logging.getLogger(__name__)
__version__ = '0.1.0'

bpersonnel_default_settings = {
    'panel-color': 'panel-default',
    'header': 'Personnel',
    'mode': 'panel',
    'template': {
        'panel': """
            <div class="panel {{ panel_color }}">
              {% if header %}
              <div class="panel-heading">
                <h3 class="panel-title">{{header}}</h3>
              </div>
              {% endif %}
              <table class="table bpersonnel-container">
              {{list}}
              </table>
            </div>
        """,
        'list': """
            {% if header %}<h3 class="section-heading text-center">{{header}}</h3>{% endif %}
            <div class="list-group bpersonnel-container">
                <div class="row">
                {{list}}
                </div>
            </div>
        """},
    'item-template': {
        'panel': """
            <tr>
                {% if photo %}
                <td class="{{item_css}}" style="width: 65px;">
                <img class="img img-circle" src="{{site_url}}/{{ photo }}" alt="{{firstname}} {{lastname}}" width="48px">
                </td>
                {% endif %}
                <td class="{{item_css}}">
                    <div class="row">
                        <div class="col-md-12">
                        <strong>{{firstname}} {{lastname}}</strong>
                        {% if homepage %}
                        <a class="icon" href="{{homepage}}"><i class="pull-right fa fa-home {{item_css}}"></i></a>
                        {% endif %}
                        {% if scholar %}
                        <a class="icon" href="{{scholar}}"><i class="pull-right fa fa-google {{item_css}}"></i></a>
                        {% endif %}
                        {% if linkedin %}
                        <a class="icon" href="{{linkedin}}"><i class="pull-right fa fa-linkedin {{item_css}}"></i></a>
                        {% endif %}
                        {% if email %}
                        <a class="icon" href="mailto:{{email}}"><i class="pull-right fa fa-envelope-o {{item_css}}"></i></a>
                        {% endif %}
                        </div>
                        {% if title %}
                        <div class="col-md-12">
                        <p class="small text-muted">
                        {{title}}
                        </p>
                        </div>
                        {% endif %}
                        {% if affiliation_title %}
                        <div class="col-md-12">
                        <p class="small text-muted">
                            {% if affiliation_url %}
                            <a class="text" href="{{affiliation_url}}">
                            {% endif %}
                                {{affiliation_title}}{% if affiliation_department %} <br><em>{{affiliation_department}}</em>{% endif %}
                            {% if affiliation_url %}
                            </a>
                            {% endif %}
                        </p>
                        </div>
                        {% endif %}
                        {% if coordinator_list %}
                        <div class="col-md-12">
                        <p class="small text-right">Coordinator of <em>{{coordinator_list}}</em></p>
                        </div>
                        {% endif %}
                        {% if responsibilities %}
                        <div class="col-md-12">
                        <p class="small text-right"><em>{{responsibilities}}</em></p>
                        </div>
                        {% endif %}
                    </div>
                </td>
            </tr>
        """,
        'list': """
            <div class="col-md-6 col-xs-12">
                <div class="row list-group-item-" style="padding-bottom:0.5em;">
                    {% if photo %}
                    <div class="col-md-2 col-xs-2">
                        <img class="img img-circle" src="{{site_url}}/{{ photo }}" alt="{{firstname}} {{lastname}}" width="55px">
                    </div>
                    {% endif %}
                    <div class="col-md-8 col-xs-8">
                        <div class="row">
                            <div class="col-md-12">
                                <h4 class="list-group-item-heading {{item_css}}">{{firstname}} {{lastname}}</h4>
                                {% if title %}
                                <p class="text-muted">
                                {{title}}
                                </p>
                                {% endif %}
                            </div>
                            {% if affiliation_title %}
                            <div class="col-md-12">
                                <p class="small text-muted">
                                    {% if affiliation_url %}
                                    <a class="text" href="{{affiliation_url}}">
                                    {% endif %}
                                        {{affiliation_title}}{% if affiliation_department %} <br><em>{{affiliation_department}}</em>{% endif %}
                                    {% if affiliation_url %}
                                    </a>
                                    {% endif %}
                                </p>
                            </div>
                            {% endif %}
                            {% if coordinator_list %}
                            <div class="col-md-12">
                                <p class="small">Coordinator of <em>{{coordinator_list}}</em></p>
                            </div>
                            {% endif %}
                            {% if responsibilities %}
                            <div class="col-md-12">
                                <p class="small"><em>{{responsibilities}}</em></p>
                            </div>
                            {% endif %}
                        </div>
                    </div>
                    <div class="col-md-2 col-xs-2">
                        {% if homepage %}
                        <a class="icon" href="{{homepage}}"><i class="fa fa-home {{item_css}}"></i></a>
                        {% endif %}
                        {% if scholar %}
                        <a class="icon" href="{{scholar}}"><i class="fa fa-google {{item_css}}"></i></a>
                        {% endif %}
                        {% if linkedin %}
                        <a class="icon" href="{{linkedin}}"><i class="fa fa-linkedin {{item_css}}"></i></a>
                        {% endif %}
                        {% if email %}
                        <a class="icon" href="mailto:{{email}}"><i class="fa fa-envelope-o {{item_css}}"></i></a>
                        {% endif %}
                    </div>
                </div>
            </div>
        """},
    'person-item-template': """
        <h4><strong>{{firstname}} {{lastname}}</strong></h4>
        {% if title %}
            <p class="text-muted">
                {{title}}
            </p>
        {% endif %}
        <div class="row">
            <div class="col-md-10">
                {% if coordinator_list %}
                <p>Coordinator of <em>{{coordinator_list}}</em></p>
                {% endif %}
                {% if responsibilities %}
                <p class="small text-muted">Responsibilities: {{responsibilities}}</p>
                {% endif %}
                {% if affiliation_title %}
                <p class="small">
                    {% if affiliation_url %}<a class="text" href="{{affiliation_url}}">{% endif %}
                    {{affiliation_title}}{% if affiliation_department %}, <br><em>{{affiliation_department}}</em>{% endif %}
                    {% if affiliation_url %}</a>{% endif %}
                </p>
                {% endif %}
                <p>
                    {% if homepage %}
                    <a class="icon" href="{{homepage}}"><i class="text-muted fa fa-home"></i></a>
                    {% endif %}
                    {% if scholar %}
                    <a class="icon" href="{{scholar}}"><i class="text-muted fa fa-google"></i></a>
                    {% endif %}
                    {% if email %}
                    <a class="icon" href="mailto:{{email}}"><i class="text-muted fa fa-envelope-o"></i></a>
                    {% endif %}
                </p>
            </div>
            <div class="col-md-2">
                {% if photo %}
                <img class="img img-rounded" src="{{site_url}}/{{ photo }}" alt="{{firstname}} {{lastname}}" height="120px" width="120px">
                {% endif %}
            </div>
        </div>
    """,
    'data-source': None,
    'set': None,
    'show': False,
    'template-variable': False,
    'person-firstname': None,
    'person-lastname': None,
    'sort': False,
    'fields': '',
    'site-url': ''
}

bpersonnel_settings = copy.deepcopy(bpersonnel_default_settings)


def load_personnel_registry(source):
    """

    :param source: filename of the data file
    :return: personnel registry
    """

    if source and os.path.isfile(source):
        try:
            with open(source, 'r') as field:
                personnel_registry = yaml.load(field)

            if 'data' in personnel_registry:
                personnel_registry = personnel_registry['data']
            personnel_data = collections.OrderedDict()
            set_data = collections.OrderedDict()
            if 'personnel' in personnel_registry:
                for item in personnel_registry['personnel']:
                    for field in item:
                        if field.endswith('_list'):
                            if not isinstance(item[field], list):
                                item[field] = [x.strip() for x in item[field].split(';')]

                            field_list = []
                            for i in item[field]:
                                parts = [x.strip() for x in i.split(',')]
                                if len(parts) == 2:
                                    field_list.append('<a class="text" href="' + parts[1] + '">' + parts[0] + '</a>')
                                else:
                                    field_list.append(parts[0])
                            item[field] = ', '.join(field_list)
                    personnel_data[item['lastname'].lower() + '-' + item['firstname'].lower()] = item

            if 'sets' in personnel_registry:
                set_data = collections.OrderedDict()
                for set in personnel_registry['sets']:
                    set_dict = collections.OrderedDict()
                    for item in personnel_registry['sets'][set]:
                        key = item['lastname'].lower() + '-' + item['firstname'].lower()
                        if key in personnel_data:
                            data = copy.deepcopy(personnel_data[key])
                            data.update(item)
                            item.update(data)
                            for field in item:
                                if field.endswith('_list'):
                                    if not isinstance(item[field], list):
                                        item[field] = [x.strip() for x in item[field].split(';')]

                                    field_list = []
                                    for i in item[field]:
                                        parts = [x.strip() for x in i.split(',')]
                                        if len(parts) == 2:
                                            field_list.append('<a class="text" href="' + parts[1] + '">' + parts[0] + '</a>')
                                        else:
                                            field_list.append(parts[0])

                                    item[field] = ', '.join(field_list)
                            set_dict[item['lastname'].lower() + '-' + item['firstname'].lower()] = item
                        else:
                            logger.warn('`pelican-bpersonnel` failed to form set [{set}], person not found [firstname={firstname} ,lastname={lastname}]'.format(
                                set=set,
                                firstname=item['firstname'],
                                lastname=item['lastname']
                            ))
                            return False
                    set_data[set] = set_dict
            return {
                'personnel': personnel_data,
                'sets': set_data
            }

        except ValueError:
            logger.warn('`pelican-bpersonnel` failed to load file [' + str(source) + ']')
            return False

    else:
        logger.warn('`pelican-bpersonnel` failed to load file [' + str(source) + ']')
        return False


def get_attribute(attrs, name, default=None):
    """
    Get div attribute
    :param attrs: attribute dict
    :param name: name field
    :param default: default value
    :return: value
    """

    if 'data-'+name in attrs:
        return attrs['data-'+name]
    else:
        return default


def generate_person_card(settings):
    """
    Generate individual personnel card

    :param settings: settings dict
    :return: html content
    """

    personnel_registry = load_personnel_registry(source=settings['data-source'])

    if personnel_registry:
        if settings['set'] and 'sets' in personnel_registry and settings['set'] in personnel_registry['sets']:
            person_data = personnel_registry['sets'][settings['set']][settings['person-lastname'].lower() + '-' + settings['person-firstname'].lower()]
        else:
            person_data = personnel_registry['personnel'][settings['person-lastname'].lower() + '-' + settings['person-firstname'].lower()]

        valid_fields = [u'firstname', u'lastname']  # default fields
        valid_fields += settings['fields']  # user defined fields

        filtered_fields = {}
        for field in person_data:
            if field in valid_fields:
                filtered_fields[field] = person_data[field]
            else:
                filtered_fields[field] = None

        template = Template(settings['person-item-template'].strip('\t\r\n').replace('&gt;', '>').replace('&lt;', '<'))

        filtered_fields['site_url'] = settings['site-url']
        html = BeautifulSoup(template.render(**filtered_fields), "html.parser")
        return html
    else:
        return ''


def generate_listing(settings):
    """
    Generate personnel listing

    :param settings: settings dict
    :return: html content
    """

    personnel_registry = load_personnel_registry(source=settings['data-source'])
    if personnel_registry and 'personnel' in personnel_registry and personnel_registry['personnel']:
        if 'sets' in personnel_registry and settings['set'] in personnel_registry['sets']:
            personnel = personnel_registry['sets'][settings['set']]
        else:
            personnel = personnel_registry['personnel']

        if settings['sort']:
            personnel = collections.OrderedDict(sorted(personnel.items()))

        html = "\n"
        main_highlight = False
        for person_key, person in personnel.iteritems():
            if 'main' in person and person['main']:
                html += generate_listing_item(person=person, settings=settings) + "\n"
                main_highlight = True

        for person_key, person in personnel.iteritems():
            if not 'main' in person or ('main' in person and not person['main']):
                html += generate_listing_item(person=person, settings=settings, main_highlight=main_highlight) + "\n"

        html += "\n"

        template = Template(settings['template'][settings['mode']].strip('\t\r\n').replace('&gt;', '>').replace('&lt;', '<'))

        return BeautifulSoup(template.render(list=html,
                                             header=settings.get('header'),
                                             site_url=settings.get('site-url'),
                                             panel_color=settings.get('panel-color'),), "html.parser")
    else:
        return ''


def generate_listing_item(person, settings, main_highlight=False):
    """

    Generate person in listing

    :param person: person data
    :param settings: settings dict
    :return: html content
    """
    if main_highlight:
        if settings['mode'] == 'panel':
            if 'main' in person and person['main']:
                item_css = 'active'
            else:
                item_css = ''
        else:
            if 'main' in person and person['main']:
                item_css = ''
            else:
                item_css = 'text-muted'
    else:
        item_css = ''

    valid_fields = [u'firstname', u'lastname']  # default fields
    valid_fields += settings['fields']          # user defined fields

    filtered_fields = {}
    for field in person:
        if field in valid_fields:
            filtered_fields[field] = person[field]
        else:
            filtered_fields[field] = None

    template = Template(settings['item-template'][settings['mode']].strip('\t\r\n').replace('&gt;', '>').replace('&lt;', '<'))
    filtered_fields['site_url'] = settings['site-url']
    filtered_fields['item_css'] = item_css

    html = BeautifulSoup(template.render(**filtered_fields), "html.parser")
    return html.decode()


def bpersonnel(content):
    """
    Main processing

    """
    global bpersonnel_settings

    if isinstance(content, contents.Static):
        return

    soup = BeautifulSoup(content._content, 'html.parser')

    # Template variable
    if bpersonnel_settings['template-variable']:
        # We have page variable set
        bpersonnel_settings['show'] = True
        div_html = generate_listing(settings=bpersonnel_settings)
        if div_html:
            content.bpersonnel = div_html.decode()
    else:
        content.bpersonnel = None

    # bpersonnel divs
    bpersonnel_divs = soup.find_all('div', class_='bpersonnel')
    bpersonnel_item_divs = soup.find_all('div', class_='bpersonnel-item')

    if bpersonnel_divs:
        bpersonnel_settings['show'] = True
        for bpersonnel_div in bpersonnel_divs:
            # We have div in the page
            settings = copy.deepcopy(bpersonnel_settings)
            settings['data-source'] = get_attribute(bpersonnel_div.attrs, 'yaml', bpersonnel_settings['data-source'])
            settings['set'] = get_attribute(bpersonnel_div.attrs, 'set', bpersonnel_settings['set'])
            settings['template'] = get_attribute(bpersonnel_div.attrs, 'template', bpersonnel_settings['template'])
            settings['item-template'] = get_attribute(bpersonnel_div.attrs, 'item-template', bpersonnel_settings['item-template'])
            settings['mode'] = get_attribute(bpersonnel_div.attrs, 'mode', bpersonnel_settings['mode'])
            settings['header'] = get_attribute(bpersonnel_div.attrs, 'header', bpersonnel_settings['header'])
            settings['panel-color'] = get_attribute(bpersonnel_div.attrs, 'panel-color', bpersonnel_settings['panel-color'])
            settings['fields'] = get_attribute(bpersonnel_div.attrs, 'fields', bpersonnel_settings['fields'])
            settings['fields'] = [x.strip() for x in settings['fields'].split(',')]
            if not isinstance(settings['fields'], list):
                settings['fields'] = [x.strip() for x in settings['fields'].split(',')]
            settings['sort'] = get_attribute(bpersonnel_div.attrs, 'sort', bpersonnel_settings['sort'])
            if settings['sort'] == 'True' or settings['sort'] == 'true':
                settings['sort'] = True
            else:
                settings['sort'] = False

            div_html = generate_listing(settings=settings)
            if div_html:
                bpersonnel_div.replaceWith(div_html)

    # bpersonnel card divs
    if bpersonnel_item_divs:
        bpersonnel_settings['show'] = True
        for bpersonnel_card_div in bpersonnel_item_divs:
            # We have div in the page
            settings = copy.deepcopy(bpersonnel_settings)
            settings['data-source'] = get_attribute(bpersonnel_card_div.attrs, 'yaml', bpersonnel_settings['data-source'])
            settings['set'] = get_attribute(bpersonnel_card_div.attrs, 'set', bpersonnel_settings['set'])
            settings['template'] = get_attribute(bpersonnel_card_div.attrs, 'template', bpersonnel_settings['template'])
            settings['item-template'] = get_attribute(bpersonnel_card_div.attrs, 'item-template', bpersonnel_settings['item-template'])
            settings['mode'] = get_attribute(bpersonnel_card_div.attrs, 'mode', bpersonnel_settings['mode'])
            settings['header'] = get_attribute(bpersonnel_card_div.attrs, 'header', bpersonnel_settings['header'])
            settings['panel-color'] = get_attribute(bpersonnel_card_div.attrs, 'panel-color', bpersonnel_settings['panel-color'])
            settings['person-firstname'] = get_attribute(bpersonnel_card_div.attrs, 'person-firstname', bpersonnel_settings['person-firstname'])
            settings['person-lastname'] = get_attribute(bpersonnel_card_div.attrs, 'person-lastname', bpersonnel_settings['person-lastname'])
            settings['fields'] = get_attribute(bpersonnel_card_div.attrs, 'fields', bpersonnel_settings['fields'])
            if not isinstance(settings['fields'], list):
                settings['fields'] = [x.strip() for x in settings['fields'].split(',')]

            div_html = generate_person_card(settings=settings)
            if div_html:
                bpersonnel_card_div.replaceWith(div_html)

    content._content = soup.decode()


def process_page_metadata(generator, metadata):
    """
    Process page metadata

    """
    global bpersonnel_default_settings, bpersonnel_settings
    bpersonnel_settings = copy.deepcopy(bpersonnel_default_settings)

    if u'bpersonnel' in metadata and (metadata['bpersonnel'] == 'True' or metadata['bpersonnel'] == 'true'):
        bpersonnel_settings['show'] = True
        bpersonnel_settings['template-variable'] = True
    else:
        bpersonnel_settings['show'] = False
        bpersonnel_settings['template-variable'] = False

    if u'bpersonnel_source' in metadata:
        bpersonnel_settings['data-source'] = metadata['bpersonnel_source']

    if u'bpersonnel_set' in metadata:
        bpersonnel_settings['set'] = metadata['bpersonnel_set']

    if u'bpersonnel_mode' in metadata:
        bpersonnel_settings['mode'] = metadata['bpersonnel_mode']

    if u'bpersonnel_panel_color' in metadata:
        bpersonnel_settings['panel-color'] = metadata['bpersonnel_panel_color']

    if u'bpersonnel_header' in metadata:
        bpersonnel_settings['header'] = metadata['bpersonnel_header']

    if u'bpersonnel_fields' in metadata:
        bpersonnel_settings['fields'] = metadata['bpersonnel_fields']
        bpersonnel_settings['fields'] = [x.strip() for x in bpersonnel_settings['fields'].split(',')]

    if u'bpersonnel_sort' in metadata and (metadata['bpersonnel_sort'] == 'True' or metadata['bpersonnel_sort'] == 'true'):
        bpersonnel_settings['sort'] = True


def init_default_config(pelican):
    """
    Handle settings from pelicanconf.py

    """
    global bpersonnel_default_settings, bpersonnel_settings

    bpersonnel_default_settings['site-url'] = pelican.settings['SITEURL']

    if 'BPERSONNEL_SOURCE' in pelican.settings:
        bpersonnel_default_settings['data-source'] = pelican.settings['BPERSONNEL_SOURCE']

    if 'BPERSONNEL_TEMPLATE' in pelican.settings:
        bpersonnel_default_settings['template'].update(pelican.settings['BPERSONNEL_TEMPLATE'])

    if 'BPERSONNEL_ITEM_TEMPLATE' in pelican.settings:
        bpersonnel_default_settings['item-template'].update(pelican.settings['BPERSONNEL_ITEM_TEMPLATE'])

    if 'BPERSONNEL_PERSON_ITEM_TEMPLATE' in pelican.settings:
        bpersonnel_default_settings['person-item-template'] = pelican.settings['BPERSONNEL_PERSON_ITEM_TEMPLATE']

    if 'BPERSONNEL_HEADER' in pelican.settings:
        bpersonnel_default_settings['header'] = pelican.settings['BPERSONNEL_HEADER']

    if 'BPERSONNEL_PANEL_COLOR' in pelican.settings:
        bpersonnel_default_settings['panel-color'] = pelican.settings['BPERSONNEL_PANEL_COLOR']

    if 'BPERSONNEL_SORT' in pelican.settings:
        bpersonnel_default_settings['sort'] = pelican.settings['BPERSONNEL_SORT']

    bpersonnel_settings = copy.deepcopy(bpersonnel_default_settings)


def register():
    """
    Register signals

    """

    signals.initialized.connect(init_default_config)
    signals.article_generator_context.connect(process_page_metadata)
    signals.page_generator_context.connect(process_page_metadata)

    signals.content_object_init.connect(bpersonnel)
