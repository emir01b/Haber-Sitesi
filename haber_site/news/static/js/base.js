document.addEventListener('DOMContentLoaded', function() {
    const navbar = document.querySelector('.navbar');
    let lastScroll = 0;

    // Navbar scroll handling
    window.addEventListener('scroll', () => {
        const currentScroll = window.pageYOffset;
        
        if (currentScroll > 50) {
            navbar.classList.add('navbar-scrolled');
            
            if (currentScroll > lastScroll) {
                navbar.classList.remove('navbar-visible');
                navbar.classList.add('navbar-hidden');
            } 
            else if (currentScroll < lastScroll) {
                navbar.classList.remove('navbar-hidden');
                navbar.classList.add('navbar-visible');
            }
        } else {
            navbar.classList.remove('navbar-scrolled');
            navbar.classList.remove('navbar-hidden');
            navbar.classList.add('navbar-visible');
        }

        lastScroll = currentScroll;
    });

    // Weather functionality
    const citySelect = document.getElementById('citySelect');
    const weatherInfo = document.getElementById('weatherInfo');
    const api_key = "b3c53f46a07d0384f764935799a0b710";

    // Turkish cities array
    const cities = [
        "Adana", "Adıyaman", "Afyonkarahisar", "Ağrı", "Amasya", "Ankara", "Antalya", "Artvin", 
        // ... Rest of the cities ...
    ];

    // Sort and add cities to select
    cities.sort().forEach(city => {
        const option = document.createElement('option');
        option.value = city;
        option.textContent = city;
        if (city === 'Elazığ') {
            option.selected = true;
        }
        citySelect.appendChild(option);
    });

    // Get weather data function
    async function getWeather(city) {
        try {
            const url = `https://api.openweathermap.org/data/2.5/weather?q=${city},TR&appid=${api_key}&units=metric&lang=tr`;
            const response = await fetch(url);
            const data = await response.json();
            
            const temp = Math.round(data.main.temp);
            const desc = data.weather[0].description
                .split(' ')
                .map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
                .join(' ');
            
            weatherInfo.textContent = `${desc} ${temp}°C`;
        } catch (err) {
            console.error('Hava durumu alınamadı:', err);
            weatherInfo.textContent = 'Hava durumu alınamadı';
        }
    }

    // Initialize weather for Elazığ
    getWeather('Elazığ');

    // Update weather on city change
    citySelect.addEventListener('change', (e) => {
        if (e.target.value) {
            getWeather(e.target.value);
        }
    });

    // Sports page specific code
    const isSportsPage = window.location.pathname.includes('/category/spor');
    
    if (isSportsPage) {
        document.documentElement.style.setProperty('--gradient-start', '#20B30F');
        document.documentElement.style.setProperty('--gradient-end', '#2ECC71');
        document.documentElement.style.setProperty('--header-color', '#20B30F');
        document.documentElement.style.setProperty('--accent-color', '#2ECC71');
        
        document.querySelector('.navbar').classList.add('sports-nav');
        document.querySelector('footer').classList.add('sports-footer');
        document.body.classList.add('sports-page');
    }

    // Weather page functionality
    const weatherContainer = document.getElementById('weatherContent');
    const loadingIndicator = document.getElementById('loading');
    let currentPage = 1;
    const cardsPerLoad = 6;

    // Create weather card function
    function createWeatherCard(data) {
        return `
            <div class="col-lg-4 col-md-6 mb-4 weather-card" style="opacity: 0; transform: translateY(20px);">
                <div class="card h-100 shadow-sm">
                    <div class="card-body">
                        <h5 class="card-title">${data.city}</h5>
                        <p class="card-text">
                            <i class="fas ${data.icon}"></i>
                            ${data.temperature}°C
                            <br>
                            ${data.description}
                        </p>
                        <div class="d-flex justify-content-between align-items-center">
                            <small class="text-muted">${data.humidity}% Nem</small>
                            <small class="text-muted">${data.windSpeed} km/s Rüzgar</small>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    // Load weather cards function
    function loadWeatherCards(page) {
        const start = (page - 1) * cardsPerLoad;
        const end = start + cardsPerLoad;
        const cards = document.querySelectorAll('.weather-card');

        cards.forEach((card, index) => {
            if (index >= start && index < end) {
                setTimeout(() => {
                    card.style.transition = 'all 0.5s ease';
                    card.style.opacity = '1';
                    card.style.transform = 'translateY(0)';
                }, (index - start) * 200);
            }
        });

        if (end >= cards.length) {
            if (loadingIndicator) {
                loadingIndicator.style.display = 'none';
            }
        } else {
            currentPage++;
            checkScroll();
        }
    }

    // Check scroll function
    function checkScroll() {
        const scrollPosition = window.innerHeight + window.scrollY;
        const pageHeight = document.documentElement.scrollHeight;

        if (scrollPosition >= pageHeight - 1000) {
            loadWeatherCards(currentPage);
        }
    }

    // Initialize weather content
    if (weatherContainer) {
        loadWeatherCards(currentPage);
        window.addEventListener('scroll', checkScroll);
    }
});