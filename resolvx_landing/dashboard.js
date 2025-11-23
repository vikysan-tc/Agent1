// CRM API Configuration
// For local development with CORS issues, use the proxy server:
// Run: python proxy_server.py (in a separate terminal)
const USE_LOCAL_PROXY = true; // Set to false to use direct API (requires CORS on server)
const LOCAL_PROXY_URL = 'http://localhost:8001';
const CRM_SERVER_URL = 'https://desperate-bird-personal-viky-c10a64c7.koyeb.app/crmserver';
const TICKETS_API_URL = USE_LOCAL_PROXY 
    ? `${LOCAL_PROXY_URL}/api/tickets`
    : `${CRM_SERVER_URL}/api/tickets`;

// Global state
let allTickets = [];
let filteredTickets = [];
let companyChart = null;
let priorityChart = null;

// Initialize dashboard on load
document.addEventListener('DOMContentLoaded', () => {
    loadDashboard();
    setupEventListeners();
});

// Setup event listeners
function setupEventListeners() {
    document.getElementById('refreshBtn').addEventListener('click', loadDashboard);
    document.getElementById('filterPriority').addEventListener('change', applyFilters);
    document.getElementById('filterCompany').addEventListener('change', applyFilters);
    document.getElementById('productCompanyFilter').addEventListener('change', showProductAnalysis);
}

// Load dashboard data
async function loadDashboard() {
    const loadingState = document.getElementById('loadingState');
    const errorState = document.getElementById('errorState');
    const dashboardContent = document.getElementById('dashboardContent');
    
    // Show loading state
    loadingState.style.display = 'block';
    errorState.style.display = 'none';
    dashboardContent.style.display = 'none';
    
    try {
        // Create AbortController for timeout
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 30000);
        
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
        console.log('Received data:', data); // Debug log
        
        // Handle the response - it should be an array
        if (Array.isArray(data)) {
            allTickets = data;
        } else if (data && typeof data === 'object') {
            // If it's a single object, wrap it in an array
            allTickets = [data];
        } else {
            throw new Error('Invalid response format: expected array or object');
        }
        
        console.log('Processed tickets:', allTickets.length); // Debug log
        
        // Hide loading, show content
        loadingState.style.display = 'none';
        dashboardContent.style.display = 'block';
        
        // Render dashboard
        renderDashboard();
        
    } catch (error) {
        console.error('Error loading dashboard:', error);
        console.error('Error details:', {
            name: error.name,
            message: error.message,
            stack: error.stack
        });
        
        loadingState.style.display = 'none';
        errorState.style.display = 'block';
        
        let errorMsg = `Failed to load dashboard: ${error.message}`;
        if (error.name === 'AbortError') {
            errorMsg = 'Request timed out. Please check your connection and try again.';
        } else if (error.message.includes('Failed to fetch') || error.message.includes('NetworkError') || error.name === 'TypeError') {
            errorMsg = 'Network/CORS error. The CRM server may not be allowing requests from this origin. ' +
                      'Please check: 1) Server is running, 2) CORS headers are configured, 3) Check browser console for details.';
        }
        
        document.getElementById('errorMessage').textContent = errorMsg;
        
        // Also log the API URL for debugging
        console.log('Attempted to fetch from:', TICKETS_API_URL);
    }
}

// Render all dashboard components
function renderDashboard() {
    try {
        updateSummaryCards();
        populateCompanyFilter();
        populateProductCompanyFilter();
        applyFilters();
        renderCompanyMetrics();
        renderPriorityChart();
        renderHighPriorityCustomers();
    } catch (error) {
        console.error('Error rendering dashboard:', error);
        const errorState = document.getElementById('errorState');
        const dashboardContent = document.getElementById('dashboardContent');
        errorState.style.display = 'block';
        dashboardContent.style.display = 'none';
        document.getElementById('errorMessage').textContent = 
            `Error rendering dashboard: ${error.message}`;
    }
}

// Update summary cards
function updateSummaryCards() {
    const totalTickets = allTickets.length;
    const highPriorityTickets = allTickets.filter(t => 
        (t.priority || '').toUpperCase() === 'HIGH'
    ).length;
    const resolvedTickets = allTickets.filter(t => 
        (t.status || '').toUpperCase() === 'RESOLVED' || 
        (t.status || '').toUpperCase() === 'CLOSED'
    ).length;
    
    // Get unique companies
    const companies = new Set();
    allTickets.forEach(ticket => {
        const company = ticket.companyName || ticket.company || 'Unknown';
        if (company && company !== 'Unknown') {
            companies.add(company);
        }
    });
    const totalCompanies = companies.size;
    
    document.getElementById('totalTickets').textContent = totalTickets;
    document.getElementById('highPriorityTickets').textContent = highPriorityTickets;
    document.getElementById('resolvedTickets').textContent = resolvedTickets;
    document.getElementById('totalCompanies').textContent = totalCompanies;
}

// Populate company filter
function populateCompanyFilter() {
    const filter = document.getElementById('filterCompany');
    const companies = new Set();
    
    allTickets.forEach(ticket => {
        const company = ticket.companyName || ticket.company || 'Unknown';
        if (company && company !== 'Unknown') {
            companies.add(company);
        }
    });
    
    // Clear existing options except "All Companies"
    filter.innerHTML = '<option value="all">All Companies</option>';
    
    // Add company options
    Array.from(companies).sort().forEach(company => {
        const option = document.createElement('option');
        option.value = company;
        option.textContent = company;
        filter.appendChild(option);
    });
}

// Populate product company filter
function populateProductCompanyFilter() {
    const filter = document.getElementById('productCompanyFilter');
    const companies = new Set();
    
    allTickets.forEach(ticket => {
        const company = ticket.companyName || ticket.company || 'Unknown';
        if (company && company !== 'Unknown') {
            companies.add(company);
        }
    });
    
    // Clear existing options
    filter.innerHTML = '<option value="">Select Company</option>';
    
    // Add company options
    Array.from(companies).sort().forEach(company => {
        const option = document.createElement('option');
        option.value = company;
        option.textContent = company;
        filter.appendChild(option);
    });
}

// Apply filters
function applyFilters() {
    const priorityFilter = document.getElementById('filterPriority').value;
    const companyFilter = document.getElementById('filterCompany').value;
    
    filteredTickets = allTickets.filter(ticket => {
        const priority = (ticket.priority || '').toUpperCase();
        const company = ticket.companyName || ticket.company || 'Unknown';
        
        const priorityMatch = priorityFilter === 'all' || priority === priorityFilter.toUpperCase();
        const companyMatch = companyFilter === 'all' || company === companyFilter;
        
        return priorityMatch && companyMatch;
    });
    
    renderTicketList();
}

// Render ticket list
function renderTicketList() {
    const ticketList = document.getElementById('ticketList');
    
    if (filteredTickets.length === 0) {
        ticketList.innerHTML = '<p class="empty-state">No tickets found matching the filters.</p>';
        return;
    }
    
    // Sort by priority and date (newest first)
    const sortedTickets = [...filteredTickets].sort((a, b) => {
        const priorityOrder = { 'HIGH': 3, 'MEDIUM': 2, 'LOW': 1 };
        const aPriority = priorityOrder[(a.priority || '').toUpperCase()] || 0;
        const bPriority = priorityOrder[(b.priority || '').toUpperCase()] || 0;
        
        if (aPriority !== bPriority) {
            return bPriority - aPriority;
        }
        
        const aDate = new Date(a.createdAt || a.created_at || 0);
        const bDate = new Date(b.createdAt || b.created_at || 0);
        return bDate - aDate;
    });
    
    ticketList.innerHTML = sortedTickets.map(ticket => createTicketCard(ticket)).join('');
    
    // Add event listeners to ticket cards
    ticketList.querySelectorAll('.ticket-item').forEach((item, index) => {
        const ticket = sortedTickets[index];
        item.addEventListener('click', () => openTicketModal(ticket));
        
        // Add click handler for View Details button
        const viewBtn = item.querySelector('.btn-action-primary');
        if (viewBtn) {
            viewBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                openTicketModal(ticket);
            });
        }
    });
}

// Create ticket card HTML
function createTicketCard(ticket) {
    const ticketRef = escapeHtml(ticket.ticketReference || ticket.ticket_reference || ticket.id || 'N/A');
    const customerName = escapeHtml(ticket.customerName || ticket.customer_name || 'Unknown');
    const customerEmail = escapeHtml(ticket.customerEmail || ticket.customer_email || 'N/A');
    const company = escapeHtml(ticket.companyName || ticket.company || 'Unknown');
    const priority = (ticket.priority || 'MEDIUM').toUpperCase();
    const status = escapeHtml(ticket.status || 'OPEN');
    const issueDesc = escapeHtml(ticket.issueDescription || ticket.issue_description || 'No description');
    const createdAt = ticket.createdAt || ticket.created_at || 'N/A';
    const phone = escapeHtml(ticket.customerPhoneNumber || ticket.customer_phone || 'N/A');
    
    return `
        <div class="ticket-item">
            <div class="ticket-header">
                <div>
                    <span class="ticket-ref">${ticketRef}</span>
                </div>
                <span class="ticket-priority priority-${priority}">${priority}</span>
            </div>
            <div class="ticket-info">
                <div class="ticket-info-item">
                    <span class="ticket-info-label">Customer</span>
                    <span class="ticket-info-value">${customerName}</span>
                </div>
                <div class="ticket-info-item">
                    <span class="ticket-info-label">Company</span>
                    <span class="ticket-info-value">${company}</span>
                </div>
                <div class="ticket-info-item">
                    <span class="ticket-info-label">Status</span>
                    <span class="ticket-info-value">${status}</span>
                </div>
                <div class="ticket-info-item">
                    <span class="ticket-info-label">Created</span>
                    <span class="ticket-info-value">${formatDate(createdAt)}</span>
                </div>
            </div>
            <div class="ticket-actions">
                <button class="btn-action btn-action-primary">
                    <i class="fas fa-eye"></i> View Details
                </button>
                <button class="btn-action btn-action-secondary" onclick="event.stopPropagation(); updateTicketStatus('${ticketRef}', 'IN_PROGRESS')">
                    <i class="fas fa-play"></i> Start
                </button>
                <button class="btn-action btn-action-secondary" onclick="event.stopPropagation(); updateTicketStatus('${ticketRef}', 'RESOLVED')">
                    <i class="fas fa-check"></i> Resolve
                </button>
            </div>
        </div>
    `;
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Format date
function formatDate(dateString) {
    if (!dateString || dateString === 'N/A') return 'N/A';
    try {
        const date = new Date(dateString);
        return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    } catch {
        return dateString;
    }
}

// Render company metrics chart
function renderCompanyMetrics() {
    const ctx = document.getElementById('companyChart');
    if (!ctx) return;
    
    // Destroy existing chart
    if (companyChart) {
        companyChart.destroy();
    }
    
    // Calculate company metrics
    const companyStats = {};
    allTickets.forEach(ticket => {
        // Try to extract company from issue description if not present
        let company = ticket.companyName || ticket.company;
        if (!company && ticket.issueDescription) {
            // Try to extract company name from issue description
            const issue = ticket.issueDescription.toLowerCase();
            // This is a fallback - ideally company should come from the API
            company = 'General';
        }
        company = company || 'General';
        
        if (!companyStats[company]) {
            companyStats[company] = { total: 0, high: 0, medium: 0, low: 0 };
        }
        companyStats[company].total++;
        const priority = (ticket.priority || 'MEDIUM').toUpperCase();
        if (priority === 'HIGH') companyStats[company].high++;
        else if (priority === 'MEDIUM') companyStats[company].medium++;
        else companyStats[company].low++;
    });
    
    const companies = Object.keys(companyStats);
    const totals = companies.map(c => companyStats[c].total);
    const highs = companies.map(c => companyStats[c].high);
    
    // Check if Chart is available
    if (typeof Chart === 'undefined') {
        console.error('Chart.js is not loaded');
        return;
    }
    
    // Handle empty data case
    if (companies.length === 0) {
        ctx.parentElement.innerHTML = '<p class="empty-state">No company data available</p>';
        return;
    }
    
    companyChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: companies,
            datasets: [
                {
                    label: 'Total Tickets',
                    data: totals,
                    backgroundColor: 'rgba(15, 98, 254, 0.6)',
                    borderColor: '#0f62fe',
                    borderWidth: 2
                },
                {
                    label: 'High Priority',
                    data: highs,
                    backgroundColor: 'rgba(245, 158, 11, 0.6)',
                    borderColor: '#f59e0b',
                    borderWidth: 2
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    labels: {
                        color: '#ffffff'
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        color: '#a0a0a0'
                    },
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    }
                },
                x: {
                    ticks: {
                        color: '#a0a0a0'
                    },
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    }
                }
            }
        }
    });
}

// Render priority distribution chart
function renderPriorityChart() {
    const ctx = document.getElementById('priorityChart');
    if (!ctx) return;
    
    // Check if Chart is available
    if (typeof Chart === 'undefined') {
        console.error('Chart.js is not loaded');
        return;
    }
    
    // Destroy existing chart
    if (priorityChart) {
        priorityChart.destroy();
    }
    
    const priorities = { HIGH: 0, MEDIUM: 0, LOW: 0 };
    allTickets.forEach(ticket => {
        const priority = (ticket.priority || 'MEDIUM').toUpperCase();
        if (priorities[priority] !== undefined) {
            priorities[priority]++;
        }
    });
    
    priorityChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['High', 'Medium', 'Low'],
            datasets: [{
                data: [priorities.HIGH, priorities.MEDIUM, priorities.LOW],
                backgroundColor: [
                    'rgba(245, 158, 11, 0.8)',
                    'rgba(59, 130, 246, 0.8)',
                    'rgba(16, 185, 129, 0.8)'
                ],
                borderColor: [
                    '#f59e0b',
                    '#3b82f6',
                    '#10b981'
                ],
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        color: '#ffffff',
                        padding: 15
                    }
                }
            }
        }
    });
}

// Render high priority customers
function renderHighPriorityCustomers() {
    const container = document.getElementById('highPriorityCustomers');
    
    // Get customers with high priority tickets
    const customerStats = {};
    allTickets.forEach(ticket => {
        const priority = (ticket.priority || '').toUpperCase();
        if (priority === 'HIGH') {
            const email = ticket.customerEmail || ticket.customer_email || 'unknown';
            const name = ticket.customerName || ticket.customer_name || 'Unknown';
            
            if (!customerStats[email]) {
                customerStats[email] = {
                    name: name,
                    email: email,
                    count: 0,
                    companies: new Set()
                };
            }
            customerStats[email].count++;
            const company = ticket.companyName || ticket.company || 'Unknown';
            if (company !== 'Unknown') {
                customerStats[email].companies.add(company);
            }
        }
    });
    
    const customers = Object.values(customerStats)
        .sort((a, b) => b.count - a.count)
        .slice(0, 10); // Top 10
    
    if (customers.length === 0) {
        container.innerHTML = '<p class="empty-state">No high priority customers found.</p>';
        return;
    }
    
    container.innerHTML = customers.map(customer => `
        <div class="customer-item">
            <div class="customer-info">
                <h4>${escapeHtml(customer.name)}</h4>
                <p>${escapeHtml(customer.email)}</p>
                <p style="font-size: 0.85rem; color: var(--text-secondary); margin-top: 0.5rem;">
                    Companies: ${escapeHtml(Array.from(customer.companies).join(', ') || 'N/A')}
                </p>
            </div>
            <div class="customer-stats">
                <div class="customer-stat">
                    <div class="customer-stat-value">${customer.count}</div>
                    <div class="customer-stat-label">High Priority<br>Tickets</div>
                </div>
            </div>
        </div>
    `).join('');
}

// Show product analysis for selected company
function showProductAnalysis() {
    const company = document.getElementById('productCompanyFilter').value;
    const container = document.getElementById('productAnalysis');
    
    if (!company) {
        container.innerHTML = '<p class="empty-state">Select a company to view product-wise ticket analysis</p>';
        return;
    }
    
    // Filter tickets for this company
    const companyTickets = allTickets.filter(ticket => {
        const ticketCompany = ticket.companyName || ticket.company || 'Unknown';
        return ticketCompany === company;
    });
    
    if (companyTickets.length === 0) {
        container.innerHTML = '<p class="empty-state">No tickets found for this company.</p>';
        return;
    }
    
    // Analyze by product (extract from issue description or use a default)
    // For privacy, we'll group by issue keywords/categories
    const productStats = {};
    
    companyTickets.forEach(ticket => {
        const issue = (ticket.issueDescription || ticket.issue_description || '').toLowerCase();
        let product = 'General';
        
        // Simple keyword-based categorization (can be enhanced)
        if (issue.includes('booking') || issue.includes('reservation')) {
            product = 'Booking/Reservation';
        } else if (issue.includes('payment') || issue.includes('refund')) {
            product = 'Payment/Refund';
        } else if (issue.includes('delivery') || issue.includes('shipping')) {
            product = 'Delivery/Shipping';
        } else if (issue.includes('account') || issue.includes('login')) {
            product = 'Account/Access';
        } else if (issue.includes('product') || issue.includes('item')) {
            product = 'Product/Item';
        } else if (issue.includes('service') || issue.includes('support')) {
            product = 'Service/Support';
        }
        
        if (!productStats[product]) {
            productStats[product] = { total: 0, high: 0, medium: 0, low: 0 };
        }
        productStats[product].total++;
        const priority = (ticket.priority || 'MEDIUM').toUpperCase();
        if (priority === 'HIGH') productStats[product].high++;
        else if (priority === 'MEDIUM') productStats[product].medium++;
        else productStats[product].low++;
    });
    
    // Create chart
    const canvas = document.createElement('canvas');
    container.innerHTML = '';
    container.appendChild(canvas);
    
    const products = Object.keys(productStats);
    const totals = products.map(p => productStats[p].total);
    const highs = products.map(p => productStats[p].high);
    
    new Chart(canvas, {
        type: 'bar',
        data: {
            labels: products,
            datasets: [
                {
                    label: 'Total Tickets',
                    data: totals,
                    backgroundColor: 'rgba(15, 98, 254, 0.6)',
                    borderColor: '#0f62fe',
                    borderWidth: 2
                },
                {
                    label: 'High Priority',
                    data: highs,
                    backgroundColor: 'rgba(245, 158, 11, 0.6)',
                    borderColor: '#f59e0b',
                    borderWidth: 2
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    labels: {
                        color: '#ffffff'
                    }
                },
                title: {
                    display: true,
                    text: `Product Analysis for ${company}`,
                    color: '#ffffff',
                    font: {
                        size: 16
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        color: '#a0a0a0'
                    },
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    }
                },
                x: {
                    ticks: {
                        color: '#a0a0a0'
                    },
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    }
                }
            }
        }
    });
}

// Open ticket modal
function openTicketModal(ticket) {
    const modal = document.getElementById('ticketModal');
    const modalBody = document.getElementById('modalBody');
    const modalTitle = document.getElementById('modalTitle');
    
    const ticketRef = escapeHtml(ticket.ticketReference || ticket.ticket_reference || ticket.id || 'N/A');
    modalTitle.textContent = `Ticket: ${ticketRef}`;
    
    modalBody.innerHTML = `
        <div class="ticket-detail-item">
            <div class="ticket-detail-label">Ticket Reference</div>
            <div class="ticket-detail-value">${ticketRef}</div>
        </div>
        <div class="ticket-detail-item">
            <div class="ticket-detail-label">Customer Name</div>
            <div class="ticket-detail-value">${escapeHtml(ticket.customerName || ticket.customer_name || 'N/A')}</div>
        </div>
        <div class="ticket-detail-item">
            <div class="ticket-detail-label">Customer Email</div>
            <div class="ticket-detail-value">${escapeHtml(ticket.customerEmail || ticket.customer_email || 'N/A')}</div>
        </div>
        <div class="ticket-detail-item">
            <div class="ticket-detail-label">Customer Phone</div>
            <div class="ticket-detail-value">${escapeHtml(ticket.customerPhoneNumber || ticket.customer_phone || 'N/A')}</div>
        </div>
        <div class="ticket-detail-item">
            <div class="ticket-detail-label">Company</div>
            <div class="ticket-detail-value">${escapeHtml(ticket.companyName || ticket.company || 'N/A')}</div>
        </div>
        <div class="ticket-detail-item">
            <div class="ticket-detail-label">Priority</div>
            <div class="ticket-detail-value">
                <span class="ticket-priority priority-${(ticket.priority || 'MEDIUM').toUpperCase()}">
                    ${(ticket.priority || 'MEDIUM').toUpperCase()}
                </span>
            </div>
        </div>
        <div class="ticket-detail-item">
            <div class="ticket-detail-label">Status</div>
            <div class="ticket-detail-value">${escapeHtml(ticket.status || 'OPEN')}</div>
        </div>
        <div class="ticket-detail-item">
            <div class="ticket-detail-label">Created At</div>
            <div class="ticket-detail-value">${formatDate(ticket.createdAt || ticket.created_at)}</div>
        </div>
        <div class="ticket-detail-item">
            <div class="ticket-detail-label">Issue Description</div>
            <div class="ticket-detail-value" style="white-space: pre-wrap; line-height: 1.6;">
                ${escapeHtml(ticket.issueDescription || ticket.issue_description || 'No description provided')}
            </div>
        </div>
        <div style="margin-top: 2rem; display: flex; gap: 1rem; flex-wrap: wrap;">
            <button class="btn-action btn-action-primary" onclick="updateTicketStatus('${ticketRef}', 'IN_PROGRESS')">
                <i class="fas fa-play"></i> Mark as In Progress
            </button>
            <button class="btn-action btn-action-primary" onclick="updateTicketStatus('${ticketRef}', 'RESOLVED')">
                <i class="fas fa-check"></i> Mark as Resolved
            </button>
            <button class="btn-action btn-action-secondary" onclick="closeTicketModal()">
                <i class="fas fa-times"></i> Close
            </button>
        </div>
    `;
    
    modal.classList.add('show');
}

// Close ticket modal
function closeTicketModal() {
    const modal = document.getElementById('ticketModal');
    modal.classList.remove('show');
}

// Update ticket status (placeholder - would need API endpoint)
function updateTicketStatus(ticketRef, status) {
    // This is a placeholder - in a real implementation, you would call an API endpoint
    alert(`Ticket ${ticketRef} status would be updated to ${status}.\n\nNote: This requires a PUT/PATCH endpoint on the CRM API to update ticket status.`);
    
    // Close modal and refresh
    closeTicketModal();
    // Optionally refresh dashboard after a delay
    // setTimeout(loadDashboard, 1000);
}

// Close modal when clicking outside
document.getElementById('ticketModal').addEventListener('click', (e) => {
    if (e.target.id === 'ticketModal') {
        closeTicketModal();
    }
});

