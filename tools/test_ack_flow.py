import time
import json
import os
from tools import greetings

print('Calling acknowledge_booking...')
res = greetings.acknowledge_booking('booking-test', 'bob@example.com', 'TKT-001')
print('acknowledge_booking returned:', res)

store_path = os.path.join(os.path.dirname(greetings.__file__), 'ack_store.json')
store = json.load(open(store_path))
print('Store after ack creation:', store)

# accelerate next_followup_at to 1 second from now for testing
for k in list(store.keys()):
    if store[k].get('bookingId') == 'booking-test':
        store[k]['next_followup_at'] = int(time.time()) + 1
json.dump(store, open(store_path, 'w'), indent=2)

print('Waiting 1.5s to simulate first followup...')
time.sleep(1.5)

# simulate follow-up worker behavior for first followup
store = json.load(open(store_path))
now = int(time.time())
for k, rec in list(store.items()):
    next_at = rec.get('next_followup_at')
    if next_at and next_at <= now and rec.get('state') == 'awaiting_upi':
        msg = 'The refund is on hold as the UPI ID for the given customer is inactive, kindly provide correct UPI ID'
        print('[SIM FOLLOWUP] to', rec.get('customerEmail'), ':', msg)
        rec['next_followup_at'] = None
        rec['upi_prompt_sent_at'] = now

json.dump(store, open(store_path, 'w'), indent=2)
print('Store after first simulated followup:', json.load(open(store_path)))

# Now simulate the customer supplying UPI
print('\nCalling submit_upi...')
res2 = greetings.submit_upi('booking-test', 'bob@example.com', 'UPI123')
print('submit_upi returned:', res2)

# speed up the final followup
store = json.load(open(store_path))
for k in list(store.keys()):
    if store[k].get('bookingId') == 'booking-test':
        store[k]['next_followup_at'] = int(time.time()) + 1
json.dump(store, open(store_path, 'w'), indent=2)

print('Waiting 1.5s to simulate final followup...')
time.sleep(1.5)

store = json.load(open(store_path))
now = int(time.time())
for k, rec in list(store.items()):
    next_at = rec.get('next_followup_at')
    if next_at and next_at <= now and rec.get('state') == 'upi_provided':
        ticket_ref = rec.get('ticketReference')
        msg = 'The refund is reinitiated'
        if ticket_ref:
            msg += f'; track the refund with ticket reference {ticket_ref}'
        print('[SIM FOLLOWUP] to', rec.get('customerEmail'), ':', msg)
        rec['state'] = 'completed'
        rec['next_followup_at'] = None
        rec['completed_at'] = now

json.dump(store, open(store_path, 'w'), indent=2)
print('Final store:', json.load(open(store_path)))
