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
                    borderWidth: 1,
                    hoverBackgroundColor: 'rgba(75, 192, 192, 0.8)',
                    hoverBorderColor: 'rgba(75, 192, 192, 1)',
                    hoverBorderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                interaction: {
                    intersect: false,
                    mode: 'index'
                },
                plugins: {
                    tooltip: {
                        enabled: true,
                        backgroundColor: 'rgba(43, 43, 43, 0.95)',
                        titleColor: '#79aec8',
                        bodyColor: '#fff',
                        borderColor: '#79aec8',
                        borderWidth: 1,
                        cornerRadius: 8,
                        displayColors: true,
                        padding: 12,
                        callbacks: {
                            title: function(tooltipItems) {
                                return `Month: ${tooltipItems[0].label}`;
                            },
                            label: function(context) {
                                const value = parseFloat(context.parsed.y);
                                return `Revenue: $${value.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2})}`;
                            }
                        }
                    },
                    legend: {
                        display: true,
                        labels: {
                            usePointStyle: true,
                            padding: 20,
                            color: '#ccc'
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: { 
                            color: '#ccc',
                            callback: function(value) {
                                return '$' + value.toLocaleString();
                            }
                        },
                        grid: {
                            color: 'rgba(255,255,255,0.1)'
                        }
                    },
                    x: {
                        ticks: { color: '#ccc' },
                        grid: {
                            color: 'rgba(255,255,255,0.1)'
                        }
                    }
                },
                onHover: function(event, elements) {
                    event.native.target.style.cursor = elements.length > 0 ? 'pointer' : 'default';
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
                    borderColor: '#2b2b2b',
                    borderWidth: 2,
                    hoverBackgroundColor: ['#c9302c', '#46b8da', '#eea236', '#449d44', '#5a32a3', '#23272b'],
                    hoverBorderWidth: 3
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                interaction: {
                    intersect: false
                },
                plugins: {
                    tooltip: {
                        enabled: true,
                        backgroundColor: 'rgba(43, 43, 43, 0.95)',
                        titleColor: '#79aec8',
                        bodyColor: '#fff',
                        borderColor: '#79aec8',
                        borderWidth: 1,
                        cornerRadius: 8,
                        displayColors: true,
                        padding: 12,
                        callbacks: {
                            title: function(tooltipItems) {
                                return `Product: ${tooltipItems[0].label}`;
                            },
                            label: function(context) {
                                const label = context.label || '';
                                const value = parseFloat(context.parsed);
                                const percentage = totalRevenue > 0 ? ((value / totalRevenue) * 100).toFixed(1) : 0;
                                return `Revenue: $${value.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2})} (${percentage}%)`;
                            },
                            afterLabel: function(context) {
                                const value = parseFloat(context.parsed);
                                const percentage = totalRevenue > 0 ? ((value / totalRevenue) * 100).toFixed(1) : 0;
                                return `Share: ${percentage}% of total revenue`;
                            }
                        }
                    },
                    legend: {
                        display: true,
                        position: 'bottom',
                        labels: {
                            usePointStyle: true,
                            padding: 15,
                            color: '#ccc',
                            font: {
                                size: 11
                            }
                        }
                    }
                },
                onHover: function(event, elements) {
                    event.native.target.style.cursor = elements.length > 0 ? 'pointer' : 'default';
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
                    borderWidth: 1,
                    hoverBackgroundColor: 'rgba(153, 102, 255, 0.8)',
                    hoverBorderColor: 'rgba(153, 102, 255, 1)',
                    hoverBorderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                indexAxis: 'y',
                interaction: {
                    intersect: false,
                    mode: 'index'
                },
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        enabled: true,
                        backgroundColor: 'rgba(43, 43, 43, 0.95)',
                        titleColor: '#79aec8',
                        bodyColor: '#fff',
                        borderColor: '#79aec8',
                        borderWidth: 1,
                        cornerRadius: 8,
                        displayColors: true,
                        padding: 12,
                        callbacks: {
                            title: function(tooltipItems) {
                                return `Product: ${tooltipItems[0].label}`;
                            },
                            label: function(context) {
                                const value = context.parsed.x;
                                return `Quantity Sold: ${value.toLocaleString()} units`;
                            },
                            afterLabel: function(context) {
                                const totalQuantity = chartData.values.reduce((sum, val) => sum + val, 0);
                                const value = context.parsed.x;
                                const percentage = totalQuantity > 0 ? ((value / totalQuantity) * 100).toFixed(1) : 0;
                                return `Share: ${percentage}% of top 5 products`;
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        beginAtZero: true,
                        ticks: { 
                            color: '#ccc',
                            callback: function(value) {
                                return value.toLocaleString();
                            }
                        },
                        grid: {
                            color: 'rgba(255,255,255,0.1)'
                        }
                    },
                    y: {
                        ticks: { 
                            color: '#ccc',
                            maxRotation: 0,
                            font: {
                                size: 10
                            }
                        },
                        grid: {
                            color: 'rgba(255,255,255,0.1)'
                        }
                    }
                },
                onHover: function(event, elements) {
                    event.native.target.style.cursor = elements.length > 0 ? 'pointer' : 'default';
                }
            }
        });
    }
});