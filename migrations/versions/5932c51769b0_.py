"""empty message

Revision ID: 5932c51769b0
Revises: None
Create Date: 2016-02-07 22:46:26.786658

"""

# revision identifiers, used by Alembic.
revision = '5932c51769b0'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('members',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=128), nullable=True),
    sa.Column('last_name', sa.String(length=128), nullable=True),
    sa.Column('address_1', sa.String(length=128), nullable=True),
    sa.Column('city', sa.String(length=128), nullable=True),
    sa.Column('state', sa.String(length=128), nullable=True),
    sa.Column('postal_code', sa.String(length=128), nullable=True),
    sa.Column('country', sa.String(length=128), nullable=True),
    sa.Column('phone', sa.String(length=128), nullable=True),
    sa.Column('email', sa.String(length=128), nullable=True),
    sa.Column('stripe_customer_id', sa.String(length=128), nullable=True),
    sa.Column('member_since', sa.DateTime(), nullable=True),
    sa.Column('member_type', sa.String(length=128), nullable=True),
    sa.Column('member_expires', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('first_name'),
    sa.UniqueConstraint('last_name')
    )
    op.create_table('stripe_payments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('charge_id', sa.String(length=128), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('amount', sa.Integer(), nullable=True),
    sa.Column('fee', sa.Integer(), nullable=True),
    sa.Column('amount_refunded', sa.Integer(), nullable=True),
    sa.Column('status', sa.String(length=128), nullable=True),
    sa.Column('customer_id', sa.String(length=128), nullable=True),
    sa.Column('customer_email', sa.String(length=128), nullable=True),
    sa.Column('captured', sa.Boolean(), nullable=True),
    sa.Column('refunded', sa.Boolean(), nullable=True),
    sa.Column('card_id', sa.String(length=128), nullable=True),
    sa.Column('card_last_4', sa.String(length=128), nullable=True),
    sa.Column('card_brand', sa.String(length=128), nullable=True),
    sa.Column('card_expiration_month', sa.SmallInteger(), nullable=True),
    sa.Column('card_expiration_year', sa.SmallInteger(), nullable=True),
    sa.Column('card_name', sa.String(length=128), nullable=True),
    sa.Column('card_address', sa.String(length=128), nullable=True),
    sa.Column('card_address_city', sa.String(length=128), nullable=True),
    sa.Column('card_address_state', sa.String(length=128), nullable=True),
    sa.Column('card_address_country', sa.String(length=128), nullable=True),
    sa.Column('card_address_zip', sa.String(length=128), nullable=True),
    sa.Column('card_fingerprint', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=80), nullable=False),
    sa.Column('email', sa.String(length=80), nullable=False),
    sa.Column('password', sa.String(length=128), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('first_name', sa.String(length=30), nullable=True),
    sa.Column('last_name', sa.String(length=30), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('roles')
    op.drop_table('users')
    op.drop_table('stripe_payments')
    op.drop_table('members')
    ### end Alembic commands ###
