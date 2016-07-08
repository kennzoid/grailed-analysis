# -*- coding: utf-8 -*-
"""
This script ingests raw json downloaded from the Grailed API and 
adds them to an SQLite database using SQLAlchemy.
"""
import datetime
import json
import time

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Listing, Photo, User


LISTING_DATASET_FILE = 'raw_listing_json_dataset'
USER_DATASET_FILE = 'raw_user_json_dataset'


def parse_datetime(iso_string):
    if not iso_string:
        return None
    return datetime.datetime.strptime(iso_string, "%Y-%m-%dT%H:%M:%S.%fZ")


def parse_price_drops(pd_list):
    pd_string_list = [str(x) for x in pd_list]
    return ','.join(pd_string_list)


def add_listing_to_database(downloaded_json, session):
    try:
        data = json.loads(downloaded_json) 

        if 'error' in data or 'data' not in data:
            print 'Listing had no data field.'
            return

        actual_data = data['data']

        id = actual_data['id']

        photos = [
            Photo(
                id=photo['id'],
                url=photo['url'],
                width=photo['width'],
                height=photo['height'],
                image_api=photo['image_api'],
                rotate=photo['rotate'],
            )
            for photo in actual_data['photos']
        ]

        buyer_id = actual_data.get('buyer_id')
        if not buyer_id:
            buyer = None
        else:
            buyer = User(id=actual_data.get('buyer_id'))

        seller_id = actual_data['seller'].get('id')
        seller = User(id=actual_data['seller'].get('id'))

        # follower information isn't stored with the listing
        new_listing = Listing(
            id=id,
            title=actual_data.get('title'),
            created_at=parse_datetime(actual_data.get('created_at')),
            price=actual_data.get('price'),
            currency=actual_data.get('currency'),
            ship_cost=actual_data.get('ship_cost'),
            ship_to=actual_data.get('ship_to'),
            fee=actual_data.get('fee'),
            designer_name=actual_data.get('designer')['name'],
            designer_id=actual_data.get('designer')['id'],
            description=actual_data.get('description'),
            size=actual_data.get('size'),
            category=actual_data.get('category'),
            followed=actual_data.get('followed'),
            buy_now=actual_data.get('buy_now'),
            make_offer=actual_data.get('make_offer'),
            accept_binding_offers=actual_data.get('accept_binding_offers'),
            sold=actual_data.get('sold'),
            sold_price=actual_data.get('sold_price'),
            sold_at=parse_datetime(actual_data.get('sold_at')),
            dropped=actual_data.get('dropped'),
            price_drops=parse_price_drops(actual_data.get('price_drops')),
            price_updated_at=parse_datetime(actual_data.get('price_updated_at')),
            strata=actual_data.get('strata'),
            followers=[],
            follower_count=actual_data.get('follower_count'),
            photos=photos,
            num_photos=len(photos),
            buyer_id=buyer_id,
            buyer=buyer,
            seller_id=seller_id,
            seller=seller,
        )

        session.merge(new_listing)
        session.commit()

    except Exception as e:
        print 'Unhandled error: {}'.format(e.message)
        return None


def add_user_to_database(downloaded_json, session):
    try:
        data = json.loads(downloaded_json) 

        if 'error' in data or 'data' not in data:
            print 'User had no data field.'
            return

        actual_data = data['data']
        id = actual_data['id']

        # perform a query for the listing objects, this is slow but the alternative is very messy
        followed_listings = session.query(Listing).filter(Listing.id.in_(actual_data['followed_listings'])).all()
        seller_scores = actual_data['seller_score']
        buyer_scores = actual_data['buyer_score']
        purchase_count = buyer_scores.get('purchase_count', 0)
        sold_count = seller_scores.get('sold_count', 0)

        new_user_values = { 
            'id': id,
            'username': actual_data.get('username'),
            'height': actual_data.get('height'),
            'weight': actual_data.get('weight'),
            'location': actual_data.get('location'),
            'purchase_count': purchase_count,
            'would_sell_to_again_count': buyer_scores.get('would_sell_to_again_count'),
            'sold_count': sold_count,
            'would_buy_from_again_count': seller_scores.get('would_buy_from_again_count'),
            'item_as_described_average': seller_scores.get('item_as_described_average'),
            'fast_shipping_average': seller_scores.get('fast_shipping_average'),
            'communication_average': seller_scores.get('communication_average'),
            'seller_feedback_count': seller_scores.get('seller_feedback_count'),
            'transaction_count': purchase_count + sold_count,
            'listings_for_sale_count': actual_data.get('listings_for_sale_count'),
            'is_banned': actual_data.get('is_banned'),
            'is_blocked': actual_data.get('is_blocked'),
            'is_admin': actual_data.get('is_admin'),
            'is_curator': actual_data.get('is_curator'),
        }

        user_query = session.query(User).filter(User.id == id)
        if not user_query.count():
            new_user_values['following'] = followed_listings
            new_user = User(**new_user_values)
            session.merge(new_user)
        else:
            user_query.update(new_user_values)
            user = user_query.first()
            user.following.extend(followed_listings)

        session.commit()

    except Exception as e:
        print 'Unhandled error: {}'.format(e.message)
        session.rollback()
        raise


def import_json_datasets():
    engine = create_engine('sqlite:///grailed.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    # Ingest listings
    line_number = 0
    with open(LISTING_DATASET_FILE) as listing_dataset_file:
        for listing_json in listing_dataset_file.readlines():
            add_listing_to_database(listing_json, session)
            print 'Ingested line #{}'.format(line_number)
            line_number += 1

    # Ingest users
    line_number = 0
    with open(USER_DATASET_FILE) as user_dataset_file:
        for user_json in user_dataset_file:
            add_user_to_database(user_json, session)
            print 'Ingested line #{}'.format(line_number)
            line_number += 1

    session.close()


if __name__ == '__main__':
    import_json_datasets()
