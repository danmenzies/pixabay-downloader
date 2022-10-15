# Searches and downloads files from Pixabay.com

import os
import csv
import json
import time
import os.path
import requests
import urllib.parse
import urllib.request
from slugify import slugify
from dotenv import load_dotenv


class Pixabay:
    """
    Searches and downloads files from Pixabay.com
    """

    def __init__(self):
        """
        Searches and downloads files from Pixabay.com
        """

        # Set up paths
        self.__asset_path = './data/'

        # Collect the API Key
        load_dotenv('./config/.env')
        self.__api_key = os.getenv('PIXABAY_API_KEY')

        # Create a User Agent, so we can use the API to retrieve images
        self.__user_agent = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive'
        }

        # Set up search parameter holders
        self.__orientation = ''
        self.__category = ''
        self.__min_width = ''
        self.__min_height = ''
        self.__search_type = ''
        self.__colors = ''

        # ...and build the search URL
        self.__search_url = \
            'https://pixabay.com/api/' \
                '?key={0}' \
                '&q={1}' \
                '&page={2}' \
                '&image_type={3}' \
                '&orientation={4}' \
                '&category={5}' \
                '&min_width={6}' \
                '&min_height={7}' \
                '&colors={8}' \
                '&safesearch=true' \
                '&per_page=200' \
                '&pretty=true'

    def set_search_params(self, orientation='all', category='', min_width=1000, min_height=1000, search_type='all', colors=''):
        """
        Sets the current search parameters
        :param orientation: Image orientation
        :param category: Image category
        :param min_width: Minimum width
        :param min_height: Minimum height
        :param search_type: Type of image to search for
        :param colors: Comma separated list of colors
        :return:
        """

        # Set the parameters
        self.__orientation = orientation
        self.__category = category
        self.__min_width = min_width
        self.__min_height = min_height
        self.__search_type = search_type

        # Tweak the orientation if needed
        if len(orientation) == 0:
            self.__orientation = 'all'

        elif orientation == 'h':
            self.__orientation = 'horizontal'

        elif orientation == 'v':
            self.__orientation = 'vertical'

        else:
            self.__orientation = 'all'

        # Set the category, if we don't have one
        if len(category) == 0:
            self.__category = 'all'

        # Set the minimum image size, if we don't have one
        if len(str(min_width)) == 0:
            self.__min_width = 1000

        if len(str(min_height)) == 0:
            self.__min_height = 1000

        # Tweak the search type if needed
        if len(search_type) == 0:
            self.__search_type = 'all'

        elif search_type == 'p':
            self.__search_type = 'photo'

        elif search_type == 'v':
            self.__search_type = 'vector'

        elif search_type == 'i':
            self.__search_type = 'illustration'

        # Set the colours, if we don't have any
        valid_colors = [
            'grayscale',
            'transparent',
            'red',
            'orange',
            'yellow',
            'green',
            'turquoise',
            'blue',
            'lilac',
            'pink',
            'white',
            'gray',
            'black',
            'brown'
        ]

        # Collect the passed colours
        color_list = colors.split(',')

        # Do we have a colour list?
        if len(colors) > 0:

            # Yes; check each one is valid
            for color in color_list:
                if color.strip() not in valid_colors:
                    color_list.remove(color)

            # ...and add them to the list of colours to pass to the API
            self.__colors = ','.join(color_list)
            self.__colors = self.__colors.replace(' ','').strip()

    def show_search_results(self, term='', orientation='all', category='', min_width=1000, min_height=1000, search_type='all', colors=''):
        """
        Show the results of a search
        :param term: Search term
        :param orientation: Image orientation [a|h|v]
        :param category: Image category
        :param min_width: Minimum width
        :param min_height: Minimum height
        :param search_type: Type of image to search for [a|p|i|v]
        :param colors: Comma separated list of colors
        :return:
        """

        # Set the search parameters
        self.set_search_params(
            orientation=orientation,
            category=category,
            min_width=min_width,
            min_height=min_height,
            search_type=search_type,
            colors=colors
        )

        # Build the search URL
        search_url = self.__search_url.format(
            self.__api_key,
            urllib.parse.quote(term, safe=''),
            1,
            self.__search_type,
            self.__orientation,
            self.__category,
            self.__min_width,
            self.__min_height,
            self.__colors
        )

        # Create a line gap
        print('')

        # Fetch the results
        response = requests.get(search_url)

        # Check the response
        if response.status_code == 200:

            # Decode the JSON
            json_data = json.loads(response.text)

            # Tell the user how many results we have
            if int(json_data['totalHits']) == 500:
                print("Found {0} images (the maximum available through the API)".format(json_data['totalHits']))

            else:
                print("Found {0} images".format(json_data['totalHits']))

            return True

        print("Failed to fetch search results, sorry.")
        return False

    def save_search_results(self, term='', orientation='all', category='', min_width=1000, min_height=1000, search_type='all', colors=''):
        """
        Saves the results of a search
        :param term: Search term
        :param orientation: Image orientation [a|h|v]
        :param category: Image category
        :param min_width: Minimum width
        :param min_height: Minimum height
        :param search_type: Type of image to search for [a|p|i|v]
        :param colors: Comma separated list of colors
        :return:
        """

        # Set the search parameters
        self.set_search_params(
            orientation=orientation,
            category=category,
            min_width=min_width,
            min_height=min_height,
            search_type=search_type,
            colors=colors
        )

        # Refine the keyword term
        web_term = urllib.parse.quote(term, safe='')
        slugified_term = slugify(str(term).strip())

        # Set up a place to hold the results
        if not os.path.exists(self.__asset_path.strip('/')):
            os.makedirs(self.__asset_path.strip('/'))

        if not os.path.exists(self.__asset_path + slugified_term):
            os.makedirs(self.__asset_path + slugified_term)

        save_path = self.__asset_path + slugified_term + '/'

        # Set up the image results holder
        image_results = []

        # Tell the user what we're doing
        print("")
        print("Collecting image data from Pixabay...")

        # Perform the actual search
        for page in range(1, 4):

            # Build the search URL
            search_url = self.__search_url.format(
                self.__api_key,
                web_term,
                page,
                self.__search_type,
                self.__orientation,
                self.__category,
                self.__min_width,
                self.__min_height,
                self.__colors
            )

            # Fetch the results
            search_results = requests.get(search_url).json()

            # Next, iterate through the search results
            for search_result in search_results['hits']:
                image_results.append(search_result)

            # Take a breath, so we don't hit the rate limiter
            time.sleep(1)

            print(' - Page {0} collected'.format(page))

        # Save the results
        with open(save_path + '__results.json', 'w') as json_file:
            json.dump(image_results, json_file, indent=2)

    def download_results(self, slugified_term=''):
        """
        Downloads images from a search result
        :param: Slug to use for sourcing and saving
        """

        print("")
        print("Downloading individual images...")

        # Set up the image save path
        save_path = self.__asset_path + slugified_term + '/'

        # Set up the credits CSV file
        if not os.path.exists(self.__asset_path + slugified_term + '/__credits.csv'):
            with open(self.__asset_path + slugified_term + '/__credits.csv', 'w', newline='') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow([
                    'IMAGE_SLUG',
                    'SOURCE_URL',
                    'AUTHOR',
                    'AUTHOR_URL'
                ])

        # Open the file holding the list of image results
        with open(self.__asset_path + slugified_term + '/__results.json') as json_file:
            image_results = json.load(json_file)

            # Iterate through the results
            for image_result in image_results:

                # Get the image data
                image_url = image_result['largeImageURL']
                source_url = image_result['pageURL']

                # Collect the author data
                author = image_result['user']
                author_url = 'https://pixabay.com/users/{0}-{1}/'.format(
                    author.replace(' ', '_').lower(),
                    image_result['user_id']
                )

                # Get the image format
                image_url_slug_split = image_url.split('/')
                image_url_slug = image_url_slug_split[len(image_url_slug_split) - 1]
                image_format = image_url_slug.split('.')[1]

                # Build the image slug
                source_url_slug = source_url.strip('/').split('/')
                source_url_slug = source_url_slug[len(source_url_slug) - 1]
                image_slug = source_url_slug + '.' + image_format

                # Confirm that the image doesn't already exist
                if os.path.exists(save_path + image_slug):
                    continue

                # Save the image
                remote_image = requests.get(url=image_url, headers=self.__user_agent)

                with open(save_path + image_slug, 'wb') as image_file:
                    image_file.write(remote_image.content)

                # Save the credits
                with open(self.__asset_path + slugified_term + '/__credits.csv', 'a', newline='') as csv_file:
                    csv_writer = csv.writer(csv_file)
                    csv_writer.writerow([
                        image_slug,
                        source_url,
                        author,
                        author_url
                    ])

                # Tell the user what's happening
                print(' - Saved {0}'.format(image_slug))

        print("")
        print("Downloads completed")