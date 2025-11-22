# Customer Complaint Knowledge Base

This knowledge base contains examples of various customer complaints to help the Email Processor Agent understand and categorize different types of issues.

## Table of Contents

1. [Flight-Related Complaints](#flight-related-complaints)
2. [Hotel Booking Complaints](#hotel-booking-complaints)
3. [Cancellation & Refund Requests](#cancellation--refund-requests)
4. [Payment & Billing Issues](#payment--billing-issues)
5. [Banking & Financial Services](#banking--financial-services)
6. [E-Commerce & Online Shopping](#e-commerce--online-shopping)
7. [Insurance Claims & Issues](#insurance-claims--issues)
8. [Healthcare & Medical Services](#healthcare--medical-services)
9. [Restaurant & Food Delivery](#restaurant--food-delivery)
10. [Subscription Services](#subscription-services)
11. [Car Rental Services](#car-rental-services)
12. [Event Tickets & Entertainment](#event-tickets--entertainment)
13. [Telecommunications](#telecommunications)
14. [Utilities & Services](#utilities--services)
15. [Education Services](#education-services)
16. [Service Quality Complaints](#service-quality-complaints)
17. [Technical Issues](#technical-issues)
18. [Booking Modification Requests](#booking-modification-requests)
19. [Priority Classification Guide](#priority-classification-guide)

---

## Flight-Related Complaints

### Flight Cancellation

**Example 1:**
```
Subject: URGENT: Flight Cancellation - Need Immediate Refund

From: Sarah Johnson <sarah.johnson@email.com>

Dear Support Team,

I am Sarah Johnson and I need urgent assistance. My flight from New York to London 
(Booking Reference: ABC123456) scheduled for March 15, 2024 has been cancelled by 
your airline. I have not received any refund or alternative flight options.

This is extremely inconvenient as I had important business meetings scheduled. 
I need a full refund immediately or a rebooking on the next available flight.

My contact details:
Email: sarah.johnson@email.com
Phone: +1-555-123-4567

Please respond urgently.

Best regards,
Sarah Johnson
```

**Expected Processing:**
- Priority: HIGH
- Issue Type: Flight Cancellation, Refund Request
- Key Information: Booking Reference, Date, Route

---

**Example 2:**
```
Subject: Flight Delay Compensation Request

From: Michael Chen <mchen@example.com>

Hello,

I am writing to complain about a significant delay on my flight yesterday. 
Flight number SHX789 from Mumbai to Delhi was delayed by 6 hours, causing me 
to miss an important connection.

I would like to request compensation for the inconvenience and the additional 
expenses I incurred due to this delay.

My booking reference is XYZ789012.
Phone: +91-98765-43210

Thank you,
Michael Chen
```

**Expected Processing:**
- Priority: HIGH
- Issue Type: Flight Delay, Compensation Request
- Key Information: Flight Number, Delay Duration, Booking Reference

---

### Flight Change/Rescheduling

**Example 3:**
```
Subject: Need to Change Flight Date

From: Emily Rodriguez <emily.r@email.com>

Hi,

I need to change my flight date. My current booking is for March 20, 2024, 
but I need to travel on March 25, 2024 instead.

Booking Reference: DEF456789
Flight: Los Angeles to Tokyo

Can you please help me reschedule? I'm willing to pay any difference in fare.

Phone: +1-555-987-6543

Thanks,
Emily Rodriguez
```

**Expected Processing:**
- Priority: MEDIUM
- Issue Type: Flight Rescheduling Request
- Key Information: Current Date, New Date, Booking Reference

---

### Lost/Damaged Baggage

**Example 4:**
```
Subject: Lost Luggage - Flight SHX456

From: David Thompson <dthompson@email.com>

Dear Customer Service,

I am David Thompson. I traveled on flight SHX456 from London to Paris on 
March 10, 2024, and my checked baggage has been lost. It's been 3 days 
and I still haven't received any update.

The bag contains important business documents and personal items worth 
approximately $2,000. I need immediate assistance in locating my luggage 
or compensation for the lost items.

Booking Reference: GHI789123
Phone: +44-20-1234-5678

This is very urgent. Please help.

Regards,
David Thompson
```

**Expected Processing:**
- Priority: HIGH
- Issue Type: Lost Baggage, Compensation Request
- Key Information: Flight Number, Date, Booking Reference, Item Value

---

## Hotel Booking Complaints

### Room Issues

**Example 5:**
```
Subject: Complaint - Dirty Room at Sherlox Hotel

From: Jennifer Williams <jwilliams@email.com>

To Whom It May Concern,

I am extremely disappointed with my stay at your hotel. I checked in on 
March 12, 2024, and my room (Room 305) was not properly cleaned. There 
were stains on the carpet, the bathroom had hair in it, and the bed 
sheets appeared to be used.

I immediately complained to the front desk, but they were unable to 
provide me with another room. This is unacceptable for a hotel of your 
caliber. I expect a full refund for my stay.

Booking ID: HOTEL-789456
Check-in: March 12, 2024
Check-out: March 15, 2024
Phone: +1-555-456-7890

I look forward to your prompt response.

Sincerely,
Jennifer Williams
```

**Expected Processing:**
- Priority: HIGH
- Issue Type: Room Quality Complaint, Refund Request
- Key Information: Booking ID, Room Number, Dates, Specific Issues

---

### Booking Not Found

**Example 6:**
```
Subject: Hotel Booking Confirmation Issue

From: Robert Kim <rkim@email.com>

Hello,

I made a hotel booking through your website on March 1, 2024, for dates 
March 20-23, 2024. I received a confirmation email with booking reference 
BOOK-123456, but when I called the hotel directly, they have no record 
of my reservation.

I have already paid $450 for this booking. Please investigate and 
confirm my reservation immediately, or provide a full refund.

Email: rkim@email.com
Phone: +82-10-1234-5678

This is urgent as my travel date is approaching.

Best regards,
Robert Kim
```

**Expected Processing:**
- Priority: HIGH
- Issue Type: Booking Confirmation Issue, Payment Concern
- Key Information: Booking Reference, Dates, Amount Paid

---

### Overbooking

**Example 7:**
```
Subject: URGENT - Hotel Overbooking Issue

From: Maria Garcia <mgarcia@email.com>

Dear Management,

I am writing to file a formal complaint. I had a confirmed reservation 
at your hotel for March 18-20, 2024 (Booking: HOTEL-456789), but when 
I arrived, I was told the hotel was overbooked and my room was not 
available.

I was forced to find alternative accommodation at the last minute, which 
cost me an additional $200. I demand a full refund for my original booking 
plus compensation for the inconvenience and additional expenses.

This is completely unacceptable. I will be taking legal action if this 
is not resolved immediately.

Phone: +34-91-123-4567

Sincerely,
Maria Garcia
```

**Expected Processing:**
- Priority: HIGH
- Issue Type: Overbooking, Compensation Request, Legal Threat
- Key Information: Booking Reference, Dates, Additional Costs

---

## Cancellation & Refund Requests

### Refund for Cancelled Service

**Example 8:**
```
Subject: Refund Request - Cancelled Booking

From: James Wilson <jwilson@email.com>

Hi,

I need to request a refund for a booking I cancelled. I had booked a 
package tour (Booking ID: PKG-987654) for April 1-7, 2024, but had 
to cancel due to a family emergency.

According to your cancellation policy, I should receive a 70% refund 
as I cancelled more than 14 days in advance. However, I have not 
received any refund after 2 weeks.

Original payment: $1,200
Expected refund: $840

Please process this refund immediately.

Phone: +1-555-321-9876

Thank you,
James Wilson
```

**Expected Processing:**
- Priority: HIGH
- Issue Type: Refund Request, Policy Dispute
- Key Information: Booking ID, Dates, Amount, Cancellation Policy

---

### Partial Refund Request

**Example 9:**
```
Subject: Request for Partial Refund

From: Lisa Anderson <landerson@email.com>

Dear Support,

I am requesting a partial refund for my recent booking. I booked a 
cruise package (CRUISE-123789) for March 25-30, 2024, but several 
excursions were cancelled due to weather conditions.

I understand weather is beyond your control, but I paid $500 specifically 
for these excursions. I believe I am entitled to a refund for the 
cancelled portions.

Please review my case and process the appropriate refund.

Booking Reference: CRUISE-123789
Phone: +1-555-654-3210

Best regards,
Lisa Anderson
```

**Expected Processing:**
- Priority: MEDIUM
- Issue Type: Partial Refund Request
- Key Information: Booking Reference, Specific Services Cancelled, Amount

---

## Payment & Billing Issues

### Double Charging

**Example 10:**
```
Subject: URGENT - Double Charge on My Credit Card

From: Thomas Brown <tbrown@email.com>

Hello,

I am writing to report that I have been charged twice for the same booking. 
I made a hotel reservation (Booking: HOTEL-321654) on March 5, 2024, 
and I can see two identical charges of $300 each on my credit card 
statement.

This is clearly an error. Please refund one of the charges immediately 
and confirm when the refund has been processed.

Credit Card: ****1234
Booking Reference: HOTEL-321654
Phone: +1-555-789-0123

I expect this to be resolved within 24 hours.

Regards,
Thomas Brown
```

**Expected Processing:**
- Priority: HIGH
- Issue Type: Billing Error, Double Charge, Refund Request
- Key Information: Booking Reference, Amount, Payment Method

---

### Incorrect Billing Amount

**Example 11:**
```
Subject: Incorrect Charge Amount

From: Patricia Lee <plee@email.com>

Dear Billing Department,

I recently made a booking through your website. The advertised price 
was $250, but I was charged $350. This is a significant discrepancy.

Booking Reference: BOOK-555888
Date of Booking: March 8, 2024
Advertised Price: $250
Amount Charged: $350
Difference: $100

Please investigate and refund the overcharge of $100.

Email: plee@email.com
Phone: +1-555-234-5678

Thank you for your attention to this matter.

Sincerely,
Patricia Lee
```

**Expected Processing:**
- Priority: HIGH
- Issue Type: Billing Error, Overcharge
- Key Information: Booking Reference, Expected vs Actual Amount

---

## Service Quality Complaints

### Poor Customer Service

**Example 12:**
```
Subject: Complaint About Poor Customer Service

From: Christopher Martinez <cmartinez@email.com>

To the Management,

I am writing to express my extreme dissatisfaction with the customer 
service I received. I called your support line multiple times regarding 
my booking issue, but each time I was put on hold for over 30 minutes 
and then disconnected.

When I finally spoke to someone, they were rude and unhelpful. This 
is completely unacceptable. I have been a loyal customer for 5 years, 
but this experience has made me reconsider my relationship with your 
company.

Booking Reference: BOOK-777999
Phone: +1-555-345-6789

I expect a formal apology and resolution to my original issue.

Best regards,
Christopher Martinez
```

**Expected Processing:**
- Priority: MEDIUM
- Issue Type: Service Quality Complaint, Customer Retention Issue
- Key Information: Booking Reference, Specific Service Issues

---

### Website/App Issues

**Example 13:**
```
Subject: Website Not Working - Cannot Complete Booking

From: Amanda Taylor <ataylor@email.com>

Hi,

I've been trying to make a booking on your website for the past 2 days, 
but I keep getting error messages. The payment page keeps crashing, and 
I've lost my booking information multiple times.

This is very frustrating. I need to make this booking urgently. Can 
someone please help me complete my reservation?

I'm trying to book:
- Hotel in Paris
- Dates: April 10-15, 2024
- 2 guests

Phone: +1-555-456-7890

Please contact me as soon as possible.

Thanks,
Amanda Taylor
```

**Expected Processing:**
- Priority: MEDIUM
- Issue Type: Technical Issue, Booking Assistance Needed
- Key Information: Technical Problem Description, Booking Details

---

## Technical Issues

### Account Access Problems

**Example 14:**
```
Subject: Cannot Access My Account

From: Daniel White <dwhite@email.com>

Hello Support,

I am unable to access my account. When I try to log in, I get an error 
message saying my password is incorrect, but I'm certain I'm using the 
correct password. I've tried resetting it multiple times, but I never 
receive the password reset email.

I need to access my booking information urgently. Can you please help 
me regain access to my account?

Email: dwhite@email.com
Phone: +1-555-567-8901

This is urgent - I have a trip coming up soon.

Regards,
Daniel White
```

**Expected Processing:**
- Priority: MEDIUM
- Issue Type: Account Access Issue, Technical Problem
- Key Information: Account Email, Specific Error

---

### Mobile App Problems

**Example 15:**
```
Subject: Mobile App Crashing

From: Jessica Harris <jharris@email.com>

Dear Technical Support,

Your mobile app keeps crashing on my phone. Every time I try to view 
my bookings or make a new reservation, the app closes unexpectedly. 
I've tried uninstalling and reinstalling, but the problem persists.

Device: iPhone 13
App Version: 2.5.1
OS: iOS 16.2

This is very inconvenient. Please fix this issue or provide an alternative 
way for me to access my bookings.

Phone: +1-555-678-9012

Thank you,
Jessica Harris
```

**Expected Processing:**
- Priority: MEDIUM
- Issue Type: Technical Issue, App Bug
- Key Information: Device, App Version, OS Version

---

## Booking Modification Requests

### Date Change Request

**Example 16:**
```
Subject: Request to Change Booking Dates

From: Ryan Clark <rclark@email.com>

Hi,

I need to change the dates of my booking. I originally booked for 
March 25-28, 2024, but I need to move it to April 5-8, 2024 instead.

Booking Reference: BOOK-111222
Original Dates: March 25-28, 2024
New Dates: April 5-8, 2024

I understand there may be a price difference, which I'm willing to pay. 
Please confirm if this change is possible.

Phone: +1-555-789-0123

Thank you,
Ryan Clark
```

**Expected Processing:**
- Priority: MEDIUM
- Issue Type: Booking Modification Request
- Key Information: Booking Reference, Original Dates, New Dates

---

### Guest Information Update

**Example 17:**
```
Subject: Update Guest Information

From: Nicole Young <nyoung@email.com>

Hello,

I need to update the guest information on my booking. I made a mistake 
when entering the passenger name. 

Booking Reference: BOOK-333444
Current Name: Nicole Young
Correct Name: Nicole Young-Smith

Please update this information as soon as possible.

Phone: +1-555-890-1234

Thanks,
Nicole Young
```

**Expected Processing:**
- Priority: LOW
- Issue Type: Information Update Request
- Key Information: Booking Reference, Current Info, Correct Info

---

## Banking & Financial Services

### Unauthorized Transactions

**Example 18:**
```
Subject: URGENT - Unauthorized Charge on My Account

From: Mark Davis <mdavis@email.com>

Dear Fraud Department,

I am Mark Davis and I need immediate assistance. I noticed an unauthorized 
charge of $1,250 on my credit card (ending in 5678) on March 14, 2024. 
The transaction was made at a store I've never visited in a city I've 
never been to.

This is clearly fraudulent activity. I need you to:
1. Reverse this charge immediately
2. Cancel my current card and issue a new one
3. Investigate this fraudulent transaction

Account: ****5678
Transaction Date: March 14, 2024
Amount: $1,250.00
Merchant: Unknown Store Location

Phone: +1-555-111-2222

This is extremely urgent. Please respond within 24 hours.

Sincerely,
Mark Davis
```

**Expected Processing:**
- Priority: HIGH
- Issue Type: Fraud, Unauthorized Transaction, Account Security
- Key Information: Account Number, Transaction Date, Amount, Urgency

---

**Example 19:**
```
Subject: Suspicious Activity on My Bank Account

From: Laura Martinez <lmartinez@email.com>

Hello,

I am Laura Martinez. I received an alert about suspicious activity on 
my checking account. There were three small transactions I don't recognize:
- $9.99 on March 12
- $15.50 on March 13
- $12.00 on March 13

These appear to be test transactions before a larger fraud attempt. 
Please freeze my account immediately and contact me.

Account Number: ****1234
Phone: +1-555-222-3333

Thank you,
Laura Martinez
```

**Expected Processing:**
- Priority: HIGH
- Issue Type: Fraud, Suspicious Activity, Account Security
- Key Information: Account Number, Transaction Details

---

### Account Access Issues

**Example 20:**
```
Subject: Cannot Access Online Banking

From: Robert Taylor <rtaylor@email.com>

Dear Support,

I am unable to access my online banking account. When I try to log in, 
I get an error message saying my account has been locked due to multiple 
failed login attempts. However, I haven't tried to log in recently.

I need access to my account urgently to pay bills and check my balance. 
Can you please unlock my account and help me regain access?

Account: ****9876
Email: rtaylor@email.com
Phone: +1-555-333-4444

Please help as soon as possible.

Best regards,
Robert Taylor
```

**Expected Processing:**
- Priority: MEDIUM
- Issue Type: Account Access Issue, Technical Problem
- Key Information: Account Number, Access Problem

---

### Loan & Credit Issues

**Example 21:**
```
Subject: Complaint About Incorrect Interest Rate

From: Jennifer White <jwhite@email.com>

To Whom It May Concern,

I am writing to complain about an incorrect interest rate being applied 
to my personal loan. When I took out the loan in January 2024, I was 
quoted an interest rate of 5.5% APR, but I'm being charged 7.2% APR.

This is a significant difference and is costing me hundreds of dollars 
in additional interest. I have documentation showing the original rate 
quoted to me.

Loan Account: LOAN-456789
Original Rate: 5.5% APR
Current Rate: 7.2% APR
Loan Amount: $25,000

Please correct this immediately and refund the overcharged interest.

Phone: +1-555-444-5555

I expect a response within 48 hours.

Sincerely,
Jennifer White
```

**Expected Processing:**
- Priority: HIGH
- Issue Type: Billing Error, Loan Dispute, Financial Impact
- Key Information: Loan Account, Interest Rates, Amount

---

**Example 22:**
```
Subject: Credit Card Payment Not Reflected

From: Michael Brown <mbrown@email.com>

Hello,

I made a payment of $500 to my credit card on March 10, 2024, but it 
hasn't been reflected in my account balance yet. It's been 5 days and 
the payment still shows as pending.

I'm concerned because my payment due date is approaching and I don't 
want to incur late fees or damage my credit score.

Card: ****3456
Payment Amount: $500
Payment Date: March 10, 2024
Transaction ID: PAY-789123

Please investigate and update my account balance immediately.

Phone: +1-555-555-6666

Thank you,
Michael Brown
```

**Expected Processing:**
- Priority: MEDIUM
- Issue Type: Payment Processing Issue, Account Update
- Key Information: Card Number, Payment Amount, Date, Transaction ID

---

### ATM & Card Issues

**Example 23:**
```
Subject: ATM Swallowed My Card - Need Immediate Help

From: Susan Anderson <sanderson@email.com>

URGENT - My debit card was swallowed by an ATM machine today. I was 
trying to withdraw cash from the ATM at 123 Main Street, but the machine 
took my card and didn't return it.

I need my card urgently as I'm traveling tomorrow and need access to 
funds. Please:
1. Retrieve my card or issue a replacement immediately
2. Ensure my account is secure
3. Provide a temporary solution for accessing my funds

Card Number: ****7890
ATM Location: 123 Main Street, City, State
Time: March 15, 2024 at 2:30 PM
Phone: +1-555-666-7777

This is very urgent. Please respond ASAP.

Susan Anderson
```

**Expected Processing:**
- Priority: HIGH
- Issue Type: Card Issue, Urgent Access Needed
- Key Information: Card Number, Location, Time, Urgency

---

**Example 24:**
```
Subject: Debit Card Not Working

From: David Wilson <dwilson@email.com>

Hi,

My debit card stopped working yesterday. I tried to use it at multiple 
locations, but all transactions are being declined. I know I have 
sufficient funds in my account.

I've been a customer for 10 years and this has never happened before. 
Please investigate and fix this issue immediately.

Account: ****2345
Card: ****2345
Phone: +1-555-777-8888

I need this resolved today as I rely on this card for daily expenses.

Thanks,
David Wilson
```

**Expected Processing:**
- Priority: MEDIUM
- Issue Type: Card Malfunction, Transaction Issue
- Key Information: Account/Card Number, Customer History

---

### Wire Transfer Issues

**Example 25:**
```
Subject: Wire Transfer Not Received - URGENT

From: Patricia Lee <plee@email.com>

Dear Wire Transfer Department,

I sent a wire transfer of $5,000 on March 12, 2024, but the recipient 
has not received it yet. This is extremely urgent as it was for a 
time-sensitive business transaction.

Wire Transfer Reference: WT-987654
Amount: $5,000
Sent Date: March 12, 2024
Recipient: ABC Company
Recipient Account: ****5678

Please trace this transfer immediately and provide an update. If there's 
a problem, I need to know right away so I can take alternative action.

Phone: +1-555-888-9999

This is critical. Please respond within 2 hours.

Patricia Lee
```

**Expected Processing:**
- Priority: HIGH
- Issue Type: Wire Transfer Issue, Urgent Financial Transaction
- Key Information: Transfer Reference, Amount, Dates, Urgency

---

### Account Statement Errors

**Example 26:**
```
Subject: Incorrect Charges on My Statement

From: James Garcia <jgarcia@email.com>

Hello,

I received my monthly statement and noticed several incorrect charges. 
There are three transactions I don't recognize:
1. $89.99 - "Online Purchase" on March 5
2. $45.50 - "Service Fee" on March 8
3. $120.00 - "Subscription" on March 10

I did not authorize any of these charges. Please investigate and remove 
these fraudulent charges from my account immediately.

Account: ****6789
Statement Period: March 1-15, 2024
Phone: +1-555-999-0000

I expect a full refund for these unauthorized charges.

James Garcia
```

**Expected Processing:**
- Priority: HIGH
- Issue Type: Unauthorized Charges, Statement Error
- Key Information: Account Number, Transaction Details, Dates

---

## E-Commerce & Online Shopping

### Order Not Received

**Example 27:**
```
Subject: Order Not Delivered - Order #ORD-123456

From: Emily Chen <echen@email.com>

Dear Customer Service,

I placed an order on March 1, 2024 (Order #ORD-123456) for a laptop 
worth $899. The order confirmation said it would be delivered by March 
8, 2024, but I still haven't received it. It's been over two weeks.

I've checked the tracking information, but it shows the package is still 
"in transit" with no updates for the past 10 days. This is unacceptable.

Order Number: ORD-123456
Order Date: March 1, 2024
Expected Delivery: March 8, 2024
Amount: $899.00
Phone: +1-555-100-2000

I need either my order delivered immediately or a full refund. Please 
respond within 24 hours.

Emily Chen
```

**Expected Processing:**
- Priority: HIGH
- Issue Type: Delivery Issue, Order Not Received, Refund Request
- Key Information: Order Number, Dates, Amount

---

**Example 28:**
```
Subject: Missing Items from My Order

From: Kevin Johnson <kjohnson@email.com>

Hi,

I received my order today (Order #ORD-789012), but two items are missing. 
I ordered 5 items but only received 3. The missing items are:
- Wireless Mouse ($29.99)
- USB-C Cable ($12.99)

The packing slip shows all 5 items, but they're not in the box. Please 
send the missing items immediately or refund me for them.

Order: ORD-789012
Received Date: March 15, 2024
Missing Items Value: $42.98
Phone: +1-555-200-3000

Thanks,
Kevin Johnson
```

**Expected Processing:**
- Priority: MEDIUM
- Issue Type: Incomplete Order, Missing Items
- Key Information: Order Number, Missing Items, Values

---

### Wrong Item Received

**Example 29:**
```
Subject: Received Wrong Product - Need Exchange

From: Lisa Wang <lwang@email.com>

Hello,

I ordered a blue jacket (Order #ORD-345678) but received a red jacket 
instead. This is not what I ordered. I need to exchange this for the 
correct item or get a full refund.

Order Number: ORD-345678
Order Date: March 5, 2024
Ordered: Blue Jacket, Size M
Received: Red Jacket, Size M
Price: $79.99

Please send me a return label and process the exchange immediately.

Phone: +1-555-300-4000

Lisa Wang
```

**Expected Processing:**
- Priority: MEDIUM
- Issue Type: Wrong Item, Exchange Request
- Key Information: Order Number, Item Details

---

### Damaged Product

**Example 30:**
```
Subject: Product Arrived Damaged - Need Refund

From: Brian Smith <bsmith@email.com>

Dear Support,

I received my order today (Order #ORD-456789), but the product arrived 
completely damaged. The box was crushed and the item inside is broken 
and unusable.

This is clearly a shipping/packaging issue. I need either:
1. A replacement sent immediately with better packaging, OR
2. A full refund

Order: ORD-456789
Item: Electronics Product
Price: $199.99
Received: March 14, 2024
Phone: +1-555-400-5000

Please resolve this quickly.

Brian Smith
```

**Expected Processing:**
- Priority: MEDIUM
- Issue Type: Damaged Product, Refund/Replacement Request
- Key Information: Order Number, Product, Condition

---

### Return & Refund Issues

**Example 31:**
```
Subject: Refund Not Processed After 3 Weeks

From: Amanda Rodriguez <arodriguez@email.com>

Hello,

I returned an item on February 25, 2024 (Order #ORD-567890) and was 
told I would receive a refund within 7-10 business days. It's been 3 
weeks and I still haven't received my refund.

I have the return tracking number showing the item was delivered to your 
warehouse on March 1, 2024. Please process my refund immediately.

Order: ORD-567890
Return Date: February 25, 2024
Refund Amount: $149.99
Tracking: RET-123456
Phone: +1-555-500-6000

This is taking too long. I expect my refund within 48 hours.

Amanda Rodriguez
```

**Expected Processing:**
- Priority: HIGH
- Issue Type: Refund Delay, Return Processing Issue
- Key Information: Order Number, Return Date, Amount, Tracking

---

### Price Discrepancy

**Example 32:**
```
Subject: Charged More Than Advertised Price

From: Christopher Kim <ckim@email.com>

Dear Billing Department,

I purchased an item from your website that was advertised at $49.99, 
but I was charged $69.99. This is a $20 difference that I did not agree 
to pay.

I have a screenshot of the advertised price from when I made the purchase. 
Please refund the $20 difference immediately.

Order: ORD-678901
Advertised Price: $49.99
Charged: $69.99
Difference: $20.00
Phone: +1-555-600-7000

I expect this to be resolved today.

Christopher Kim
```

**Expected Processing:**
- Priority: MEDIUM
- Issue Type: Pricing Error, Overcharge
- Key Information: Order Number, Prices, Difference

---

## Insurance Claims & Issues

### Claim Denial

**Example 33:**
```
Subject: Appeal - My Insurance Claim Was Wrongly Denied

From: Michelle Thompson <mthompson@email.com>

Dear Claims Department,

I am writing to appeal the denial of my insurance claim. I filed a claim 
for water damage to my home on February 20, 2024 (Claim #CLM-123456), 
but it was denied stating it was "pre-existing damage."

This is incorrect. The damage occurred on February 18, 2024, due to 
a burst pipe, which is a covered event under my policy. I have photos, 
repair estimates, and a plumber's report proving this was a sudden event.

Claim Number: CLM-123456
Date of Loss: February 18, 2024
Claim Amount: $8,500
Policy Number: POL-789012

Please review my claim again and approve it. If this is not resolved, 
I will be contacting the insurance commissioner.

Phone: +1-555-700-8000

Michelle Thompson
```

**Expected Processing:**
- Priority: HIGH
- Issue Type: Claim Denial Appeal, Policy Dispute
- Key Information: Claim Number, Policy Number, Amount, Legal Threat

---

### Delayed Claim Processing

**Example 34:**
```
Subject: Insurance Claim Taking Too Long

From: Daniel Martinez <dmartinez@email.com>

Hello,

I filed an auto insurance claim on March 1, 2024 (Claim #CLM-234567) 
for damage to my car from an accident. It's been 2 weeks and I still 
haven't received any update on the status of my claim.

I need my car repaired urgently as I use it for work. The damage estimate 
is $3,200 and I've already paid the deductible. Please process my claim 
immediately.

Claim: CLM-234567
Date: March 1, 2024
Amount: $3,200
Policy: POL-890123
Phone: +1-555-800-9000

This delay is unacceptable. Please expedite.

Daniel Martinez
```

**Expected Processing:**
- Priority: MEDIUM
- Issue Type: Claim Processing Delay
- Key Information: Claim Number, Dates, Amount, Urgency

---

### Coverage Dispute

**Example 35:**
```
Subject: Dispute - Service Not Covered by Insurance

From: Stephanie White <swhite@email.com>

Dear Insurance Department,

I am disputing a coverage decision. I had a medical procedure done that 
my doctor said was medically necessary, but my insurance company is 
refusing to cover it, saying it's "not medically necessary."

I have documentation from my doctor explaining why this procedure was 
required. The procedure cost $5,000 and I cannot afford to pay this 
out of pocket.

Claim: CLM-345678
Procedure Date: March 5, 2024
Amount: $5,000
Policy: POL-901234

Please review this decision and approve coverage. I will file an appeal 
if necessary.

Phone: +1-555-900-1000

Stephanie White
```

**Expected Processing:**
- Priority: HIGH
- Issue Type: Coverage Dispute, Medical Claim
- Key Information: Claim Number, Amount, Medical Necessity

---

## Healthcare & Medical Services

### Appointment Issues

**Example 36:**
```
Subject: URGENT - Need to Reschedule Appointment

From: Richard Brown <rbrown@email.com>

Hello,

I have an urgent medical appointment scheduled for tomorrow, March 16, 
2024 at 2:00 PM, but I have a family emergency and cannot make it. 
I need to reschedule as soon as possible.

This is for a follow-up appointment that I cannot miss. Please help 
me find another available time this week.

Appointment: APP-123456
Original Date: March 16, 2024, 2:00 PM
Doctor: Dr. Smith
Phone: +1-555-100-1100

Please call me back today to reschedule.

Richard Brown
```

**Expected Processing:**
- Priority: MEDIUM
- Issue Type: Appointment Rescheduling, Urgent
- Key Information: Appointment ID, Date, Doctor, Urgency

---

**Example 37:**
```
Subject: Complaint - Doctor Appointment Cancelled Without Notice

From: Nancy Davis <ndavis@email.com>

Dear Patient Relations,

I am very upset. I had an appointment scheduled for March 10, 2024 at 
10:00 AM with Dr. Johnson. I took time off work and drove 30 minutes 
to the clinic, only to find out the appointment had been cancelled 
without any notification to me.

This is the second time this has happened. I wasted my time and lost 
a day's pay. I need either:
1. An immediate appointment this week, OR
2. Compensation for my lost time and wages

Appointment: APP-234567
Date: March 10, 2024
Doctor: Dr. Johnson
Phone: +1-555-110-1200

This is unacceptable. I expect a response within 24 hours.

Nancy Davis
```

**Expected Processing:**
- Priority: HIGH
- Issue Type: Service Failure, Compensation Request
- Key Information: Appointment Details, Impact, Repeat Issue

---

### Medical Billing Errors

**Example 38:**
```
Subject: Incorrect Medical Bill - Overcharged

From: Joseph Wilson <jwilson@email.com>

Hello,

I received a medical bill for $2,500, but I believe I'm being overcharged. 
I had a routine checkup on February 15, 2024, and the bill shows charges 
for procedures I never received.

Specifically, I'm being charged for:
- Lab tests I didn't have
- Specialist consultation I didn't receive
- Procedures not performed

I only had a basic physical exam. Please review my bill and correct it.

Account: MED-345678
Date of Service: February 15, 2024
Billed Amount: $2,500
Expected Amount: ~$200
Phone: +1-555-120-1300

Please investigate and correct this immediately.

Joseph Wilson
```

**Expected Processing:**
- Priority: HIGH
- Issue Type: Billing Error, Overcharge, Medical Services
- Key Information: Account Number, Service Date, Amount Discrepancy

---

### Prescription Issues

**Example 39:**
```
Subject: Prescription Not Filled Correctly

From: Karen Anderson <kanderson@email.com>

Dear Pharmacy,

I picked up my prescription yesterday (March 14, 2024), but when I got 
home, I realized the medication and dosage are incorrect. The prescription 
label shows the right information, but the actual pills inside are different.

This is a serious medication error that could have health consequences. 
I need the correct medication immediately.

Prescription: RX-456789
Date: March 14, 2024
Pharmacy: Main Street Pharmacy
Phone: +1-555-130-1400

Please contact me immediately to resolve this.

Karen Anderson
```

**Expected Processing:**
- Priority: HIGH
- Issue Type: Medication Error, Safety Concern
- Key Information: Prescription Number, Date, Safety Issue

---

## Restaurant & Food Delivery

### Food Quality Issues

**Example 40:**
```
Subject: Complaint - Food Poisoning from Your Restaurant

From: Steven Taylor <staylor@email.com>

URGENT - I am writing to report a serious food safety issue. I ordered 
food from your restaurant on March 12, 2024, and became severely ill 
with food poisoning symptoms within hours of eating.

I had to visit the emergency room and was diagnosed with foodborne 
illness. This is completely unacceptable and I'm considering legal action.

Order: REST-123456
Date: March 12, 2024
Items: Chicken meal, salad
Phone: +1-555-140-1500

I expect compensation for my medical bills and lost wages. Please 
respond immediately.

Steven Taylor
```

**Expected Processing:**
- Priority: HIGH
- Issue Type: Food Safety, Health Issue, Legal Threat
- Key Information: Order Number, Date, Health Impact

---

**Example 41:**
```
Subject: Wrong Order Delivered

From: Melissa Garcia <mgarcia@email.com>

Hi,

I placed an order for delivery today (Order #DEL-234567) but received 
completely wrong items. I ordered vegetarian pasta but received a meat 
pizza instead. I'm vegetarian and cannot eat this.

I've already paid $25 for this order. Please either:
1. Deliver the correct order immediately, OR
2. Provide a full refund

Order: DEL-234567
Ordered: Vegetarian Pasta
Received: Meat Pizza
Amount: $25.00
Phone: +1-555-150-1600

Please fix this quickly.

Melissa Garcia
```

**Expected Processing:**
- Priority: MEDIUM
- Issue Type: Wrong Order, Dietary Restriction Issue
- Key Information: Order Number, Items, Dietary Concern

---

### Delivery Problems

**Example 42:**
```
Subject: Food Delivery Never Arrived

From: Andrew Lee <alee@email.com>

Hello,

I placed an order for food delivery 2 hours ago (Order #DEL-345678) 
and it still hasn't arrived. The tracking shows it's been "out for 
delivery" for over an hour, but no one has come to my address.

I'm hungry and frustrated. I've already been charged $35 for this 
order. Please either deliver my food immediately or refund my money.

Order: DEL-345678
Order Time: 6:00 PM
Current Time: 8:00 PM
Amount: $35.00
Address: 456 Oak Street
Phone: +1-555-160-1700

This is unacceptable service.

Andrew Lee
```

**Expected Processing:**
- Priority: MEDIUM
- Issue Type: Delivery Delay, Order Not Received
- Key Information: Order Number, Times, Amount

---

## Subscription Services

### Unauthorized Charges

**Example 43:**
```
Subject: Unauthorized Subscription Charge

From: Rachel Kim <rkim@email.com>

Dear Billing Department,

I noticed a charge of $29.99 on my credit card for a subscription service 
I never signed up for. I did not authorize this subscription and want 
it cancelled immediately.

I also want a full refund for all charges made to my account. This appears 
to be fraudulent activity.

Subscription: SUB-123456
Charge Amount: $29.99
Charge Date: March 10, 2024
Card: ****7890
Phone: +1-555-170-1800

Please cancel and refund immediately.

Rachel Kim
```

**Expected Processing:**
- Priority: HIGH
- Issue Type: Unauthorized Subscription, Fraud
- Key Information: Subscription ID, Amount, Card

---

### Cancellation Issues

**Example 44:**
```
Subject: Cannot Cancel My Subscription

From: Jason Park <jpark@email.com>

Hello,

I've been trying to cancel my subscription for the past week, but your 
website keeps giving me errors when I try to cancel. I've also called 
your customer service line multiple times but have been on hold for 
over an hour each time.

This is very frustrating. I want to cancel my subscription immediately 
and I don't want to be charged again.

Subscription: SUB-234567
Account: jpark@email.com
Phone: +1-555-180-1900

Please cancel my subscription and confirm via email.

Jason Park
```

**Expected Processing:**
- Priority: MEDIUM
- Issue Type: Cancellation Difficulty, Technical Issue
- Key Information: Subscription ID, Account, Frustration Level

---

### Service Not Working

**Example 45:**
```
Subject: Streaming Service Not Working

From: Samantha Chen <schen@email.com>

Hi,

I'm paying $14.99/month for your streaming service, but it hasn't been 
working properly for the past week. Videos keep buffering, freezing, 
and the quality is terrible even though I have a fast internet connection.

I've tried everything - restarting the app, clearing cache, checking 
my internet - but nothing works. This is not what I'm paying for.

Account: SUB-345678
Monthly Fee: $14.99
Issue Duration: 1 week
Phone: +1-555-190-2000

Please fix this or refund my subscription fees.

Samantha Chen
```

**Expected Processing:**
- Priority: MEDIUM
- Issue Type: Service Quality, Technical Problem
- Key Information: Account, Fee, Duration, Refund Request

---

## Car Rental Services

### Vehicle Problems

**Example 46:**
```
Subject: URGENT - Rental Car Broke Down

From: Thomas Moore <tmoore@email.com>

URGENT - I rented a car from your company (Rental #RENT-123456) and it 
broke down on the highway today. The car just stopped working and I had 
to be towed. This is extremely dangerous and inconvenient.

I'm currently stranded and need immediate assistance. Please:
1. Send a replacement vehicle immediately
2. Arrange for the broken car to be towed
3. Refund me for the inconvenience

Rental: RENT-123456
Pickup Date: March 10, 2024
Current Location: Highway 101, Mile Marker 45
Phone: +1-555-200-2100

This is an emergency. Please respond immediately.

Thomas Moore
```

**Expected Processing:**
- Priority: HIGH
- Issue Type: Vehicle Breakdown, Safety Issue, Urgent
- Key Information: Rental Number, Location, Emergency Situation

---

**Example 47:**
```
Subject: Rental Car Had Mechanical Issues

From: Lisa Johnson <ljohnson@email.com>

Dear Customer Service,

I rented a car from your location on March 8, 2024 (Rental #RENT-234567), 
but the car had several mechanical issues:
- Brakes were making loud grinding noises
- Check engine light was on
- Air conditioning didn't work

I returned the car early because I didn't feel safe driving it. I want 
a full refund for the rental period I didn't use.

Rental: RENT-234567
Rental Period: March 8-15, 2024
Returned: March 10, 2024 (early)
Amount Paid: $350
Phone: +1-555-210-2200

Please process my refund immediately.

Lisa Johnson
```

**Expected Processing:**
- Priority: HIGH
- Issue Type: Vehicle Safety Issue, Early Return, Refund Request
- Key Information: Rental Number, Safety Concerns, Refund Amount

---

### Billing Disputes

**Example 48:**
```
Subject: Incorrect Charges on Rental Car Bill

From: Robert Martinez <rmartinez@email.com>

Hello,

I returned my rental car on March 12, 2024, but I'm being charged for 
damages I didn't cause. The car had a scratch on it when I picked it 
up, but I didn't report it because it was minor. Now you're charging 
me $500 for "damage repair."

I have photos of the car when I picked it up showing the scratch was 
already there. Please remove this charge from my bill.

Rental: RENT-345678
Return Date: March 12, 2024
Charge: $500 (damage repair)
Phone: +1-555-220-2300

I will dispute this with my credit card company if not resolved.

Robert Martinez
```

**Expected Processing:**
- Priority: HIGH
- Issue Type: Billing Dispute, Damage Charge, Evidence Provided
- Key Information: Rental Number, Charge Amount, Dispute

---

## Event Tickets & Entertainment

### Ticket Issues

**Example 49:**
```
Subject: Concert Tickets Not Received

From: Michelle Brown <mbrown@email.com>

Dear Ticket Office,

I purchased concert tickets on February 20, 2024 (Order #TIX-123456) 
for a concert on April 5, 2024. The confirmation email said tickets 
would be emailed within 48 hours, but I still haven't received them.

The concert is in 3 weeks and I'm worried I won't get my tickets in time. 
I paid $200 for these tickets and need them immediately.

Order: TIX-123456
Event: Concert on April 5, 2024
Amount: $200
Purchase Date: February 20, 2024
Phone: +1-555-230-2400

Please send my tickets today or provide a refund.

Michelle Brown
```

**Expected Processing:**
- Priority: MEDIUM
- Issue Type: Ticket Delivery Issue, Time-Sensitive
- Key Information: Order Number, Event Date, Amount

---

**Example 50:**
```
Subject: Event Cancelled - Need Refund

From: David Kim <dkim@email.com>

Hello,

I purchased tickets for an event scheduled for March 20, 2024, but the 
event has been cancelled. I haven't received any refund or information 
about when I'll get my money back.

I paid $150 for two tickets and need this refunded immediately.

Order: TIX-234567
Event: March 20, 2024
Amount: $150
Phone: +1-555-240-2500

Please process my refund within 5 business days.

David Kim
```

**Expected Processing:**
- Priority: HIGH
- Issue Type: Event Cancellation, Refund Request
- Key Information: Order Number, Event Date, Amount

---

## Priority Classification Guide

### HIGH Priority Indicators

- Keywords: urgent, emergency, critical, asap, immediately
- Refund requests (especially for cancelled services)
- Billing errors (double charges, overcharges)
- Lost/damaged items (baggage, belongings)
- Service failures (overbooking, no-show rooms)
- Legal threats or escalation language
- Time-sensitive issues (upcoming travel dates)
- Significant financial impact ($500+)

### MEDIUM Priority Indicators

- Booking modifications
- Service quality complaints
- Technical issues (website, app problems)
- Date change requests
- General inquiries with issues
- Moderate financial impact ($100-$500)

### LOW Priority Indicators

- Information updates
- General questions
- Feedback or suggestions
- Minor modifications
- Non-urgent inquiries
- Low financial impact (<$100)

---

## Common Patterns to Recognize

### Booking References
- Format: Usually alphanumeric (e.g., ABC123456, BOOK-789456, HOTEL-321654)
- Location: Often in subject line or first paragraph
- Importance: Critical for tracking and resolution

### Dates
- Travel dates: Check-in/check-out, departure/arrival
- Booking dates: When reservation was made
- Cancellation dates: When service was cancelled
- Format: Usually MM/DD/YYYY or DD/MM/YYYY

### Financial Information
- Amounts: Usually in currency format ($XXX, €XXX, £XXX)
- Payment methods: Credit card, debit card, PayPal
- Refund amounts: Expected vs actual

### Contact Information
- Phone numbers: Various international formats
- Email addresses: Usually in "From" header
- Names: May be in signature, "I am" statements, or From header

---

## Processing Tips

1. **Subject Line Analysis**: Often contains the most important information (urgency, issue type, booking reference)

2. **First Paragraph**: Usually contains the main complaint or request

3. **Booking References**: Look for alphanumeric codes, often near dates or amounts

4. **Urgency Indicators**: Words like "urgent", "asap", "immediately" in subject or body

5. **Financial Impact**: Higher amounts typically indicate higher priority

6. **Legal Language**: Phrases like "legal action", "lawyer", "sue" indicate HIGH priority

7. **Customer History**: References to "loyal customer", "years of service" may indicate retention risk

---

## Example Processing Results

### Example 1 Result:
```json
{
  "CustomerName": "Sarah Johnson",
  "CustomerEmail": "sarah.johnson@email.com",
  "CustomerPhoneNumber": "+1-555-123-4567",
  "IssueDescription": "[Subject: URGENT: Flight Cancellation - Need Immediate Refund] I am Sarah Johnson and I need urgent assistance. My flight from New York to London (Booking Reference: ABC123456) scheduled for March 15, 2024 has been cancelled by your airline. I have not received any refund or alternative flight options. This is extremely inconvenient as I had important business meetings scheduled. I need a full refund immediately or a rebooking on the next available flight.",
  "Priority": "HIGH",
  "Subject": "URGENT: Flight Cancellation - Need Immediate Refund",
  "EmailMetadata": {
    "From": "Sarah Johnson <sarah.johnson@email.com>",
    "To": "reachus.sherlox@gmail.com",
    "Subject": "URGENT: Flight Cancellation - Need Immediate Refund",
    "HasSubject": true,
    "SubjectLength": 50,
    "BodyLength": 450
  }
}
```

### Example 5 Result:
```json
{
  "CustomerName": "Jennifer Williams",
  "CustomerEmail": "jwilliams@email.com",
  "CustomerPhoneNumber": "+1-555-456-7890",
  "IssueDescription": "[Subject: Complaint - Dirty Room at Sherlox Hotel] I am extremely disappointed with my stay at your hotel. I checked in on March 12, 2024, and my room (Room 305) was not properly cleaned. There were stains on the carpet, the bathroom had hair in it, and the bed sheets appeared to be used. I immediately complained to the front desk, but they were unable to provide me with another room. This is unacceptable for a hotel of your caliber. I expect a full refund for my stay.",
  "Priority": "HIGH",
  "Subject": "Complaint - Dirty Room at Sherlox Hotel",
  "EmailMetadata": {
    "From": "Jennifer Williams <jwilliams@email.com>",
    "To": "reachus.sherlox@gmail.com",
    "Subject": "Complaint - Dirty Room at Sherlox Hotel",
    "HasSubject": true,
    "SubjectLength": 38,
    "BodyLength": 520
  }
}
```

---

## Notes for Agent Training

1. **Context Matters**: A "refund" request for a $50 booking is different from a $5,000 booking cancellation

2. **Tone Analysis**: Aggressive language, legal threats, or escalation mentions should increase priority

3. **Time Sensitivity**: References to "upcoming trip", "leaving tomorrow", or specific dates soon should be flagged

4. **Financial Impact**: Always extract and consider the monetary value when determining priority

5. **Customer Status**: References to "loyal customer", "frequent traveler", or "VIP" may indicate retention risk

6. **Multiple Issues**: Emails mentioning multiple problems (e.g., dirty room + poor service + billing error) should be HIGH priority

7. **Subject Line Priority**: If subject contains urgent keywords, the email is likely HIGH priority even if body is less urgent

---

This knowledge base should be used as a reference when processing customer emails to ensure accurate categorization, priority assignment, and information extraction.

