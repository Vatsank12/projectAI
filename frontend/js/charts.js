let performanceChart = null;
let networkChart = null;
let cpuTrendChart = null;
let memoryTrendChart = null;

function initializeCharts() {
    const perfCtx = document.getElementById('performanceChart');
    const netCtx = document.getElementById('networkChart');
    const cpuTrendCtx = document.getElementById('cpuTrendChart');
    const memTrendCtx = document.getElementById('memoryTrendChart');
    
    if (!perfCtx || !netCtx) return;
    
    performanceChart = new Chart(perfCtx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [
                {
                    label: 'CPU Usage (%)',
                    data: [],
                    borderColor: '#06b6d4',
                    backgroundColor: 'rgba(6, 182, 212, 0.1)',
                    borderWidth: 2,
                    tension: 0.4,
                    fill: true,
                    pointRadius: 2,
                    pointBackgroundColor: '#06b6d4',
                    pointBorderColor: '#06b6d4'
                },
                {
                    label: 'Memory Usage (%)',
                    data: [],
                    borderColor: '#a855f7',
                    backgroundColor: 'rgba(168, 85, 247, 0.1)',
                    borderWidth: 2,
                    tension: 0.4,
                    fill: true,
                    pointRadius: 2,
                    pointBackgroundColor: '#a855f7',
                    pointBorderColor: '#a855f7'
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    labels: {
                        color: '#cbd5e1',
                        font: {
                            size: 12
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,
                    grid: {
                        color: 'rgba(6, 182, 212, 0.1)'
                    },
                    ticks: {
                        color: '#94a3b8'
                    }
                },
                x: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        color: '#94a3b8'
                    }
                }
            }
        }
    });
    
    networkChart = new Chart(netCtx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [
                {
                    label: 'Upload (MB)',
                    data: [],
                    borderColor: '#10b981',
                    backgroundColor: 'rgba(16, 185, 129, 0.1)',
                    borderWidth: 2,
                    tension: 0.4,
                    fill: true,
                    pointRadius: 2,
                    pointBackgroundColor: '#10b981',
                    pointBorderColor: '#10b981'
                },
                {
                    label: 'Download (MB)',
                    data: [],
                    borderColor: '#f59e0b',
                    backgroundColor: 'rgba(245, 158, 11, 0.1)',
                    borderWidth: 2,
                    tension: 0.4,
                    fill: true,
                    pointRadius: 2,
                    pointBackgroundColor: '#f59e0b',
                    pointBorderColor: '#f59e0b'
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    labels: {
                        color: '#cbd5e1',
                        font: {
                            size: 12
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(6, 182, 212, 0.1)'
                    },
                    ticks: {
                        color: '#94a3b8'
                    }
                },
                x: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        color: '#94a3b8'
                    }
                }
            }
        }
    });

    if (cpuTrendCtx) {
        cpuTrendChart = new Chart(cpuTrendCtx, {
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    label: 'CPU Usage (%)',
                    data: [],
                    borderColor: '#06b6d4',
                    backgroundColor: 'rgba(6, 182, 212, 0.1)',
                    borderWidth: 2,
                    tension: 0.4,
                    fill: true,
                    pointRadius: 3,
                    pointBackgroundColor: '#06b6d4'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        labels: { color: '#cbd5e1' }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100,
                        grid: { color: 'rgba(6, 182, 212, 0.1)' },
                        ticks: { color: '#94a3b8' }
                    },
                    x: {
                        grid: { display: false },
                        ticks: { color: '#94a3b8' }
                    }
                }
            }
        });
    }

    if (memTrendCtx) {
        memoryTrendChart = new Chart(memTrendCtx, {
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    label: 'Memory Usage (%)',
                    data: [],
                    borderColor: '#a855f7',
                    backgroundColor: 'rgba(168, 85, 247, 0.1)',
                    borderWidth: 2,
                    tension: 0.4,
                    fill: true,
                    pointRadius: 3,
                    pointBackgroundColor: '#a855f7'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        labels: { color: '#cbd5e1' }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100,
                        grid: { color: 'rgba(6, 182, 212, 0.1)' },
                        ticks: { color: '#94a3b8' }
                    },
                    x: {
                        grid: { display: false },
                        ticks: { color: '#94a3b8' }
                    }
                }
            }
        });
    }
}

function updateCharts() {
    if (!performanceChart || !metricsData.cpu.length) return;
    
    const maxDataPoints = 30;
    const startIdx = Math.max(0, metricsData.cpu.length - maxDataPoints);
    
    const labels = metricsData.timestamps.slice(startIdx).map((t, i) => {
        return i % 5 === 0 ? t : '';
    });
    
    performanceChart.data.labels = labels;
    performanceChart.data.datasets[0].data = metricsData.cpu.slice(startIdx);
    performanceChart.data.datasets[1].data = metricsData.memory.slice(startIdx);
    performanceChart.update('none');
    
    if (cpuTrendChart) {
        cpuTrendChart.data.labels = labels;
        cpuTrendChart.data.datasets[0].data = metricsData.cpu.slice(startIdx);
        cpuTrendChart.update('none');
    }
    
    if (memoryTrendChart) {
        memoryTrendChart.data.labels = labels;
        memoryTrendChart.data.datasets[0].data = metricsData.memory.slice(startIdx);
        memoryTrendChart.update('none');
    }
    
    if (currentMetrics.network) {
        if (!networkChart.data.datasets[0].data) {
            networkChart.data.datasets[0].data = [];
        }
        if (!networkChart.data.datasets[1].data) {
            networkChart.data.datasets[1].data = [];
        }
        
        networkChart.data.labels = labels;
        networkChart.data.datasets[0].data.push(currentMetrics.network.bytes_sent);
        networkChart.data.datasets[1].data.push(currentMetrics.network.bytes_recv);
        
        if (networkChart.data.datasets[0].data.length > maxDataPoints) {
            networkChart.data.datasets[0].data.shift();
            networkChart.data.datasets[1].data.shift();
        }
        
        networkChart.update('none');
    }
}

window.addEventListener('load', () => {
    setTimeout(initializeCharts, 100);
});
