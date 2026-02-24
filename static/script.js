document.getElementById('fromCity').addEventListener('input', async function(e) {
    const city = e.target.value; 
    const response = await fetch(`http://localhost:5000/api/cities?q=${city}`);
    const cities = await response.json();
    
    const dropdown = document.getElementById('fromDropdown');
    dropdown.innerHTML = cities.map(c => 
        `<div onclick="this.parentElement.previousElementSibling.value = '${c.name}'; 
        this.parentElement.style.display = 'none'">
            ${c.name}
        </div>`
    ).join('');
    
    dropdown.style.display = 'block';
});

document.getElementById('toCity').addEventListener('input', async function(e) {
    const city = e.target.value; 
    const response = await fetch(`http://localhost:5000/api/cities?q=${city}`);
    const cities = await response.json();
    
    const dropdown = document.getElementById('toDropdown');
    dropdown.innerHTML = cities.map(c => 
        `<div onclick="this.parentElement.previousElementSibling.value = '${c.name}'; 
        this.parentElement.style.display = 'none'">
            ${c.name}
        </div>`
    ).join('');
    
    dropdown.style.display = 'block';
});
document.querySelector('.btn-swap').addEventListener('click', function() {
    const from = document.getElementById('fromCity');
    const to = document.getElementById('toCity');
    [from.value, to.value] = [to.value, from.value];
});









document.querySelector('.btn-search').addEventListener('click', async () => {
    const fromCity = document.getElementById('fromCity').value;
    const toCity = document.getElementById('toCity').value;
    const dateFrom = document.getElementById('dateFrom').value;
    const dateTo = document.getElementById('dateTo').value || dateFrom;
    
    if (!fromCity || !toCity || !dateFrom) {
        alert('Заполните все поля');
        return;
    }
    
    try {
        const params = new URLSearchParams({
            from: fromCity,
            to: toCity,
            date_start: dateFrom,
            date_end: dateTo
        });
        
        const response = await fetch(`/api/flights/search?${params}`);
        const data = await response.json();
        
        const container = document.querySelector('.overflow-auto');
        container.innerHTML = '';
        
        data.flights.forEach(flight => {
            const ticket = document.createElement('div');
            ticket.className = 'aviaticket';
            ticket.innerHTML = `
                <div class="price">
                    <h5>${Math.round(flight.price)} руб</h5>
                </div>
                <div class="route-container">
                    <div class="route">
                        <div class="route-from">
                            <h5>${flight.from.time}</h5>
                            <p>${flight.from.city}</p>
                            <p>${formatDate(flight.from.date)}</p>
                        </div>
                        <div class="route-line">
                            <div class="scr-from">${flight.from.airport}</div>
                            <div class="line-line"></div>
                            <div class="scr-to">${flight.to.airport}</div>
                        </div>
                        <div class="route-to">
                            <h5>${flight.to.time}</h5>
                            <p>${flight.to.city}</p>
                            <p>${formatDate(flight.to.date)}</p>
                        </div>
                    </div>
                </div>
            `;
            container.appendChild(ticket);
        });
        
    } catch (error) {
        console.error('Ошибка:', error);
        alert('Ошибка при поиске рейсов');
    }
});

function formatDate(dateStr) {
    const months = ['янв', 'февр', 'мар', 'апр', 'мая', 'июн', 'июл', 'авг', 'сен', 'окт', 'ноя', 'дек'];
    const date = new Date(dateStr);
    const day = date.getDate();
    const month = months[date.getMonth()];
    return `${day} ${month}`;
}