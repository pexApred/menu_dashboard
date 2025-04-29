document.addEventListener("DOMContentLoaded", async () => {
    const response = await fetch("/menu-performance");
    const data = await response.json();

    const colors = {
        star: 'rgba(75, 192, 192, 0.8)',
        workhorse: 'rgba(255, 206, 86, 0.8)',
        puzzle: 'rgba(153, 102, 255, 0.8)',
        dog: 'rgba(255, 99, 132, 0.8)'
    };

    const quadrantCounts = {
        star: 0,
        workhorse: 0,
        puzzle: 0,
        dog: 0
    }

    const chartData = {
        datasets: data.map(item => {
            quadrantCounts[item.quadrant] = (quadrantCounts[item.quadrant] || 0) + 1;
            return {
                label: item.item_name,
                data: [{ x: item.avg_price, y: item.qty_sold }],
                backgroundColor: colors[item.quadrant] || 'gray',
                borderWidth: 1,
                radius: 5,
            };
        })
    };

    const menuTableBody = document.getElementById('menuTableBody');
    Object.entries(quadrantCounts).forEach(([quadrant, count]) => {
        const row = document.createElement('tr');
        row.innerHTML = `<td>${quadrant}</td><td>${count}</td>`;
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
                        label: ctx => `${ctx.raw.x} USD, ${ctx.raw.y} sold`
                    }
                }
            },
            scales: {
                x: { title: { display: true, text: 'Avg Price ($' } },
                y: { title: { display: true, text: 'Qty Sold' } }
            }
        }
    });
});