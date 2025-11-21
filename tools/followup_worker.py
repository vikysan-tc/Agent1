"""
Simple follow-up worker for booking acknowledgements.

This script polls the ack_store.json file and when an entry's
`next_followup_at` <= now it will "send" the followup message.

Sending behavior:
- If environment variable FOLLOWUP_WEBHOOK is set, it will POST JSON {bookingId, customerEmail, message}
  to that webhook.
- Otherwise it will print the followup to stdout.

Run this as a background process alongside your agent to deliver delayed messages.
"""
import time
import json
import os
import requests

ACK_STORE = os.path.join(os.path.dirname(__file__), 'ack_store.json')
WEBHOOK = os.environ.get('FOLLOWUP_WEBHOOK')
POLL_INTERVAL = int(os.environ.get('FOLLOWUP_POLL_INTERVAL', '2'))


def _load():
    try:
        if os.path.exists(ACK_STORE):
            with open(ACK_STORE, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception:
        return {}
    return {}


def _save(d):
    try:
        with open(ACK_STORE, 'w', encoding='utf-8') as f:
            json.dump(d, f)
    except Exception:
        pass


print('Follow-up worker starting. Webhook=' + (WEBHOOK or 'stdout'))
while True:
    store = _load()
    now = int(time.time())
    changed = False
    for key, rec in list(store.items()):
        try:
            next_at = rec.get('next_followup_at')
            if not next_at:
                continue
            if next_at <= now:
                state = rec.get('state')
                if state == 'awaiting_upi':
                    # send UPI request message
                    msg = 'The refund is on hold as the UPI ID for the given customer is inactive, kindly provide correct UPI ID'
                    payload = {'bookingId': rec.get('bookingId'), 'customerEmail': rec.get('customerEmail'), 'message': msg}
                    if WEBHOOK:
                        try:
                            requests.post(WEBHOOK, json=payload, timeout=5)
                        except Exception as e:
                            print('Webhook post failed:', e)
                    else:
                        print('[FOLLOWUP] to', rec.get('customerEmail'), ':', msg)
                    # update state to waiting for UPI (keep same state) but clear next_followup to avoid repeat
                    rec['next_followup_at'] = None
                    rec['upi_prompt_sent_at'] = now
                    changed = True
                elif state == 'upi_provided':
                    # send refund reinitiated message
                    ticket_ref = rec.get('ticketReference')
                    msg = 'The refund is reinitiated'
                    if ticket_ref:
                        msg += f'; track the refund with ticket reference {ticket_ref}'
                    payload = {'bookingId': rec.get('bookingId'), 'customerEmail': rec.get('customerEmail'), 'message': msg}
                    if WEBHOOK:
                        try:
                            requests.post(WEBHOOK, json=payload, timeout=5)
                        except Exception as e:
                            print('Webhook post failed:', e)
                    else:
                        print('[FOLLOWUP] to', rec.get('customerEmail'), ':', msg)
                    # mark complete
                    rec['state'] = 'completed'
                    rec['next_followup_at'] = None
                    rec['completed_at'] = now
                    changed = True
        except Exception:
            continue

    if changed:
        _save(store)
    time.sleep(POLL_INTERVAL)
