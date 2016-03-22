# This is a template for a Python scraper on morph.io (https://morph.io)
# including some code snippets below that you should find helpful

import re

import scraperwiki
import lxml.html

source_url = "http://www.parliament.go.tz/mps-list"
term = '5th Assembly'
html = scraperwiki.scrape(source_url)

root = lxml.html.fromstring(html)

trs = root.cssselect('tr.odd')

data = []

for tr in trs:
    member = {}
    member['image'] = tr.cssselect('img')[0].attrib.get('src')
    member['source'] = tr.cssselect('a')[0].attrib.get('href')
    member['id'] = member['source'].rsplit('/', 1)[1]

    tds = tr.cssselect('td')

    member['name'] = tds[1].cssselect('a')[0].text.strip()
    print member['name']
    member['area'] = tds[2].text.strip()
    member['group'] = tds[3].text.strip()

    member_html = scraperwiki.scrape(member['source'])
    member_root = lxml.html.fromstring(member_html)

    items = member_root.cssselect('span.item')

    item_dict = {}
    for item in items:
        key = re.sub(r'\s', '', item.text)
        value = item.tail.strip()
        item_dict[key] = value


    member['phone'] = item_dict['Phone:']
    member['email'] = item_dict['EmailAddress:']
    member['birth_date'] = item_dict['DateofBirth:']

    data.append(member)


scraperwiki.sqlite.save(unique_keys=['id'], data=data)