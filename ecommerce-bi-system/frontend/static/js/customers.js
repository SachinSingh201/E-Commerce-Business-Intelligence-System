document.addEventListener('DOMContentLoaded', function() {
    const API_URL = 'http://localhost:8000/api';

    if (window.location.pathname === '/customers') {
        // Fetch Latest Customers
        fetch(`${API_URL}/customers/latest`)
            .then(response => response.json())
            .then(data => {
                const tableBody = document.getElementById('latest-customers-body');
                data.forEach(customer => {
                    const row = `
                        <tr>
                            <td>${customer.customer_id}</td>
                            <td>${customer.order_time}</td>
                            <td>$${customer.monetary.toFixed(2)}</td>
                        </tr>
                    `;
                    tableBody.innerHTML += row;
                });
            });

        // Fetch Segmentation
        fetch(`${API_URL}/customers/segmentation`)
            .then(response => response.json())
            .then(data => {
                const tableBody = document.getElementById('customer-table-body');
                data.forEach(customer => {
                    const row = `
                        <tr>
                            <td>${customer.customer_id}</td>
                            <td>${customer.recency}</td>
                            <td>${customer.frequency}</td>
                            <td>$${customer.monetary.toFixed(2)}</td>
                            <td><span class="badge bg-${getBadgeColor(customer.cluster)}">Cluster ${customer.cluster}</span></td>
                        </tr>
                    `;
                    tableBody.innerHTML += row;
                });
            });
    }

    function getBadgeColor(cluster) {
        const colors = ['primary', 'success', 'info', 'warning'];
        return colors[cluster] || 'secondary';
    }
});
