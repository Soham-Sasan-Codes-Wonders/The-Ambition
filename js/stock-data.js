document.addEventListener('DOMContentLoaded', () => {
    const stockSymbols = {
        'dow-jones': { symbol: 'DIA', name: 'DOW Jones (DIA)' },        
        'sp-500': { symbol: 'SPY', name: 'S&P 500 (SPY)' },          
        'nasdaq': { symbol: 'QQQ', name: 'NASDAQ 100 (QQQ)' },      
    };

    const stockDataContainer = document.getElementById('stock-market-data-content');

    if (!stockDataContainer) {
        console.error('Stock market data container not found.');
        return;
    }
    stockDataContainer.innerHTML = '';
    const selectedKeys = ['dow-jones', 'sp-500', 'nasdaq'];
    const chartInstances = {};

    selectedKeys.forEach(key => {
        const stockInfo = stockSymbols[key];
        if (!stockInfo) return;

        const chartWrapper = document.createElement('div');
        chartWrapper.style.marginBottom = '30px';

        const title = document.createElement('h3');
        title.textContent = stockInfo.name;
        title.style.color = 'white';
        title.style.fontFamily = 'Arial, sans-serif';
        title.style.marginBottom = '8px';

        const canvas = document.createElement('canvas');
        canvas.id = `marketChart-${key}`;
        canvas.style.width = '300px';
        canvas.style.height = '160px';

        chartWrapper.appendChild(title);
        chartWrapper.appendChild(canvas);
        stockDataContainer.appendChild(chartWrapper);

        const ctx = canvas.getContext('2d');

        chartInstances[key] = new Chart(ctx, {
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    label: 'Monthly Closing Prices',
                    data: [],
                    fill: false,
                    borderColor: 'green',
                    backgroundColor: 'green',
                    pointRadius: 3,
                    pointHoverRadius: 6,
                    tension: 0.2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        labels: {
                            color: 'white'
                        }
                    },
                    background: {
                        color: 'black'
                    }
                },
                scales: {
                    x: {
                        ticks: { color: 'white' },
                        grid: {
                            color: '#333'
                        }
                    },
                    y: {
                        beginAtZero: false,
                        ticks: { color: 'white' },
                        grid: {
                            color: '#333'
                        }
                    }
                },
                layout: {
                    padding: 8
                }
            }
        });
    });

    async function fetchStockData(symbol) {
        const url = `https://ambition-proxy-server.onrender.com/api/stock?symbol=${symbol}`;
        try {
            const response = await fetch(url);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status} for ${symbol}`);
            }
            const data = await response.json();
            console.log(`Raw API response for ${symbol}:`, JSON.stringify(data, null, 2));

            if (data && data.status === "ok" && Array.isArray(data.values)) {
                const reversed = data.values.slice().reverse(); // oldest to newest
                const dates = reversed.map(entry => entry.datetime);
                const closingPrices = reversed.map(entry => parseFloat(entry.close));
                return { dates, closingPrices };
            } else if (data.code || data.message) {
                return { error: data.message || "API returned an error." };
            } else {
                return { error: 'Unexpected API response format.' };
            }
        } catch (error) {
            console.error(`Error fetching data for ${symbol}:`, error);
            return { error: error.message };
        }
    }

    function sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    async function updateAllStocks() {
        console.log("Fetching stock data...");
        for (let i = 0; i < selectedKeys.length; i++) {
            const key = selectedKeys[i];
            const stockInfo = stockSymbols[key];
            if (!stockInfo) continue;

            console.log(`Fetching historical data for ${stockInfo.name} (${stockInfo.symbol})...`);
            const data = await fetchStockData(stockInfo.symbol);

            if (data && !data.error) {
                const { dates, closingPrices } = data;

                const overallColor = closingPrices[closingPrices.length - 1] >= closingPrices[0] ? 'limegreen' : 'red';

                const chart = chartInstances[key];
                if (chart) {
                    chart.data.labels = dates;
                    chart.data.datasets[0].data = closingPrices;
                    chart.data.datasets[0].borderColor = overallColor;
                    chart.data.datasets[0].backgroundColor = overallColor;
                    chart.update();
                }
            } else if (data && data.error) {
                console.warn(`Error fetching historical data for ${stockInfo.name}: ${data.note ? data.note : data.error}`);
            } else {
                console.warn(`No data returned for ${stockInfo.name}`);
            }

            if (i < selectedKeys.length - 1) {
                await sleep(15000);
            }
        }
        const cacheData = {};
        selectedKeys.forEach(key => {
            const chart = chartInstances[key];
            if (chart) {
                cacheData[key] = {
                    dates: chart.data.labels,
                    closingPrices: chart.data.datasets[0].data
                };
            }
        });
        sessionStorage.setItem('etfChartData', JSON.stringify({
            timestamp: Date.now(),
            data: cacheData
        }));
    }

    const cache = sessionStorage.getItem('etfChartData');
    if (cache) {
        const parsed = JSON.parse(cache);
        const maxAge = 10 * 60 * 1000; // 10 minutes
        if (Date.now() - parsed.timestamp < maxAge) {
            console.log("Loading ETF data from session cache...");
            Object.entries(parsed.data).forEach(([key, { dates, closingPrices }]) => {
                const overallColor = closingPrices[closingPrices.length - 1] >= closingPrices[0] ? 'limegreen' : 'red';
                const chart = chartInstances[key];
                if (chart) {
                    chart.data.labels = dates;
                    chart.data.datasets[0].data = closingPrices;
                    chart.data.datasets[0].borderColor = overallColor;
                    chart.data.datasets[0].backgroundColor = overallColor;
                    chart.update();
                }
            });
            return;
        }
    }
    updateAllStocks();
    setInterval(updateAllStocks, 5 * 60 * 1000);
});