document.addEventListener("DOMContentLoaded", async () => {
    const response = await fetch("/api/menu-performance");
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

    document.getElementById('starItems').textContent = quadrantCounts.star;
    document.getElementById('puzzleItems').textContent = quadrantCounts.puzzle;
    document.getElementById('dogItems').textContent = quadrantCounts.dog;
    document.getElementById('workhorseItems').textContent = quadrantCounts.workhorse;
    document.getElementById('totalItems').textContent = data.length;
    document.getElementById('totalSales').textContent = data.reduce((acc, item) => acc + item.net_sales, 0).toFixed(2);
    

    const menuTableBody = document.getElementById('menuTableBody');
    data.forEach(item => {
        const row = document.createElement('tr');
        row.innerHTML = `
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