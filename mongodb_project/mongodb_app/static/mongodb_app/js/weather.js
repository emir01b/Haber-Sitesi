document.addEventListener('DOMContentLoaded', function() {
    const map = document.getElementById('turkey-map');
    const selectedCityWeather = document.getElementById('selected-city-weather');
    const API_KEY = "b3c53f46a07d0384f764935799a0b710"; // Önceki koddan alınan API key

    // Her şehir için path elementlerine event listener ekle
    map.querySelectorAll('path').forEach(path => {
        path.addEventListener('click', async function() {
            const cityName = this.getAttribute('title');
            
            // Tıklanan şehri vurgula
            map.querySelectorAll('path').forEach(p => p.style.fill = '#e0e0e0');
            this.style.fill = '#2193b0';

            try {
                // Hava durumu verisini al
                const response = await fetch(
                    `https://api.openweathermap.org/data/2.5/weather?q=${cityName},TR&appid=${API_KEY}&units=metric&lang=tr`
                );
                const data = await response.json();

                // Hava durumu kartını oluştur
                selectedCityWeather.innerHTML = `
                    <div class="weather-card">
                        <h2>${cityName}</h2>
                        <div class="weather-info">
                            <img src="https://openweathermap.org/img/wn/${data.weather[0].icon}@2x.png" 
                                 alt="${data.weather[0].description}">
                            <div class="temperature">${Math.round(data.main.temp)}°C</div>
                            <div class="description">${data.weather[0].description}</div>
                            <div class="weather-details">
                                <div class="detail">
                                    <i class="fas fa-tint"></i>
                                    <span>Nem: ${data.main.humidity}%</span>
                                </div>
                                <div class="detail">
                                    <i class="fas fa-wind"></i>
                                    <span>Rüzgar: ${Math.round(data.wind.speed)} km/s</span>
                                </div>
                            </div>
                        </div>
                    </div>
                `;
            } catch (error) {
                console.error('Hava durumu alınamadı:', error);
                selectedCityWeather.innerHTML = `
                    <div class="weather-card error">
                        <h2>Hata</h2>
                        <p>Hava durumu bilgisi alınamadı.</p>
                    </div>
                `;
            }
        });
    });

    // Şehir arama fonksiyonalitesi
    const citySearchInput = document.getElementById('citySearchInput');
    const searchCityBtn = document.getElementById('searchCityBtn');

    function searchCity() {
        const searchTerm = citySearchInput.value.toLowerCase();
        map.querySelectorAll('path').forEach(path => {
            const cityName = path.getAttribute('title').toLowerCase();
            if (cityName === searchTerm) {
                path.dispatchEvent(new Event('click'));
                citySearchInput.value = '';
            }
        });
    }

    searchCityBtn.addEventListener('click', searchCity);
    citySearchInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            searchCity();
        }
    });
});