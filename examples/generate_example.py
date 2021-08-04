#!/usr/bin/env python3
'''
Generate example STAC from test data
'''
from stactools.sentinel1 import stac
import pystac

catalog = pystac.Catalog(id='sentinel1-rtc-example',
                  description='Example Catalog: Analysis Ready Sentinel-1 Backscatter Imagery AWS Public Dataset',
                  title="Sentinel-1 RTC AWS Open Data",
                  catalog_type=pystac.CatalogType.RELATIVE_PUBLISHED)

collection = stac.create_collection()

base_href = 'https://sentinel-s1-rtc-indigo.s3.us-west-2.amazonaws.com'
key = 'tiles/RTC/1/IW/17/R/MJ/2020/S1A_20200103_17RMJ_ASC'
item1 = stac.create_item(f'{base_href}/{key}')

key = 'tiles/RTC/1/IW/12/S/YJ/2016/S1B_20161121_12SYJ_ASC'
item2 = stac.create_item(f'{base_href}/{key}')

collection.add_items([item1, item2])

catalog.add_child(collection)
catalog.generate_subcatalogs(template='${year}')

catalog.normalize_hrefs('./')
# NOTE: can simplify after https://github.com/stac-utils/pystac/pull/565/files
#published_root_url = 'https://raw.githubusercontent.com/stactools-packages/sentinel1/main/examples/catalog.json'
#catalog.set_self_href(published_root_url) # !!! manually change after saving !!!
catalog.validate_all()
catalog.save()
