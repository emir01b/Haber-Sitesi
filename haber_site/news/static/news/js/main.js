document.addEventListener('DOMContentLoaded', function() {
    // Sayfa yüklenme animasyonu
    document.body.classList.add('loaded');

    // Haber kartları için lazy loading
    const newsCards = document.querySelectorAll('.card');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1
    });

    newsCards.forEach((card, index) => {
        card.style.setProperty('--animation-order', index);
        observer.observe(card);
    });

    // Tarih formatlaması
    const dateElements = document.querySelectorAll('.text-muted');
    dateElements.forEach(element => {
        const date = new Date(element.textContent);
        element.textContent = date.toLocaleDateString('tr-TR', {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    });

    // Header scroll efekti
    let lastScroll = 0;
    const navbar = document.querySelector('.navbar');
    const scrollThreshold = 50;
    let scrollTimer = null;

    window.addEventListener('scroll', () => {
        const currentScroll = window.pageYOffset;
        
        if (scrollTimer !== null) {
            clearTimeout(scrollTimer);
        }

        if (currentScroll > scrollThreshold) {
            // Aşağı scroll
            if (currentScroll > lastScroll) {
                navbar.classList.remove('navbar-visible');
                navbar.classList.add('navbar-hidden');
            } 
            // Yukarı scroll
            else {
                navbar.classList.remove('navbar-hidden');
                navbar.classList.add('navbar-visible');
            }
            navbar.classList.add('navbar-scrolled');
        } else {
            navbar.classList.remove('navbar-scrolled');
            navbar.classList.remove('navbar-hidden');
            navbar.classList.add('navbar-visible');
        }

        // Scroll durduğunda son kontrol
        scrollTimer = setTimeout(() => {
            if (currentScroll < lastScroll) {
                navbar.classList.remove('navbar-hidden');
                navbar.classList.add('navbar-visible');
            }
        }, 100);

        lastScroll = currentScroll;
    });

    // Sayfa yüklendiğinde navbar'ı göster
    navbar.classList.add('navbar-visible');
});
