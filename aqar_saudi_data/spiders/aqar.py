import json
import os
import scrapy
from aqar_saudi_data.items import AqarItem, AqarItemLoader
BASE_URL = 'https://sa.aqar.fm'

class AqarSpider(scrapy.Spider):
    name = "aqar"
    allowed_domains = ["aqar.fm"]

    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'app-version': '0.20.44',
        'content-type': 'application/json',
        'dpr': '1.25',
        'origin': BASE_URL,
        'priority': 'u=1, i',
        'referer': BASE_URL,
        'req-app': 'web',
    }

    meta = {
        "zyte_api_automap": {
            "geolocation": "DE",
            "device": "desktop",
            "httpResponseBody": True,
        },
    }

    def start_requests(self):
        json_data = self.generate_json_data(from_value=0, size_value=0)
        yield scrapy.Request(
            url=f'{BASE_URL}/graphql',
            method='POST',
            headers=self.headers,
            body=json.dumps(json_data),
            callback=self.parse_total,
            meta=self.meta,
        )

    def parse_total(self, response):
        data = json.loads(response.text)
        total = data.get('data', {}).get('Web', {}).get('find', {}).get('total', 0)
        self.logger.info(f'Total listings: {total}')

        if total == 0:
            self.logger.error('Unable to retrieve listings')
            return

        page_size = int(os.getenv('PAGE_SIZE', 20))
        for i in range(0, total, page_size):
            json_data = self.generate_json_data(from_value=i, size_value=page_size)
            yield response.follow(
                url=f'{BASE_URL}/graphql',
                method='POST',
                headers=self.headers,
                body=json.dumps(json_data),
                callback=self.parse,
                meta=self.meta,
            )

    def parse(self, response):
        data = json.loads(response.text)
        for listing in data.get('data', {}).get('Web', {}).get('find', {}).get('listings', []):
            loader = AqarItemLoader(item=AqarItem())
            
            # Basic Information
            loader.add_value('id', listing.get('id'))
            loader.add_value('url', f'{BASE_URL}{listing.get("path")}')
            loader.add_value('title', listing.get('title'))
            loader.add_value('description', listing.get('content'))
            loader.add_value('category', listing.get('path', '').strip('/').split('/')[0] if listing.get('path') else None)
            loader.add_value('category_id', listing.get('category'))
            loader.add_value('type', listing.get('type'))
            loader.add_value('status', listing.get('status'))
            loader.add_value('create_time', listing.get('create_time'))
            loader.add_value('last_update', listing.get('last_update'))
            loader.add_value('refresh', listing.get('refresh'))
            loader.add_value('published_at', listing.get('published_at'))
            
            # Location Information
            loader.add_value('address', listing.get('address'))
            loader.add_value('city', listing.get('city'))
            loader.add_value('city_id', listing.get('city_id'))
            loader.add_value('district', listing.get('district'))
            loader.add_value('district_id', listing.get('district_id'))
            loader.add_value('direction', listing.get('direction'))
            loader.add_value('direction_id', listing.get('direction_id'))
            loader.add_value('province_id', listing.get('province_id'))
            location = listing.get('location', {})
            loader.add_value('latitude', location.get('lat'))
            loader.add_value('longitude', location.get('lng'))
            loader.add_value('street_width', listing.get('street_width'))
            loader.add_value('street_direction', listing.get('street_direction'))
            
            # Property Details
            loader.add_value('area', listing.get('area'))
            loader.add_value('price', listing.get('price'))
            loader.add_value('rent_period', listing.get('rent_period'))
            loader.add_value('property_age', listing.get('age'))
            loader.add_value('rooms', listing.get('rooms'))
            loader.add_value('bedrooms', listing.get('beds'))
            loader.add_value('bathrooms', listing.get('wc'))
            loader.add_value('halls', listing.get('livings'))
            loader.add_value('furnished', listing.get('furnished'))
            loader.add_value('kitchen', listing.get('ketchen'))
            loader.add_value('ac', listing.get('ac'))
            
            # Additional Features
            loader.add_value('parking', listing.get('car_entrance'))
            loader.add_value('family', listing.get('family'))
            loader.add_value('duplex', listing.get('duplex'))
            loader.add_value('basement', listing.get('basement'))
            loader.add_value('driver_room', listing.get('driver'))
            loader.add_value('maid_room', listing.get('maid'))
            loader.add_value('pool', listing.get('pool'))
            loader.add_value('elevator', listing.get('lift'))
            loader.add_value('tent', listing.get('tent'))
            loader.add_value('yard', listing.get('backyard'))
            
            # Property Documents
            loader.add_value('deed_number', listing.get('deed_number'))
            loader.add_value('plan_no', listing.get('plan_no'))
            
            # Utilities
            loader.add_value('water_availability', listing.get('water_availability'))
            loader.add_value('electrical_availability', listing.get('electrical_availability'))
            loader.add_value('drainage_availability', listing.get('drainage_availability'))
            
            # Additional Features
            loader.add_value('private_roof', listing.get('private_roof'))
            loader.add_value('apartment_in_villa', listing.get('apartment_in_villa'))
            loader.add_value('two_entrances', listing.get('two_entrances'))
            loader.add_value('special_entrance', listing.get('special_entrance'))
            
            yield loader.load_item()

    def generate_json_data(self, from_value=0, size_value=0):
        json_data = {
            'operationName': 'findListings',
            'variables': {
                'size': size_value,
                'from': from_value,
                'sort': {
                    'create_time': 'desc',
                    'has_img': 'desc',
                },
                'where': {},
            },
            'query': 'fragment WebResult on WebResults {\n  total\n  listings {\n    id\n    rnpl_monthly_price\n    sov_campaign_id\n    boosted\n    ac\n    age\n    apts\n    area\n    backyard\n    basement\n    beds\n    car_entrance\n    category\n    city_id\n    create_time\n    biddable\n    published_at\n    direction_id\n    district_id\n    province_id\n    driver\n    duplex\n    extra_unit\n    family\n    family_section\n    fb\n    fl\n    furnished\n    has_img\n    imgs\n    imgs_desc\n    ketchen\n    last_update\n    refresh\n    lift\n    livings\n    location {\n      lat\n      lng\n      __typename\n    }\n    maid\n    men_place\n    meter_price\n    playground\n    pool\n    premium\n    price\n    price_2_payments\n    price_4_payments\n    price_12_payments\n    range_price\n    rent_period\n    rooms\n    stairs\n    stores\n    status\n    street_direction\n    street_width\n    tent\n    trees\n    type\n    user_id\n    user {\n      phone\n      name\n      img\n      type\n      paid\n      fee\n      review\n      iam_verified\n      rega_id\n      bml_license_number\n      bml_url\n      __typename\n    }\n    user_type\n    vb\n    wc\n    wells\n    women_place\n    has_video\n    videos {\n      video\n      thumbnail\n      orientation\n      __typename\n    }\n    verified\n    special\n    employee_user_id\n    mgr_user_id\n    unique_listing\n    advertiser_type\n    appraisal_id\n    appraisal\n    virtual_tour_link\n    project_id\n    approved\n    native {\n      logo\n      title\n      image\n      description\n      external_url\n      __typename\n    }\n    gh_id\n    private_listing\n    blur\n    location_circle_radius\n    width\n    length\n    water_availability\n    electrical_availability\n    drainage_availability\n    private_roof\n    apartment_in_villa\n    two_entrances\n    special_entrance\n    daily_rentable\n    has_extended_details\n    extended_details {\n      minimum_booking_days\n      __typename\n    }\n    hide_contact_details\n    ad_license_number\n    deed_number\n    rega_licensed\n    published\n    comments_enabled\n    content\n    address\n    district\n    direction\n    city\n    title\n    path\n    uri\n    range_price\n    original_range_price\n    plan_no\n    parcel_no\n    __typename\n  }\n  __typename\n}\n\nquery findListings($size: Int, $from: Int, $sort: SortInput, $where: WhereInput, $polygon: [LocationInput!], $daily_renting_filter: DailyRentingFilter) {\n  Web {\n    find(\n      size: $size\n      from: $from\n      sort: $sort\n      where: $where\n      polygon: $polygon\n      daily_renting_filter: $daily_renting_filter\n    ) {\n      ...WebResult\n      __typename\n    }\n    __typename\n  }\n}\n',
        }
        return json_data
