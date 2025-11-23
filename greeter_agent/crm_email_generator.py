"""
CRM Email Response Generator
Generates mock email responses based on CRM API responses for ticket creation, booking acknowledgement, etc.
"""

import os
import requests
from typing import Optional, Dict, Any
import json

# CRM Server configuration
CRM_SERVER_URL = os.environ.get('CRM_SERVER_URL', 'http://localhost:8080')


def get_ticket_by_reference(ticket_reference: str) -> Optional[Dict[str, Any]]:
    """
    Get ticket details from CRM API by ticket reference.
    
    Args:
        ticket_reference: Ticket reference number (e.g., "TKT#1")
    
    Returns:
        Ticket details dict or None if not found
    """
    try:
        # Get all tickets and find the one matching the reference
        url = f"{CRM_SERVER_URL}/api/tickets"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            tickets = response.json()
            if isinstance(tickets, list):
                for ticket in tickets:
                    if ticket.get('ticketReference') == ticket_reference:
                        return ticket
        return None
    except Exception as e:
        print(f"Error fetching ticket from CRM: {e}")
        return None


def get_bookings_by_email(customer_email: str) -> list:
    """
    Get bookings for a customer from CRM API.
    
    Args:
        customer_email: Customer email address
    
    Returns:
        List of booking dicts
    """
    try:
        from urllib.parse import quote_plus
        url = f"{CRM_SERVER_URL}/api/tickets/bookings?email={quote_plus(customer_email)}"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            bookings = response.json()
            if isinstance(bookings, list):
                return bookings
        return []
    except Exception as e:
        print(f"Error fetching bookings from CRM: {e}")
        return []


def generate_ticket_created_email_body(
    customer_name: str,
    ticket_reference: Optional[str] = None,
    issue_description: Optional[str] = None,
    ticket_data: Optional[Dict[str, Any]] = None
) -> str:
    """
    Generate email body for ticket creation notification.
    Uses CRM API data if available to enrich the email content.
    
    Args:
        customer_name: Customer name
        ticket_reference: Ticket reference number
        issue_description: Issue description
        ticket_data: Full ticket data from CRM API (optional)
    
    Returns:
        Email body text
    """
    # Fetch ticket data from CRM if reference is provided
    if ticket_reference and not ticket_data:
        ticket_data = get_ticket_by_reference(ticket_reference)
    
    # Build email body
    body = f"Dear {customer_name},\n\n"
    body += "Thank you for contacting Sherlox Support.\n\n"
    body += "We have received your request and created a support ticket for you.\n\n"
    
    if ticket_data:
        ticket_ref = ticket_data.get('ticketReference') or ticket_reference
        if ticket_ref:
            body += f"Your ticket reference number is: {ticket_ref}\n"
        
        priority = ticket_data.get('priority', 'HIGH')
        body += f"Priority: {priority}\n"
        
        created_at = ticket_data.get('createdAt', '')
        if created_at:
            body += f"Created: {created_at}\n"
        
        body += "\n"
    
    elif ticket_reference:
        body += f"Your ticket reference number is: {ticket_reference}\n\n"
    
    if issue_description:
        # Truncate if too long
        desc = issue_description[:200] + ('...' if len(issue_description) > 200 else '')
        body += f"Issue: {desc}\n\n"
    
    body += "Our team will review your request and get back to you shortly.\n\n"
    body += "If you have any questions, please reply to this email with your ticket reference number.\n\n"
    body += "Best regards,\nSherlox Support Team"
    
    return body


def generate_booking_acknowledgement_email_body(
    customer_name: str,
    booking_id: str,
    ticket_reference: Optional[str] = None,
    customer_email: Optional[str] = None
) -> str:
    """
    Generate email body for booking acknowledgement.
    Uses CRM API to fetch booking details.
    
    Args:
        customer_name: Customer name
        booking_id: Booking ID
        ticket_reference: Ticket reference number
        customer_email: Customer email (to fetch booking details)
    
    Returns:
        Email body text
    """
    booking_data = None
    if customer_email:
        bookings = get_bookings_by_email(customer_email)
        for booking in bookings:
            if booking.get('bookingId') == booking_id:
                booking_data = booking
                break
    
    body = f"Dear {customer_name},\n\n"
    body += f"We have acknowledged your refund request for booking {booking_id}.\n\n"
    
    if booking_data:
        booking_date = booking_data.get('bookingDate', '')
        status = booking_data.get('status', '')
        refund = booking_data.get('refund', '')
        
        if booking_date:
            body += f"Booking Date: {booking_date}\n"
        if status:
            body += f"Status: {status}\n"
        if refund:
            body += f"Refund Status: {refund}\n"
        body += "\n"
    
    if ticket_reference:
        body += f"Ticket Reference: {ticket_reference}\n\n"
    
    body += "We will connect with the bank and respond on the refund status.\n\n"
    body += "You will receive another email shortly with further instructions regarding your refund.\n\n"
    body += "Best regards,\nSherlox Support Team"
    
    return body


def generate_refund_reinitiated_email_body(
    customer_name: str,
    booking_id: str,
    ticket_reference: Optional[str] = None,
    customer_email: Optional[str] = None
) -> str:
    """
    Generate email body for refund reinitiation notification.
    Uses CRM API to fetch booking details.
    
    Args:
        customer_name: Customer name
        booking_id: Booking ID
        ticket_reference: Ticket reference number
        customer_email: Customer email (to fetch booking details)
    
    Returns:
        Email body text
    """
    booking_data = None
    if customer_email:
        bookings = get_bookings_by_email(customer_email)
        for booking in bookings:
            if booking.get('bookingId') == booking_id:
                booking_data = booking
                break
    
    body = f"Dear {customer_name},\n\n"
    body += f"The refund for your booking {booking_id} has been reinitiated.\n\n"
    
    if booking_data:
        booking_date = booking_data.get('bookingDate', '')
        if booking_date:
            body += f"Booking Date: {booking_date}\n"
        body += "\n"
    
    if ticket_reference:
        body += f"You can track the refund status using ticket reference: {ticket_reference}\n\n"
    
    body += "We will update the same on the bank side and keep you posted on the refund status.\n\n"
    body += "Thank you for your patience.\n\n"
    body += "Best regards,\nSherlox Support Team"
    
    return body


def generate_mock_email_response(
    response_type: str,
    customer_name: str,
    customer_email: str,
    **kwargs
) -> Dict[str, Any]:
    """
    Generate a mock email response based on CRM API data.
    
    Args:
        response_type: Type of email ('ticket_created', 'booking_acknowledged', 'refund_reinitiated')
        customer_name: Customer name
        customer_email: Customer email
        **kwargs: Additional parameters (ticket_reference, booking_id, etc.)
    
    Returns:
        Dict with email subject, body, and metadata
    """
    ticket_reference = kwargs.get('ticket_reference')
    booking_id = kwargs.get('booking_id')
    issue_description = kwargs.get('issue_description')
    
    if response_type == 'ticket_created':
        subject = f"Ticket Created - Reference: {ticket_reference}" if ticket_reference else "Ticket Created - Sherlox Support"
        body = generate_ticket_created_email_body(
            customer_name=customer_name,
            ticket_reference=ticket_reference,
            issue_description=issue_description
        )
        
    elif response_type == 'booking_acknowledged':
        subject = f"Booking Refund Acknowledged - {booking_id}" if booking_id else "Booking Refund Acknowledged"
        body = generate_booking_acknowledgement_email_body(
            customer_name=customer_name,
            booking_id=booking_id or '',
            ticket_reference=ticket_reference,
            customer_email=customer_email
        )
        
    elif response_type == 'refund_reinitiated':
        subject = f"Refund Reinitiated - Booking {booking_id}" if booking_id else "Refund Reinitiated"
        body = generate_refund_reinitiated_email_body(
            customer_name=customer_name,
            booking_id=booking_id or '',
            ticket_reference=ticket_reference,
            customer_email=customer_email
        )
        
    else:
        subject = "Sherlox Support Update"
        body = f"Dear {customer_name},\n\nThank you for contacting Sherlox Support.\n\nBest regards,\nSherlox Support Team"
    
    return {
        "status": "success",
        "email": {
            "to": customer_email,
            "subject": subject,
            "body": body,
            "type": response_type
        },
        "crm_data_used": True,
        "metadata": {
            "ticket_reference": ticket_reference,
            "booking_id": booking_id,
            "customer_name": customer_name
        }
    }

