import logging

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class Scraper(object):
    __slots__ = []

    _ecobee_object_name_to_url = {}
    _scraped_lines = []

    @classmethod
    def run(cls):
        cls.scrape_objects_and_urls()
        cls.scrap_object_properties()

    @classmethod
    def scrape_objects_and_urls(cls):
        response = requests.get('https://www.ecobee.com/home/developer/api/documentation/v1/auth/auth-intro.shtml')

        if response.status_code == requests.codes.ok:
            soup = BeautifulSoup(response.content, 'html.parser')
            objects_unordered_list = soup.select('ul.content-list.objects-content-list')[1]
            objects_list_items = objects_unordered_list.find_all('li')

            for object_list_item in objects_list_items[3:]:
                object_anchor = object_list_item.find_all('a')

                if object_anchor:
                    cls._ecobee_object_name_to_url[object_anchor[0].get_text().strip()] = '{0}{1}'.format(
                        'https://www.ecobee.com',
                        object_anchor[0]['href'])

    @classmethod
    def scrap_object_properties(cls):
        for ecobee_object_name in sorted(cls._ecobee_object_name_to_url):
            logger.debug('Scraping {0}'.format(ecobee_object_name))

            cls._scraped_lines.append('{0}\t{1}\n'.format(ecobee_object_name,
                                                          cls._ecobee_object_name_to_url[ecobee_object_name]))

            response = requests.get(cls._ecobee_object_name_to_url[ecobee_object_name])

            if response.status_code == requests.codes.ok:
                soup = BeautifulSoup(response.content, 'html.parser')
                object_tables = soup.select('table.content-table.object-table.last-par')

                for object_table in object_tables:
                    properties_header = object_table.find_previous_sibling('h3')

                    if properties_header and properties_header.get_text().strip() == 'Properties':
                        properties_table = object_table
                        break
                else:
                    logger.error('Failed to find Properties Table')
                    raise Exception

                properties_table_rows = properties_table.find_all('tr')

                for properties_table_row in properties_table_rows[1:]:  # Skip th
                    tab = ''
                    properties_line = []
                    properties_table_row_columns = properties_table_row.find_all('td')

                    for properties_table_row_column in properties_table_row_columns[:-1]:  # Skip Description Column
                        properties_line.append('{0}{1}'.format(tab, properties_table_row_column.get_text().strip()))
                        tab = '\t'

                    properties_line.append('\n')
                    cls._scraped_lines.append(''.join(properties_line))

        cls._scraped_lines.append('End\t//')

    @classmethod
    def get_scraped_lines(cls):
        return cls._scraped_lines
