# -*- coding: utf-8 -*-
from datetime import datetime
from flask import Blueprint, request, current_app
from members.member.models import Member, StripePayment

blueprint = Blueprint('webhooks', __name__, url_prefix='/webhooks')


@blueprint.route('/stripe', methods=['POST'])
def stripe_hook():
    expected_handshake = current_app.config.get('HOOK_STRIPE_HANDSHAKE')
    actual_handshake = request.args.get('handshake')

    if expected_handshake != actual_handshake:
        return "Bad handshake", 400

    body = request.get_json()
    action = body['type']
    livemode = body['livemode']
    obj = body['data']['object']

    if not livemode:
        current_app.logger.info("Skipping webhook for test mode")
        return "OK", 200

    current_app.logger.info("Received Stripe webhook action: " + action)

    if action.startswith('charge.'):
        current_app.logger.info("Saving charge.* webhook")

        card = obj['card']
        StripePayment.create(
            charge_id=obj['id'],
            created_at=datetime.utcfromtimestamp(obj['created']),
            amount=obj['amount'],
            amount_refunded=obj['amount_refunded'],
            # fee=obj['fee'],
            status=obj['status'],
            customer_id=obj['customer'],
            customer_email=obj['receipt_email'],
            captured=obj['captured'],
            refunded=obj['refunded'],
            card_id=card['id'],
            card_last_4=card['last4'],
            card_brand=card['brand'],
            card_expiration_month=card['exp_month'],
            card_expiration_year=card['exp_year'],
            card_name=card['name'],
            card_address=card['address_line1'],
            card_address_city=card['address_city'],
            card_address_state=card['address_state'],
            card_address_country=card['address_country'],
            card_address_zip=card['address_zip'],
            card_fingerprint=card['fingerprint'],
        )

    if action == 'customer.created':
        member = Member.find_by_email(obj['email'])

        if member:
            current_app.logger.info("Customer created hook: existing member getting updated")

            member.update(
                stripe_customer_id=obj['id'],
            )
        else:
            current_app.logger.info("Customer created hook: new member getting created")

            Member.create(
                stripe_customer_id=obj['id'],
                email=obj['email'],
            )

    elif action == 'customer.subscription.created':
        member = Member.find_by_customer_id(obj['customer'])

        if member:
            current_app.logger.info("Subscription created hook: existing member getting updated")
            member.update(
                stripe_customer_id=obj['customer'],
                member_since=datetime.utcfromtimestamp(obj['start']),
                member_expires=datetime.utcfromtimestamp(obj['current_period_end']),
            )
        else:
            current_app.logger.info("Subscription created hook: new member getting created")
            Member.create(
                stripe_customer_id=obj['customer'],
                member_since=datetime.utcfromtimestamp(obj['start']),
                member_expires=datetime.utcfromtimestamp(obj['current_period_end']),
            )

    elif action == 'customer.subscription.updated':
        member = Member.find_by_customer_id(obj['customer'])

        if member:
            member.update(
                stripe_customer_id=obj['customer'],
                member_expires=datetime.utcfromtimestamp(obj['current_period_end']),
            )

    elif action == 'customer.subscription.deleted':
        member = Member.find_by_customer_id(obj['customer'])

        if member:
            current_app.logger.info("Subscription deleted hook: existing membership getting canceled")
            canceled_at = datetime.utcfromtimestamp(obj['canceled_at'])
            member.update(
                member_expires=canceled_at
            )
        else:
            current_app.logger.warn("Subscription deleted hook: existing membership not found")

    return "OK", 200


@blueprint.route('/wufoo', methods=['POST'])
def wufoo_hook():
    current_app.logger.info("Received Wufoo webhook: " + request.form)
    expected_handshake = current_app.config.get('HOOK_WUFOO_HANDSHAKE')
    actual_handshake = request.form['HandshakeKey']

    if expected_handshake != actual_handshake:
        return "Bad handshake", 400

    email = request.form['Field19']

    data_dict = {
        "first_name": request.form['Field15'],
        "last_name": request.form['Field16'],
        "address_1": request.form['Field3'],
        "city": request.form['Field5'],
        "state": request.form['Field6'],
        "postal_code": request.form['Field7'],
        "country": request.form['Field8'],
        "phone": request.form['Field10'],
        "email": request.form['Field19'],
        "member_type": request.form['Field24'],
    }

    member = Member.find_by_email(email)
    if member:
        member.update(
            **data_dict
        )
    else:
        Member.create(
            **data_dict
        )

    return "OK", 200
