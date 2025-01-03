# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst
from scrapy.loader import ItemLoader

def clean_value(value):
    if value is None:
        return None
    if isinstance(value, str) and value.strip() == '':
        return None
    return value

def convert_to_int(value):
    value = clean_value(value)
    if value is None:
        return None
    try:
        return int(float(value))  # handle string float values
    except (ValueError, TypeError):
        return None

def convert_to_float(value):
    value = clean_value(value)
    if value is None:
        return None
    try:
        return float(value)
    except (ValueError, TypeError):
        return None

def clean_boolean(value):
    value = clean_value(value)
    if value is None:
        return None
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        value = value.lower().strip()
        if value in ['true', '1', 'yes']:
            return True
        if value in ['false', '0', 'no']:
            return False
        return None
    if isinstance(value, (int, float)):
        return bool(value)
    return None


class AqarItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


class AqarItem(scrapy.Item):
    fields_order = [
        # Basic Information
        'id',
        'url',
        'title',
        'description',
        'category',
        'category_id',
        'type',
        'status',
        'create_time',
        'last_update',
        'refresh',
        'published_at',
        
        # Location Information
        'address',
        'city',
        'city_id',
        'district',
        'district_id',
        'direction',
        'direction_id',
        'province_id',
        'latitude',
        'longitude',
        'street_width',
        'street_direction',
        
        # Property Details
        'area',
        'price',
        'rent_period',
        'property_age',
        'rooms',
        'bedrooms',
        'bathrooms',
        'halls',
        'furnished',
        'kitchen',
        'ac',
        
        # Additional Features
        'parking',
        'family',
        'duplex',
        'basement',
        'driver_room',
        'maid_room',
        'pool',
        'elevator',
        'tent',
        'yard',
        
        # Property Documents
        'deed_number',
        'plan_no',
        
        # Utilities
        'water_availability',
        'electrical_availability',
        'drainage_availability',
        
        # Additional Features
        'private_roof',
        'apartment_in_villa',
        'two_entrances',
        'special_entrance'
    ]

    # Basic Information
    id = scrapy.Field(
        input_processor=MapCompose(convert_to_int),
        output_processor=TakeFirst()
    )
    url = scrapy.Field(
        output_processor=TakeFirst()
    )
    title = scrapy.Field(
        output_processor=TakeFirst()
    )
    description = scrapy.Field(
        output_processor=TakeFirst()
    )
    category = scrapy.Field(
        output_processor=TakeFirst()
    )
    category_id = scrapy.Field(
        input_processor=MapCompose(convert_to_int),
        output_processor=TakeFirst()
    )
    type = scrapy.Field(
        input_processor=MapCompose(convert_to_int),
        output_processor=TakeFirst()
    )
    status = scrapy.Field(
        input_processor=MapCompose(convert_to_int),
        output_processor=TakeFirst()
    )
    create_time = scrapy.Field(
        input_processor=MapCompose(convert_to_int),
        output_processor=TakeFirst()
    )
    last_update = scrapy.Field(
        input_processor=MapCompose(convert_to_int),
        output_processor=TakeFirst()
    )
    refresh = scrapy.Field(
        input_processor=MapCompose(convert_to_int),
        output_processor=TakeFirst()
    )
    published_at = scrapy.Field(
        input_processor=MapCompose(convert_to_int),
        output_processor=TakeFirst()
    )
    
    # Location Information
    address = scrapy.Field(
        output_processor=TakeFirst()
    )
    city = scrapy.Field(
        output_processor=TakeFirst()
    )
    city_id = scrapy.Field(
        input_processor=MapCompose(convert_to_int),
        output_processor=TakeFirst()
    )
    district = scrapy.Field(
        output_processor=TakeFirst()
    )
    district_id = scrapy.Field(
        input_processor=MapCompose(convert_to_int),
        output_processor=TakeFirst()
    )
    direction = scrapy.Field(
        output_processor=TakeFirst()
    )
    direction_id = scrapy.Field(
        input_processor=MapCompose(convert_to_int),
        output_processor=TakeFirst()
    )
    province_id = scrapy.Field(
        input_processor=MapCompose(convert_to_int),
        output_processor=TakeFirst()
    )
    latitude = scrapy.Field(
        input_processor=MapCompose(convert_to_float),
        output_processor=TakeFirst()
    )
    longitude = scrapy.Field(
        input_processor=MapCompose(convert_to_float),
        output_processor=TakeFirst()
    )
    street_width = scrapy.Field(
        input_processor=MapCompose(convert_to_int),
        output_processor=TakeFirst()
    )
    street_direction = scrapy.Field(
        input_processor=MapCompose(convert_to_int),
        output_processor=TakeFirst()
    )
    
    # Property Details
    area = scrapy.Field(
        input_processor=MapCompose(convert_to_float),
        output_processor=TakeFirst()
    )
    price = scrapy.Field(
        input_processor=MapCompose(convert_to_float),
        output_processor=TakeFirst()
    )
    rent_period = scrapy.Field(
        input_processor=MapCompose(convert_to_int),
        output_processor=TakeFirst()
    )
    property_age = scrapy.Field(
        input_processor=MapCompose(convert_to_int),
        output_processor=TakeFirst()
    )
    rooms = scrapy.Field(
        input_processor=MapCompose(convert_to_int),
        output_processor=TakeFirst()
    )
    bedrooms = scrapy.Field(
        input_processor=MapCompose(convert_to_int),
        output_processor=TakeFirst()
    )
    bathrooms = scrapy.Field(
        input_processor=MapCompose(convert_to_int),
        output_processor=TakeFirst()
    )
    halls = scrapy.Field(
        input_processor=MapCompose(convert_to_int),
        output_processor=TakeFirst()
    )
    furnished = scrapy.Field(
        input_processor=MapCompose(convert_to_int),
        output_processor=TakeFirst()
    )
    kitchen = scrapy.Field(
        input_processor=MapCompose(convert_to_int),
        output_processor=TakeFirst()
    )
    ac = scrapy.Field(
        input_processor=MapCompose(convert_to_int),
        output_processor=TakeFirst()
    )
    
    # Additional Features
    parking = scrapy.Field(
        input_processor=MapCompose(convert_to_int),
        output_processor=TakeFirst()
    )
    family = scrapy.Field(
        input_processor=MapCompose(convert_to_int),
        output_processor=TakeFirst()
    )
    duplex = scrapy.Field(
        input_processor=MapCompose(convert_to_int),
        output_processor=TakeFirst()
    )
    basement = scrapy.Field(
        input_processor=MapCompose(convert_to_int),
        output_processor=TakeFirst()
    )
    driver_room = scrapy.Field(
        input_processor=MapCompose(convert_to_int),
        output_processor=TakeFirst()
    )
    maid_room = scrapy.Field(
        input_processor=MapCompose(convert_to_int),
        output_processor=TakeFirst()
    )
    pool = scrapy.Field(
        input_processor=MapCompose(convert_to_int),
        output_processor=TakeFirst()
    )
    elevator = scrapy.Field(
        input_processor=MapCompose(convert_to_int),
        output_processor=TakeFirst()
    )
    tent = scrapy.Field(
        input_processor=MapCompose(convert_to_int),
        output_processor=TakeFirst()
    )
    yard = scrapy.Field(
        input_processor=MapCompose(convert_to_int),
        output_processor=TakeFirst()
    )
    
    # Property Documents
    deed_number = scrapy.Field(
        output_processor=TakeFirst()
    )
    plan_no = scrapy.Field(
        output_processor=TakeFirst()
    )
    
    # Utilities
    water_availability = scrapy.Field(
        input_processor=MapCompose(clean_boolean),
        output_processor=TakeFirst()
    )
    electrical_availability = scrapy.Field(
        input_processor=MapCompose(clean_boolean),
        output_processor=TakeFirst()
    )
    drainage_availability = scrapy.Field(
        input_processor=MapCompose(clean_boolean),
        output_processor=TakeFirst()
    )
    
    # Additional Features
    private_roof = scrapy.Field(
        input_processor=MapCompose(clean_boolean),
        output_processor=TakeFirst()
    )
    apartment_in_villa = scrapy.Field(
        input_processor=MapCompose(clean_boolean),
        output_processor=TakeFirst()
    )
    two_entrances = scrapy.Field(
        input_processor=MapCompose(clean_boolean),
        output_processor=TakeFirst()
    )
    special_entrance = scrapy.Field(
        input_processor=MapCompose(clean_boolean),
        output_processor=TakeFirst()
    )
