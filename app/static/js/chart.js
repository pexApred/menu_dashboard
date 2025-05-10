document.addEventListener("DOMContentLoaded", () => {
    const groupFilter = document.getElementById('groupFilter');
    const includeOpenCheckbox = document.getElementById('includeOpenCheckbox');
    const selectAllBtn = document.getElementById('selectAllBtn');
    const clearAllBtn = document.getElementById('clearAllBtn');

    let allMenuData = [];

    const populateGroupFilter = (data) => {
        const uniqueGroups = [...new Set(data.map(item => item.group))];
        groupFilter.innerHTML = ''; // Clear existing options
        uniqueGroups.forEach(group => {
            const option = document.createElement('option');
            option.value = group;
            option.textContent = group;
            option.selected = true; // Select all by default
            groupFilter.appendChild(option);
        });
    };

    const fetchAndRenderChart = async () => {
        const selectedGroups = Array.from(groupFilter.selectedOptions).map(option => option.value);
        const includeOpen = includeOpenCheckbox.checked;

        const queryParams = new URLSearchParams();
        selectedGroups.forEach(group => queryParams.append('group', group));
        queryParams.append('include_open', includeOpen);

        const response = await fetch(`/api/menu-performance?${queryParams.toString()}`);
        const data = await response.json();

        renderChart(data);
        populateTable(data);
    };
    const renderChart = (data) => {
        const colors = {
            Star: 'rgba(75, 192, 192, 0.8)',
            Workhorse: 'rgba(255, 206, 86, 0.8)',
            Puzzle: 'rgba(153, 102, 255, 0.8)',
            Dog: 'rgba(255, 99, 132, 0.8)'
        };

        const quadrantCounts = {
            Star: 0,
            Workhorse: 0,
            Puzzle: 0,
            Dog: 0
        };

        const groupedData = {
            Star: [],
            Workhorse: [],
            Puzzle: [],
            Dog: []
        };
        // console.log(data);
        data.forEach(item => {
            // console.log(item.item_name, item.quadrant);
            if (item.quadrant && groupedData[item.quadrant]) {
                groupedData[item.quadrant]?.push({
                    x: item.avg_price,
                    y: item.qty_sold,
                    label: item.item_name
                });
                quadrantCounts[item.quadrant]++;
            }
        });
        // console.log('Grouped Data', groupedData);
        const chartData = {
            datasets: Object.entries(groupedData).map(([quadrant, items]) => ({
                label: quadrant.charAt(0).toUpperCase() + quadrant.slice(1),
                data: items,
                backgroundColor: colors[quadrant] || 'gray',
                borderWidth: 1,
                radius: 5
            }))
        };

        const ctx = document.getElementById('menuChart').getContext('2d');
        if (window.menuChartInstance) {
            window.menuChartInstance.destroy();
        }
        window.menuChartInstance = new Chart(ctx, {
            type: 'scatter',
            data: chartData,
            options: {
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        callbacks: {
                            label: ctx => {
                                const point = ctx.raw;
                                return `${point.label}: $${point.x}, ${point.y} sold`;
                            }
                        }
                    }
                },
                scales: {
                    x: { title: { display: true, text: 'Avg Price ($)' } },
                    y: { title: { display: true, text: 'Qty Sold' } }
                }
            }
        });

        // console.log('ChartData', chartData);
        // Update the stats
        document.getElementById('starItems').textContent = quadrantCounts.Star;
        document.getElementById('puzzleItems').textContent = quadrantCounts.Puzzle;
        document.getElementById('dogItems').textContent = quadrantCounts.Dog;
        document.getElementById('workhorseItems').textContent = quadrantCounts.Workhorse;
        document.getElementById('totalItems').textContent = data.length;
        document.getElementById('totalSales').textContent = data.reduce((acc, item) => acc + item.net_sales, 0).toFixed(2);
        document.getElementById('averageQtySales').textContent = (data.reduce((acc, item) => acc + item.qty_sold, 0) / data.length).toFixed(2);
        document.getElementById('averagePrice').textContent = (data.reduce((acc, item) => acc + item.avg_price, 0) / data.length).toFixed(2);
    }
    const populateTable = (data) => {
        const menuTableBody = document.getElementById('menuTableBody');
        menuTableBody.innerHTML = ''; // Clear existing rows
        data.forEach(item => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td class="border p-2">${item.group}</td>
                <td class="border p-2">${item.item_name}</td>
                <td class="border p-2">$${item.avg_price.toFixed(2)}</td>
                <td class="border p-2">${item.qty_sold}</td>
                <td class="border p-2">${item.quadrant}</td>
            `;
            menuTableBody.appendChild(row);
        });
    };
    groupFilter.addEventListener('change', fetchAndRenderChart);
    includeOpenCheckbox.addEventListener('change', fetchAndRenderChart);

    selectAllBtn.addEventListener('click', () => {
        Array.from(groupFilter.options).forEach(option => {
            option.selected = true;
        });
        fetchAndRenderChart();
    });

    clearAllBtn.addEventListener('click', () => {
        Array.from(groupFilter.options).forEach(option => {
            option.selected = false;
        });
        fetchAndRenderChart();
    });

    // On initial load: get all data, populate filter, and render chart
    (async () => {
        const includeOpen = includeOpenCheckbox.checked;
        const queryParams = new URLSearchParams();
        queryParams.append('include_open', includeOpen);

        const response = await fetch(`/api/menu-performance?${queryParams.toString()}`);
        allMenuData = await response.json();
        populateGroupFilter(allMenuData);
        setTimeout(fetchAndRenderChart, 0); // applies all groups initially
    })();
});