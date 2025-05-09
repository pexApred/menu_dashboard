document.addEventListener("DOMContentLoaded", async () => {
    const response = await fetch("/api/menu-performance");
    const data = await response.json();

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
    }

    const groupedData = {
        Star: [],
        Workhorse: [],
        Puzzle: [],
        Dog: []
    };
    console.log(data);
    data.forEach(item => {
        console.log(item.item_name, item.quadrant);
        if (item.quadrant && groupedData[item.quadrant]) {
            groupedData[item.quadrant]?.push({
                x: item.avg_price,
                y: item.qty_sold,
                label: item.item_name
            });
            quadrantCounts[item.quadrant]++;
        }
    });
    console.log('Grouped Data', groupedData);
    const chartData = {
        datasets: Object.entries(groupedData).map(([quadrant, items]) => ({
            label: quadrant.charAt(0).toUpperCase() + quadrant.slice(1),
            data: items,
            backgroundColor: colors[quadrant] || 'gray',
            borderWidth: 1,
            radius: 5
        }))
        
    };
    console.log('ChartData', chartData);
    document.getElementById('starItems').textContent = quadrantCounts.Star;
    document.getElementById('puzzleItems').textContent = quadrantCounts.Puzzle;
    document.getElementById('dogItems').textContent = quadrantCounts.Dog;
    document.getElementById('workhorseItems').textContent = quadrantCounts.Workhorse;
    document.getElementById('totalItems').textContent = data.length;
    document.getElementById('totalSales').textContent = data.reduce((acc, item) => acc + item.net_sales, 0).toFixed(2);


    const menuTableBody = document.getElementById('menuTableBody');
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

    const ctx = document.getElementById('menuChart').getContext('2d');
    new Chart(ctx, {
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
    console.log(chartData);
});