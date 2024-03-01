from flask import Flask, Blueprint, request
import stripe
import os
from flask_cors import CORS

payment_controller = Blueprint('payment_controller', __name__)
stripe.api_key = os.getenv("STRIPE_API_KEY")
CORS(payment_controller)

YOUR_DOMAIN = 'http://localhost:5000'  # Change later



@payment_controller.route('/', methods=['GET'])
def get_success_message():
    return "all the payments"

@payment_controller.route('/payment/', methods=['POST'])
def make_payment():
    details = request.get_json()


@payment_controller.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    """
    request must have:
    - lookup_key

    :return:
    """
    payment_data = request.get_json()
    print(payment_data['lookup_key'])

    print(stripe.api_key)
    prices = stripe.Price.list(
        lookup_keys=[payment_data['lookup_key']],
        expand=['data.product']
    )
    print(prices)

    try:

        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price': prices.data[0].id,
                    'quantity': 1,
                },
            ],
            mode='subscription',
            success_url=YOUR_DOMAIN + '/success.html',
            cancel_url=YOUR_DOMAIN + '/cancel.html'
            ,
        )
        return {"success": True, "url": checkout_session.url}
    except Exception as e:
        print(e)
        return "Server error", 500


@payment_controller.route('/create-portal-session', methods=['POST'])
def customer_portal():
    # For demonstration purposes, we're using the Checkout session to retrieve the customer ID.
    # Typically, this is stored alongside the authenticated user in your database.
    checkout_session_id = request.form.get('session_id')
    checkout_session = stripe.checkout.Session.retrieve(checkout_session_id)

    # This is the URL to which the customer will be redirected after they are
    # done managing their billing with the portal.
    return_url = YOUR_DOMAIN

    portalSession = stripe.billing_portal.Session.create(
        customer=checkout_session.customer,
        return_url=return_url,
    )
    return redirect(portalSession.url, code=303)


@payment_controller.route('/webhook', methods=['POST'])
def webhook_received():
    # Replace this endpoint secret with your endpoint's unique secret
    # If you are testing with the CLI, find the secret by running 'stripe listen'
    # If you are using an endpoint defined with the API or dashboard, look in your webhook settings
    # at https://dashboard.stripe.com/webhooks
    webhook_secret = os.getenv("WEBHOOK_SECRET")
    request_data = json.loads(request.data)

    if webhook_secret:
        # Retrieve the event by verifying the signature using the raw body and secret if webhook signing is configured.
        signature = request.headers.get('stripe-signature')
        try:
            event = stripe.Webhook.construct_event(
                payload=request.data, sig_header=signature, secret=webhook_secret)
            data = event['data']
        except Exception as e:
            return e
        # Get the type of webhook event sent - used to check the status of PaymentIntents.
        event_type = event['type']
    else:
        data = request_data['data']
        event_type = request_data['type']
    data_object = data['object']

    print('event ' + event_type)

    if event_type == 'checkout.session.completed':
        print('🔔 Payment succeeded!')
    elif event_type == 'customer.subscription.trial_will_end':
        print('Subscription trial will end')
    elif event_type == 'customer.subscription.created':
        print('Subscription created %s', event.id)
    elif event_type == 'customer.subscription.updated':
        print('Subscription created %s', event.id)
    elif event_type == 'customer.subscription.deleted':
        # handle subscription canceled automatically based
        # upon your subscription settings. Or if the user cancels it.
        print('Subscription canceled: %s', event.id)

    return jsonify({'status': 'success'})