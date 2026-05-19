document.addEventListener('DOMContentLoaded', function() {
    const API_URL = 'http://localhost:8000/api';
    const WS_URL = 'ws://localhost:8000/api/ws';
    
    let salesChart = null;
    let categoryChart = null;

    function updateKPIs(data) {
        document.getElementById('total-revenue').innerText = `$${data.total_revenue.toLocaleString()}`;
        document.getElementById('total-orders').innerText = data.total_orders.toLocaleString();
        document.getElementById('total-customers').innerText = data.total_customers.toLocaleString();
        document.getElementById('avg-order-value').innerText = `$${data.avg_order_value.toFixed(2)}`;
    }

    function fetchKPIs() {
        fetch(`${API_URL}/dashboard/summary`)
            .then(response => response.json())
            .then(updateKPIs);
    }

    function fetchSalesData() {
        Promise.all([
            fetch(`${API_URL}/sales/monthly`).then(r => r.json()),
            fetch(`${API_URL}/forecast/?periods=90`).then(r => r.json())
        ]).then(([historical, forecast]) => {
            const ctx = document.getElementById('salesChart').getContext('2d');
            
            const forecastedMonths = {};
            forecast.forEach(f => {
                const month = new Date(f.ds).toISOString().substring(0, 7);
                forecastedMonths[month] = (forecastedMonths[month] || 0) + f.yhat;
            });

            const labels = [...historical.map(h => h.month)];
            const historicalData = [...historical.map(h => h.revenue)];
            const forecastData = historical.map(() => null);

            Object.keys(forecastedMonths).sort().forEach(month => {
                if (!labels.includes(month)) {
                    labels.push(month);
                    historicalData.push(null);
                    forecastData.push(forecastedMonths[month]);
                } else {
                    const idx = labels.indexOf(month);
                    forecastData[idx] = forecastedMonths[month];
                }
            });

            if (salesChart) {
                salesChart.destroy();
            }

            salesChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [
                        {
                            label: 'Historical Revenue',
                            data: historicalData,
                            borderColor: 'rgb(75, 192, 192)',
                            backgroundColor: 'rgba(75, 192, 192, 0.2)',
                            fill: true,
                            tension: 0.1
                        },
                        {
                            label: 'Forecasted Revenue',
                            data: forecastData,
                            borderColor: 'rgb(255, 99, 132)',
                            borderDash: [5, 5],
                            fill: false,
                            tension: 0.1
                        }
                    ]
                },
                options: {
                    responsive: true,
                    animation: {
                        duration: 500 // Smooth transition
                    },
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        });
    }

    function fetchCategoryData() {
        fetch(`${API_URL}/sales/category`)
            .then(response => response.json())
            .then(data => {
                const ctx = document.getElementById('categoryChart').getContext('2d');
                
                if (categoryChart) {
                    categoryChart.destroy();
                }

                categoryChart = new Chart(ctx, {
                    type: 'pie',
                    data: {
                        labels: data.map(item => item.category),
                        datasets: [{
                            data: data.map(item => item.revenue),
                            backgroundColor: [
                                'rgb(255, 99, 132)',
                                'rgb(54, 162, 235)',
                                'rgb(255, 205, 86)',
                                'rgb(75, 192, 192)',
                                'rgb(153, 102, 255)',
                                'rgb(255, 159, 64)',
                                'rgb(201, 203, 207)',
                                'rgb(255, 99, 132)',
                                'rgb(54, 162, 235)',
                                'rgb(255, 205, 86)'
                            ]
                        }]
                    },
                    options: {
                        responsive: true,
                        animation: {
                            duration: 500
                        }
                    }
                });
            });
    }

    // Initial Load
    fetchKPIs();
    fetchSalesData();
    fetchCategoryData();

    // WebSocket for Real-time Updates
    function connectWebSocket() {
        const socket = new WebSocket(WS_URL);

        socket.onopen = function() {
            console.log("Connected to Real-time Data Stream");
        };

        socket.onmessage = function(event) {
            const message = JSON.parse(event.data);
            if (message.type === 'kpi_update') {
                console.log("Received data update");
                updateKPIs(message.data);
                // Also refresh charts to reflect potential underlying data changes
                fetchSalesData();
                fetchCategoryData();
            }
        };

        socket.onclose = function() {
            console.log("Disconnected from Real-time Data Stream. Retrying in 5s...");
            setTimeout(connectWebSocket, 5000);
        };

        socket.onerror = function(err) {
            console.error("WebSocket Error: ", err);
            socket.close();
        };
    }

    connectWebSocket();
});
