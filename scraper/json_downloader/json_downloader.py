# -*- coding: utf-8 -*-
"""
Script that downloads json responses from individual grailed.com api pages.
A cookie and user agent string need to be provided to scraper user data.

This requires cfscrape, which requires a Javascript engine to be installed.
We used nodejs.
"""
import cfscrape
import json
import time

USER_AGENT = 'REDACTED'
COOKIE = 'REDACTED'
HOST = 'www.grailed.com'
NEXT_INDEX_FILENAME = 'next_index'
API_FORMAT = 'https://www.grailed.com/api/{}/{}'
MAX_INDEX = 500000


def download_data_for_id(data_type, id, json_dir):
    uri = API_FORMAT.format(data_type, id)
    print 'Attempting to scrape: {}'.format(uri)

    headers = {
        'User-Agent': USER_AGENT,
        'Cookie': COOKIE,
        'Host': HOST,
    }

    try:
        scraper = cfscrape.create_scraper()
        data = scraper.get(uri, headers=headers).content
        data_dict = json.loads(data)

        with open('{}/{}.json'.format(json_dir, id), 'w') as data_file:
            data_file.write(json.dumps(data_dict))

    except ValueError:
        print 'Error with {}'.format(uri)

def run_downloader():
    with open('next_index') as next_index_file:
        next_index = int(next_index_file.read())

    curr_index = next_index
    for id in xrange(next_index, MAX_INDEX):
        download_data_for_id('listings', id, 'downloaded_listing_json')
        time.sleep(5)

        curr_index += 1
        with open(NEXT_INDEX_FILENAME, 'w') as next_index_file:
            next_index_file.write(str(curr_index))

if __name__ == '__main__':
    run_downloader()
