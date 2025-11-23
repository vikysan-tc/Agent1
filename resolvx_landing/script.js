// Target email - sends directly to this address
const TARGET_EMAIL = 'reachus.sherlox@gmail.com';

// Form submission handler
document.getElementById('complaintForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const submitBtn = document.getElementById('submitBtn');
    const messageDiv = document.getElementById('message');
    const form = e.target;
    
    // Get form values
    const personalEmail = document.getElementById('personalEmail').value.trim();
    const customerName = document.getElementById('customerName').value.trim();
    const companyName = document.getElementById('companyName').value.trim();
    const phoneNumber = document.getElementById('phoneNumber').value.trim();
    const problemDescription = document.getElementById('problemDescription').value.trim();
    
    // Validate form
    if (!personalEmail || !customerName || !companyName || !problemDescription) {
        showMessage('Please fill in all required fields.', 'error');
        return;
    }
    
    // Validate email format
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(personalEmail)) {
        showMessage('Please enter a valid email address.', 'error');
        return;
    }
    
    // Disable submit button and show loading
    submitBtn.disabled = true;
    submitBtn.classList.add('loading');
    messageDiv.classList.remove('show');
    
    try {
        // Construct email content
        const emailSubject = `Complaint: ${companyName}`;
        const emailBody = `Dear CarePilot - the customer's co-pilot Team,

I would like to raise a complaint regarding ${companyName}.

Customer Information:
- Name: ${customerName}
- Email: ${personalEmail}
${phoneNumber ? `- Phone: ${phoneNumber}` : ''}

Problem Description:
${problemDescription}

Please process this complaint and ensure it reaches the appropriate team for resolution.

Thank you,
${customerName}`;

        // Open Gmail compose window
        openGmailCompose(personalEmail, customerName, emailSubject, emailBody);
        
        // Success message
        showMessage('Gmail will open in a new window. Please review and send the email to complete your complaint submission.', 'success');
        
        // Reset form after a short delay
        setTimeout(() => {
            form.reset();
        }, 1000);
        
    } catch (error) {
        console.error('Error submitting complaint:', error);
        showMessage('There was an error opening Gmail. Please try again or contact support directly.', 'error');
    } finally {
        // Re-enable submit button
        submitBtn.disabled = false;
        submitBtn.classList.remove('loading');
    }
});

// Open Gmail compose window with pre-filled email
function openGmailCompose(fromEmail, fromName, subject, body) {
    // Encode the email body and subject for URL
    const encodedSubject = encodeURIComponent(subject);
    const encodedBody = encodeURIComponent(body);
    
    // Create Gmail compose URL
    // This will open Gmail in a new tab/window
    const gmailUrl = `https://mail.google.com/mail/?view=cm&fs=1&to=${TARGET_EMAIL}&su=${encodedSubject}&body=${encodedBody}`;
    
    // Try to open Gmail in a new window
    const gmailWindow = window.open(gmailUrl, '_blank');
    
    // If popup was blocked, try alternative: use mailto as fallback
    if (!gmailWindow || gmailWindow.closed || typeof gmailWindow.closed === 'undefined') {
        // Fallback to mailto link (will open default email client)
        const mailtoLink = `mailto:${TARGET_EMAIL}?subject=${encodedSubject}&body=${encodedBody}&reply-to=${encodeURIComponent(fromEmail)}`;
        window.location.href = mailtoLink;
    }
}

// Show message to user
function showMessage(text, type) {
    const messageDiv = document.getElementById('message');
    messageDiv.textContent = text;
    messageDiv.className = `message ${type} show`;
    
    // Auto-hide after 10 seconds for success messages
    if (type === 'success') {
        setTimeout(() => {
            messageDiv.classList.remove('show');
        }, 10000);
    }
}

// Add smooth scroll behavior
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Load dashboard metrics for the metrics bar
async function loadDashboardMetrics() {
    // Use local proxy if available, otherwise direct API (may have CORS issues)
    const USE_LOCAL_PROXY = true; // Set to false to use direct API
    const LOCAL_PROXY_URL = 'http://localhost:8001';
    const CRM_SERVER_URL = 'https://desperate-bird-personal-viky-c10a64c7.koyeb.app/crmserver';
    const TICKETS_API_URL = USE_LOCAL_PROXY 
        ? `${LOCAL_PROXY_URL}/api/tickets`
        : `${CRM_SERVER_URL}/api/tickets`;
    
    const metricsBar = document.getElementById('dashboardMetricsBar');
    if (!metricsBar) return;
    
    try {
        // Create AbortController for timeout
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 10000); // 10 second timeout for metrics
        
        const response = await fetch(TICKETS_API_URL, {
            method: 'GET',
            headers: {
                'Accept': 'application/json',
            },
            signal: controller.signal
        });
        
        clearTimeout(timeoutId);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        const tickets = Array.isArray(data) ? data : [data];
        
        // Calculate metrics
        const totalTickets = tickets.length;
        const highPriorityTickets = tickets.filter(t => 
            (t.priority || '').toUpperCase() === 'HIGH'
        ).length;
        const resolvedTickets = tickets.filter(t => 
            (t.status || '').toUpperCase() === 'RESOLVED' || 
            (t.status || '').toUpperCase() === 'CLOSED'
        ).length;
        
        // Update metrics display
        document.getElementById('metricTotalTickets').textContent = totalTickets;
        document.getElementById('metricHighPriority').textContent = highPriorityTickets;
        document.getElementById('metricResolved').textContent = resolvedTickets;
        
        // Remove loading state
        metricsBar.classList.remove('loading');
        
    } catch (error) {
        console.error('Error loading dashboard metrics:', error);
        // Set default values on error
        document.getElementById('metricTotalTickets').textContent = '-';
        document.getElementById('metricHighPriority').textContent = '-';
        document.getElementById('metricResolved').textContent = '-';
        metricsBar.classList.remove('loading');
    }
}

// Load metrics when page loads
document.addEventListener('DOMContentLoaded', () => {
    const metricsBar = document.getElementById('dashboardMetricsBar');
    if (metricsBar) {
        metricsBar.classList.add('loading');
        loadDashboardMetrics();
        
        // Refresh metrics every 30 seconds
        setInterval(loadDashboardMetrics, 30000);
    }
});

