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

item1 = stac.create_item('../tests/data-files/S1A_20200103_17RMJ_ASC',
                         asset='local_incident_angle.vrt')

item2 = stac.create_item('../tests/data-files/S1B_20161121_12SYJ_ASC',
                         asset='local_incident_angle.vrt')

collection.add_items([item1, item2])

catalog.add_child(collection)
catalog.generate_subcatalogs(template='${year}')

catalog.normalize_hrefs('./')
# NOTE: can simplify after https://github.com/stac-utils/pystac/pull/565/files
#published_root_url = 'https://raw.githubusercontent.com/stactools-packages/sentinel1/main/examples/catalog.json'
#catalog.set_self_href(published_root_url) #manually change after saving
catalog.validate_all()
catalog.save()
