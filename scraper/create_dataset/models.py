# -*- coding: utf-8 -*-
"""
This file declares the models used to create the SQLite database
for Grailed.com data.

Running the script will create the database file.
"""
from sqlalchemy import Boolean, Column, DateTime, Integer, Float, ForeignKey, String, Table
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


Base = declarative_base()


listings_user_follow = Table(
    'listings_user_follow',
    Base.metadata,
    Column('listing_id', Integer, ForeignKey('listings.id')),
    Column('user_id', Integer, ForeignKey('users.id'))
)


class Listing(Base):
    __tablename__ = 'listings'

    id = Column(Integer, index=True, unique=True, primary_key=True)
    title = Column(String)
    created_at = Column(DateTime)
    price = Column(Integer)
    currency = Column(String)
    ship_cost = Column(Integer)
    ship_to = Column(String)
    fee = Column(Float)
    designer_name = Column(String)
    designer_id = Column(Integer)
    description = Column(String)
    size = Column(String)
    category = Column(String)
    followed = Column(Boolean)

    buy_now = Column(Boolean)
    make_offer = Column(Boolean)
    accept_binding_offers = Column(Boolean)

    sold = Column(Boolean)
    sold_price = Column(Integer)
    sold_at = Column(DateTime)

    dropped = Column(Boolean)
    price_drops = Column(String)
    price_updated_at = Column(DateTime)

    strata = Column(String)

    followers = relationship('User', secondary=listings_user_follow, back_populates='following')
    follower_count = Column(Integer)
    buyer_id = Column(Integer, ForeignKey('users.id'))
    buyer = relationship('User', foreign_keys=[buyer_id], backref='bought')

    photos = relationship('Photo')
    num_photos = Column(Integer)

    seller_id = Column(Integer, ForeignKey('users.id'))
    seller = relationship('User', foreign_keys=[seller_id], backref='sold')


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, index=True, unique=True, primary_key=True)
    username = Column(String)
    height = Column(Integer)
    weight = Column(Integer)
    location = Column(String)

    # buyer score
    purchase_count = Column(Integer)
    would_sell_to_again_count = Column(Integer)

    # seller score
    sold_count = Column(Integer)
    would_buy_from_again_count = Column(Integer)
    item_as_described_average = Column(Float)
    fast_shipping_average = Column(Float)
    communication_average = Column(Float)
    seller_feedback_count = Column(Integer)

    transaction_count = Column(Integer)
    listings_for_sale_count = Column(Integer)
    unread_buying_count = Column(Integer)
    unread_selling_count = Column(Integer)

    # random shit
    is_banned = Column(Boolean)
    is_blocked = Column(Boolean)
    is_admin = Column(Boolean)
    is_curator = Column(Boolean)
    following = relationship('Listing', secondary=listings_user_follow, back_populates='followers')


class Photo(Base):
    __tablename__ = 'photos'
    id = Column(Integer, index=True, unique=True, primary_key=True)
    listing_id = Column(Integer, ForeignKey('listings.id'))
    url = Column(String)
    width = Column(Integer)
    height = Column(Integer)
    image_api = Column(String)
    rotate = Column(Integer)

if __name__ == '__main__':
    engine = create_engine('sqlite:///grailed.db')
    Base.metadata.create_all(engine)
