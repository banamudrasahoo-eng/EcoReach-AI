/**
 * EcoReach AI - Sustainability Dashboard Visualization Script
 * Uses Chart.js to render campus demo metrics.
 */

document.addEventListener('DOMContentLoaded', () => {
    // Check if Chart.js is loaded
    if (typeof Chart === 'undefined') {
        console.warn('Chart.js CDN not loaded.');
        return;
    }

    // Chart 1: Weekly Electricity Consumption (Bar Chart)
    const ctxElectricity = document.getElementById('electricityChart');
    if (ctxElectricity) {
        new Chart(ctxElectricity, {
            type: 'bar',
            data: {
                labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                datasets: [{
                    label: 'Academic Blocks (kWh)',
                    data: [1200, 1350, 1280, 1420, 1390, 850, 780],
                    backgroundColor: '#2d6a4f',
                    borderRadius: 6
                }, {
                    label: 'Hostel Blocks (kWh)',
                    data: [950, 980, 960, 990, 1020, 1150, 1100],
                    backgroundColor: '#52b788',
                    borderRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { position: 'top' },
                    title: { display: false }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        title: { display: true, text: 'Energy (kWh)' }
                    }
                }
            }
        });
    }

    // Chart 2: Water Usage Distribution by Campus Zone (Doughnut Chart)
    const ctxWater = document.getElementById('waterChart');
    if (ctxWater) {
        new Chart(ctxWater, {
            type: 'doughnut',
            data: {
                labels: ['Hostels & Residential', 'Mess & Canteen', 'Labs & Classrooms', 'Grounds & Irrigation'],
                datasets: [{
                    data: [45, 25, 18, 12],
                    backgroundColor: [
                        '#0288d1',
                        '#26c6da',
                        '#80deea',
                        '#484848'
                    ],
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { position: 'bottom' }
                }
            }
        });
    }

    // Chart 3: Waste Segregation Breakdown (Pie / Horizontal Bar Chart)
    const ctxWaste = document.getElementById('wasteChart');
    if (ctxWaste) {
        new Chart(ctxWaste, {
            type: 'pie',
            data: {
                labels: ['Organic / Compostable', 'Recyclable Plastic & Metal', 'Paper & Cardboard', 'E-Waste & Hazardous', 'Non-Recyclable Landfill'],
                datasets: [{
                    data: [42, 28, 16, 4, 10],
                    backgroundColor: [
                        '#4CAF50',
                        '#2196F3',
                        '#FF9800',
                        '#E91E63',
                        '#9E9E9E'
                    ],
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { position: 'bottom' }
                }
            }
        });
    }
});
