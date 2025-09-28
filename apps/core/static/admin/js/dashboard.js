document.addEventListener('DOMContentLoaded', () => {
    // This script assumes the global Chart.js defaults have been set
    // in the inline script tag of the index.html template.
    const dataUrl = '/api/v1/reports/dashboard-data/';

    fetch(dataUrl)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log("Dashboard data received:", data);
            populateKpis(data.kpi);
            renderMonthlySalesChart(data.charts.monthly_sales);
            renderTopProductsRevenueChart(data.charts.top_products_revenue);
            renderTopProductsQuantityChart(data.charts.top_products_quantity);
        })
        .catch(error => {
            console.error("Failed to fetch or render dashboard data:", error);
        });

    function populateKpis(kpiData) {
        document.getElementById('kpi-revenue-today').textContent = kpiData.revenue_today;
        document.getElementById('kpi-sales-today').textContent = kpiData.sales_today;
        document.getElementById('kpi-revenue-month').textContent = kpiData.revenue_this_month;
        document.getElementById('kpi-new-customers').textContent = kpiData.new_customers_this_month;
    }

    function renderMonthlySalesChart(chartData) {
        const ctx = document.getElementById('monthlySalesChart')?.getContext('2d');
        if (!ctx) {
            console.error("Could not find canvas with ID 'monthlySalesChart'");
            return;
        }
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: chartData.labels,
                datasets: [{
                    label: 'Total Revenue',
                    data: chartData.values,
                    backgroundColor: 'rgba(75, 192, 192, 0.6)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: { color: '#ccc' }
                    },
                    x: {
                        ticks: { color: '#ccc' }
                    }
                }
            }
        });
    }

    function renderTopProductsRevenueChart(chartData) {
        const ctx = document.getElementById('topProductsRevenueChart')?.getContext('2d');
        if (!ctx) {
            console.error("Could not find canvas with ID 'topProductsRevenueChart'");
            return;
        }
        const totalRevenue = parseFloat(chartData.total);

        new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: chartData.labels,
                datasets: [{
                    label: 'Revenue',
                    data: chartData.values,
                    backgroundColor: ['#d9534f', '#5bc0de', '#f0ad4e', '#5cb85c', '#6f42c1', '#343a40'],
                    borderColor: '#2b2b2b', // Match the container background for a nice effect
                    borderWidth: 2
                }]
            },
            options: {
                maintainAspectRatio: false,
                plugins: {
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const label = context.label || '';
                                const value = context.parsed;
                                const percentage = totalRevenue > 0 ? ((value / totalRevenue) * 100).toFixed(1) : 0;
                                return `${label}: $${parseFloat(value).toFixed(2)} (${percentage}%)`;
                            }
                        }
                    }
                }
            }
        });
    }

    function renderTopProductsQuantityChart(chartData) {
        const ctx = document.getElementById('topProductsQuantityChart')?.getContext('2d');
        if (!ctx) {
            console.error("Could not find canvas with ID 'topProductsQuantityChart'");
            return;
        }
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: chartData.labels,
                datasets: [{
                    label: 'Quantity Sold',
                    data: chartData.values,
                    backgroundColor: 'rgba(153, 102, 255, 0.6)',
                    borderColor: 'rgba(153, 102, 255, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                maintainAspectRatio: false,
                indexAxis: 'y',
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    x: {
                        beginAtZero: true,
                        ticks: { color: '#ccc' }
                    },
                    y: {
                        ticks: { color: '#ccc' }
                    }
                }
            }
        });
    }
});