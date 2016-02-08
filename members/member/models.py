# -*- coding: utf-8 -*-
"""Member models."""
import datetime as dt

from members.database import Column, Model, SurrogatePK, db, reference_col, relationship


class Member(SurrogatePK, Model):
    """A member of the organization."""

    __tablename__ = 'members'
    first_name = Column(db.String(128), unique=True, nullable=True)
    last_name = Column(db.String(128), unique=True, nullable=True)
    address_1 = Column(db.String(128), nullable=True)
    city = Column(db.String(128), nullable=True)
    state = Column(db.String(128), nullable=True)
    postal_code = Column(db.String(128), nullable=True)
    country = Column(db.String(128), nullable=True)
    phone = Column(db.String(128), nullable=True)
    email = Column(db.String(128), nullable=True)

    stripe_customer_id = Column(db.String(128), nullable=True)

    member_since = Column(db.DateTime, nullable=True)
    member_type = Column(db.String(128), nullable=True)
    member_expires = Column(db.DateTime, nullable=True)

    @classmethod
    def find_by_email(self, email):
        return self.query.filter_by(email=email).first()

    @classmethod
    def find_by_customer_id(self, customer_id):
        return self.query.filter_by(stripe_customer_id=customer_id).first()


class StripePayment(SurrogatePK, Model):
    """A Stripe payment from a member."""

    __tablename__ = 'stripe_payments'
    charge_id = Column(db.String(128), nullable=False)
    created_at = Column(db.DateTime, nullable=True)
    amount = Column(db.Integer, nullable=True)
    fee = Column(db.Integer, nullable=True)
    amount_refunded = Column(db.Integer, nullable=True)
    status = Column(db.String(128), nullable=True)
    customer_id = Column(db.String(128), nullable=True)
    customer_email = Column(db.String(128), nullable=True)
    captured = Column(db.Boolean, nullable=True)
    refunded = Column(db.Boolean, nullable=True)
    card_id = Column(db.String(128), nullable=True)
    card_last_4 = Column(db.String(128), nullable=True)
    card_brand = Column(db.String(128), nullable=True)
    card_expiration_month = Column(db.SmallInteger, nullable=True)
    card_expiration_year = Column(db.SmallInteger, nullable=True)
    card_name = Column(db.String(128), nullable=True)
    card_address = Column(db.String(128), nullable=True)
    card_address_city = Column(db.String(128), nullable=True)
    card_address_state = Column(db.String(128), nullable=True)
    card_address_country = Column(db.String(128), nullable=True)
    card_address_zip = Column(db.String(128), nullable=True)
    card_fingerprint = Column(db.String(128), nullable=True)
