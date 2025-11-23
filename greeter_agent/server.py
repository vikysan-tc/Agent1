"""
Greeter Agent Server
A Python server that handles ticket creation from email processor payloads.

This server:
1. Receives webhook POST requests from email_processor with JSON payloads
2. Directly processes the payload and creates tickets using the greeter tools
3. Sends email notifications to customers after ticket creation
"""

import os
import json
import logging
from typing import Dict, Any, Optional
from flask import Flask, request, jsonify

# Configure logging first
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import greeter tools directly
try:
    from greeter_tools import create_ticket_from_json
except ImportError:
    # Try relative import if running as package
    try:
        from .greeter_tools import create_ticket_from_json
    except ImportError:
        logger.error("Failed to import greeter_tools. Make sure greeter_tools.py is in the same directory.")
        create_ticket_from_json = None

app = Flask(__name__)

# Environment variables
WEBHOOK_PORT = int(os.environ.get('WEBHOOK_PORT', '5000'))
WEBHOOK_HOST = os.environ.get('WEBHOOK_HOST', '0.0.0.0')


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "healthy", "service": "greeter_agent"}), 200


@app.route('/webhook', methods=['POST'])
def webhook_handler():
    """
    Webhook endpoint to receive payloads from email_processor.
    
    Expected payload format:
    {
        "CustomerName": "...",
        "CustomerEmail": "...",
        "CustomerPhoneNumber": "...",  // optional
        "IssueDescription": "...",
        "Priority": "HIGH|MEDIUM|LOW"  // optional, defaults to HIGH
    }
    
    This endpoint:
    1. Validates the payload
    2. Calls create_ticket_from_json tool directly
    3. Returns the result (ticket creation already handles email sending)
    """
    try:
        # Get JSON payload
        payload = request.get_json()
        if not payload:
            return jsonify({
                "status": "error",
                "error": "No JSON payload provided"
            }), 400

        logger.info(f"Received webhook payload: {json.dumps(payload, indent=2)}")

        # Validate required fields
        required_fields = ["CustomerEmail", "IssueDescription"]
        missing_fields = [field for field in required_fields if not payload.get(field)]
        if missing_fields:
            return jsonify({
                "status": "error",
                "error": f"Missing required fields: {', '.join(missing_fields)}"
            }), 400

        # Check if greeter_tools is available
        if create_ticket_from_json is None:
            return jsonify({
                "status": "error",
                "error": "Greeter tools not available. Cannot process ticket creation."
            }), 500

        # Directly call the create_ticket_from_json tool
        # This function will:
        # 1. Create ticket via CRM API
        # 2. Send email notification to customer (handled inside the tool)
        result = create_ticket_from_json(payload)

        logger.info(f"Ticket creation result: {json.dumps(result, indent=2, default=str)}")

        # Return the result
        return jsonify({
            "status": "success",
            "result": result
        }), 200

    except Exception as e:
        logger.error(f"Error processing webhook: {e}", exc_info=True)
        return jsonify({
            "status": "error",
            "error": f"Internal server error: {str(e)}"
        }), 500


@app.route('/chat', methods=['POST'])
def chat_handler():
    """
    Direct chat endpoint for testing the agent.
    
    Expected payload:
    {
        "message": "JSON payload string or dict"
    }
    
    If message is a JSON string or dict, it will be processed as a ticket creation request.
    """
    try:
        payload = request.get_json()
        if not payload or 'message' not in payload:
            return jsonify({
                "status": "error",
                "error": "Missing 'message' field in payload"
            }), 400

        message = payload['message']
        logger.info(f"Received chat message: {message}")

        # Check if greeter_tools is available
        if create_ticket_from_json is None:
            return jsonify({
                "status": "error",
                "error": "Greeter tools not available. Cannot process ticket creation."
            }), 500

        # Try to parse message as JSON if it's a string
        if isinstance(message, str):
            try:
                message = json.loads(message)
            except json.JSONDecodeError:
                # If not JSON, return error
                return jsonify({
                    "status": "error",
                    "error": "Message must be a valid JSON string or object for ticket creation"
                }), 400

        # Process as ticket creation request
        result = create_ticket_from_json(message)

        logger.info(f"Ticket creation result: {json.dumps(result, indent=2, default=str)}")

        return jsonify({
            "status": "success",
            "result": result
        }), 200

    except Exception as e:
        logger.error(f"Error processing chat: {e}", exc_info=True)
        return jsonify({
            "status": "error",
            "error": f"Internal server error: {str(e)}"
        }), 500


if __name__ == '__main__':
    # Validate that greeter tools are available
    if create_ticket_from_json is None:
        logger.error(
            "Greeter tools not available. Cannot start server.\n"
            "Make sure greeter_tools.py is in the same directory as server.py"
        )
        exit(1)

    logger.info(f"Starting Greeter Agent Server on {WEBHOOK_HOST}:{WEBHOOK_PORT}")
    logger.info("Server is ready to receive webhook requests from email_processor")
    logger.info("Ticket creation and email notifications will be handled automatically")

    app.run(
        host=WEBHOOK_HOST,
        port=WEBHOOK_PORT,
        debug=os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    )

