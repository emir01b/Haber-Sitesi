document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('citySearch');
    const weatherItems = document.querySelectorAll('.weather-item');
    const noResults = document.getElementById('noResults');
    const loading = document.getElementById('loading');
    const weatherCards = document.getElementById('weatherCards');
    
    // Yükleme göstergesini göster
    loading.style.display = 'block';
    
    // Kartları yükle
    setTimeout(() => {
        loading.style.display = 'none';
        weatherCards.style.display = 'flex';
    }, 100);

    // Arama işlevi
    searchInput.addEventListener('input', function() {
        const searchTerm = this.value.toLowerCase().trim();
        let hasResults = false;

        weatherItems.forEach(item => {
            const cityName = item.dataset.city;
            if (cityName.includes(searchTerm)) {
                item.classList.remove('hidden');
                hasResults = true;
            } else {
                item.classList.add('hidden');
            }
        });

        // Sonuç bulunamadı mesajını göster/gizle
        noResults.style.display = hasResults ? 'none' : 'flex';
    });

    // Türkçe karakterleri düzeltme
    searchInput.addEventListener('keyup', function() {
        this.value = this.value
            .replace('i', 'i')
            .replace('ı', 'i')
            .replace('ğ', 'g')
            .replace('ü', 'u')
            .replace('ş', 's')
            .replace('ö', 'o')
            .replace('ç', 'c');
    });

    // Kart hover efektleri
    document.querySelectorAll('.weather-card').forEach(card => {
        card.addEventListener('mousemove', e => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            card.style.setProperty('--mouse-x', `${x}px`);
            card.style.setProperty('--mouse-y', `${y}px`);
        });
    });
}); 