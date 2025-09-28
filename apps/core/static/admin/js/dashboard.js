document.addEventListener('DOMContentLoaded', () => {
    console.log("DEBUG MODE: Dashboard script loaded.");

    // Global defaults are maintained
    Chart.defaults.color = '#ccc';
    Chart.defaults.interaction = { intersect: false, mode: 'index' };

    const dataUrl = '/api/v1/reports/dashboard-data/';

    async function initializeDashboard() {
        try {
            const response = await fetch(dataUrl);
            if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
            
            const data = await response.json();
            console.log("DEBUG MODE: Data received successfully from API.", data);

            // The function to populate KPIs was simplified to not use formatting
            // and to avoid any `getElementById` errors in case the HTML is not 100%
            document.getElementById('kpi-revenue-today').textContent = data.kpi.revenue_today;
            document.getElementById('kpi-sales-today').textContent = data.kpi.sales_today;
            document.getElementById('kpi-revenue-month').textContent = data.kpi.revenue_this_month;
            document.getElementById('kpi-new-customers').textContent = data.kpi.new_customers_this_month;
            
            console.log("DEBUG MODE: KPIs populated.");

            renderCharts(data.charts);
        } catch (error) {
            console.error("DEBUG MODE: Failed to initialize dashboard.", error);
        }
    }

    function renderCharts(chartsData) {
        // --- Chart 1: Monthly Sales ---
        const monthlyCtx = document.getElementById('monthlySalesChart')?.getContext('2d');
        if (monthlyCtx) {
            new Chart(monthlyCtx, {
                type: 'bar',
                data: {
                    labels: chartsData.monthly_sales.labels,
                    datasets: [{
                        label: 'Total Revenue',
                        data: chartsData.monthly_sales.values,
                        backgroundColor: 'rgba(75, 192, 192, 0.6)',
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            display: true,
                            position: 'top',
                            labels: {
                                color: '#ccc',
                                padding: 15,
                                font: {
                                    size: 12
                                }
                            }
                        }
                    },
                    scales: {
                        x: {
                            ticks: {
                                maxRotation: 45,
                                minRotation: 0,
                                padding: 10,
                                font: {
                                    size: 11
                                }
                            },
                            grid: {
                                display: false
                            }
                        },
                        y: {
                            beginAtZero: true,
                            ticks: {
                                padding: 10,
                                font: {
                                    size: 11
                                }
                            },
                            grid: {
                                color: 'rgba(255, 255, 255, 0.1)'
                            }
                        }
                    },
                    layout: {
                        padding: {
                            left: 10,
                            right: 10,
                            top: 10,
                            bottom: 20
                        }
                    }
                }
            });
            console.log("DEBUG MODE: Monthly Sales Chart rendered.");
        }

        // --- Chart 2: Revenue by Product ---
        const revenueCtx = document.getElementById('topProductsRevenueChart')?.getContext('2d');
        if (revenueCtx) {
            new Chart(revenueCtx, {
                type: 'doughnut',
                data: {
                    labels: chartsData.top_products_revenue.labels,
                    datasets: [{
                        label: 'Revenue',
                        data: chartsData.top_products_revenue.values,
                        backgroundColor: ['#d9534f', '#5bc0de', '#f0ad4e', '#5cb85c', '#6f42c1', '#343a40'],
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'right',
                            labels: {
                                color: '#ccc',
                                padding: 15,
                                font: {
                                    size: 11
                                },
                                boxWidth: 12,
                                generateLabels: function(chart) {
                                    const data = chart.data;
                                    if (data.labels.length && data.datasets.length) {
                                        return data.labels.map((label, i) => {
                                            const value = data.datasets[0].data[i];
                                            return {
                                                text: label,
                                                fillStyle: data.datasets[0].backgroundColor[i],
                                                fontColor: '#ccc',
                                                hidden: false,
                                                index: i
                                            };
                                        });
                                    }
                                    return [];
                                }
                            }
                        }
                    },
                    layout: {
                        padding: {
                            left: 10,
                            right: 10,
                            top: 10,
                            bottom: 10
                        }
                    }
                }
            });
            console.log("DEBUG MODE: Top Products by Revenue Chart rendered.");
        }

        // --- Chart 3: Quantity by Product ---
        const quantityCtx = document.getElementById('topProductsQuantityChart')?.getContext('2d');
        if (quantityCtx) {
            new Chart(quantityCtx, {
                type: 'bar',
                data: {
                    labels: chartsData.top_products_quantity.labels,
                    datasets: [{
                        label: 'Quantity Sold',
                        data: chartsData.top_products_quantity.values,
                        backgroundColor: 'rgba(153, 102, 255, 0.6)',
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    indexAxis: 'y',
                    plugins: {
                        legend: {
                            display: true,
                            position: 'top',
                            labels: {
                                color: '#ccc',
                                padding: 15,
                                font: {
                                    size: 12
                                }
                            }
                        }
                    },
                    scales: {
                        x: {
                            beginAtZero: true,
                            ticks: {
                                padding: 10,
                                font: {
                                    size: 11
                                }
                            },
                            grid: {
                                color: 'rgba(255, 255, 255, 0.1)'
                            }
                        },
                        y: {
                            ticks: {
                                padding: 10,
                                font: {
                                    size: 11
                                },
                                maxRotation: 0,
                                minRotation: 0
                            },
                            grid: {
                                display: false
                            }
                        }
                    },
                    layout: {
                        padding: {
                            left: 10,
                            right: 10,
                            top: 10,
                            bottom: 20
                        }
                    }
                }
            });
            console.log("DEBUG MODE: Top Products by Quantity Chart rendered.");
        }
    }

    initializeDashboard();
});