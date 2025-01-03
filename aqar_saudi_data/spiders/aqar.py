import json
import os
from uuid import uuid4
import scrapy


class AqarSpider(scrapy.Spider):
    name = "aqar"
    allowed_domains = ["aqar.fm"]

    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'app-version': '0.20.44',
        'content-type': 'application/json',
        'dpr': '1.25',
        'origin': 'https://sa.aqar.fm',
        'priority': 'u=1, i',
        'referer': 'https://sa.aqar.fm/',
        'req-app': 'web',
        'req-device-token': str(uuid4()),
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
            url='https://sa.aqar.fm/graphql',
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
        for i in range(0, total, page_size)[:5]:
            json_data = self.generate_json_data(from_value=i, size_value=page_size)
            yield response.follow(
                url='https://sa.aqar.fm/graphql',
                method='POST',
                headers=self.headers,
                body=json.dumps(json_data),
                callback=self.parse,
                meta=self.meta,
            )

    def parse(self, response):
        self.logger.info(response.text)

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
