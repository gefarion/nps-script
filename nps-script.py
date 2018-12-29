#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import csv
import tempfile
import subprocess
import os
import sys

REGIONS = ('us', 'eu', 'jp', 'asia')

GAMES_TSV_FILENAME = '%s_GAMES.tsv'
GAMES_TSV_URL = 'https://nopaystation.com/tsv/%s_GAMES.tsv'

PKG2ZIP = 'pkg2zip'

PLATFORMS = {
    'psp': {
        'games': {
            'filename': GAMES_TSV_FILENAME % 'PSP',
            'url': GAMES_TSV_URL % 'PSP',
            'fieldnames': ('title_id', 'region', 'type', 'name', 'pkg_url', 'content_id',
                'last_modifcation_date', 'rap', 'download_rap_file', 'file_size', 'sha256')
        }
    },
    'psx': {
        'games': {
            'filename': GAMES_TSV_FILENAME % 'PSX',
            'url': GAMES_TSV_URL % 'PSX',
            'fieldnames': ('title_id', 'region', 'name', 'pkg_url', 'content_id',
                'last_modifcation_date', 'original_name', 'file_size', 'sha256')
        }
    },
    'psv': {
        'games': {
            'filename': GAMES_TSV_FILENAME % 'PSV',
            'url': GAMES_TSV_URL % 'PSV',
            'fieldnames': ('title_id', 'region', 'name', 'pkg_url', 'zrif', 'content_id',
                'last_modifcation_date', 'original_name', 'file_size', 'sha256', 'required_firmware', 'app_version')
        }
    },
}


def fmt_size(num, suffix='B'):
    try:
        num = int(num)
    except:
        return 'unknown size'

    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)


def fmt_item(item):
    return "[%s-%s] %s (%s)" % (
            item['region'], item['title_id'], item['name'], fmt_size(item['file_size'])
        )


def main(args):

    config = PLATFORMS[args.platform]['games']
    items = load_items(config, args)
    assert items

    if args.list:
        list_items(items, args)
    elif args.download:
        download_item(items, args)
    else:
        raise Exception("Use: --download TITLE_ID or --list")


def list_items(items, args):
    filter = args.filter.lower() if args.filter else None
    region = args.region.upper() if args.region else None

    print "[REGION-TITLE_ID] TITLE_NAME (FILE_SIZE)"
    for item in items:
        if filter and filter not in item['name'].lower():
            continue

        if region and region != item['region']:
            continue

        print fmt_item(item)

    return 0

def download_item(items, args):

    title_id = args.download
    if '-' in title_id:
        title_id = title_id[title_id.index('-') + 1:]

    try:
        item = [item for item in items if item['title_id'] == title_id][0]
    except:
        raise Exception('Item %s not found' % title_id)

    with tempfile.NamedTemporaryFile() as tmp:
        print 'Downloading: %s\n' % fmt_item(item)
        subprocess.check_call(["wget", item['pkg_url'], "-O", tmp.name])
        print 'Extracting pkg...\n'
        subprocess.check_call([PKG2ZIP, "-x", tmp.name, item.get('zrif', '')])


def load_items(config, args):

    if args.refresh or not os.path.isfile(config['filename']):
        print 'Downloading database from %s\n' % config['url']
        subprocess.check_call(["wget", config['url'], "-O", config['filename']])

    with open(config['filename']) as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=config['fieldnames'], delimiter='\t')
        # skip the header
        reader.next()
        return list(reader)


parser = argparse.ArgumentParser(description='A simple Python script to download games from https://nopaystation.com/')

parser.add_argument('--platform', '-p', type=str, required=True, choices=PLATFORMS.keys(), help='select the platform')

parser.add_argument('--download', '-d', type=str, required=False, help='download a game')

parser.add_argument('--list', '-l', action='store_true', help='list games')
parser.add_argument('--region', '-r', type=str, required=False, choices=REGIONS, help='filter games by region')
parser.add_argument('--filter', '-f', type=str, required=False, help='filter games by name')

parser.add_argument('--refresh', '-R', action='store_true', help='refresh NPS database')

main(parser.parse_args())
sys.exit(0)
