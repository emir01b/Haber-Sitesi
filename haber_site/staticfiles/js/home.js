document.addEventListener('DOMContentLoaded', function() {
    // Slider işlemleri
    const items = document.querySelectorAll('.featured-item');
    const dots = document.querySelectorAll('.dot');
    let currentIndex = 0;
    const totalItems = items.length;

    // İlk öğeyi göster
    if (items.length > 0) {
        items[0].style.display = 'flex';
        items[0].style.opacity = '1';
        dots[0].classList.add('active');
    }

    // Slider fonksiyonu
    function showSlide(index) {
        items.forEach(item => {
            item.style.display = 'none';
            item.style.opacity = '0';
        });
        dots.forEach(dot => dot.classList.remove('active'));

        items[index].style.display = 'flex';
        setTimeout(() => {
            items[index].style.opacity = '1';
        }, 10);
        dots[index].classList.add('active');
    }

    // Otomatik slider
    setInterval(() => {
        currentIndex = (currentIndex + 1) % totalItems;
        showSlide(currentIndex);
    }, 5000);

    // Dot tıklama işlemleri
    dots.forEach((dot, index) => {
        dot.addEventListener('click', () => {
            currentIndex = index;
            showSlide(currentIndex);
        });
    });

    // Kart hover efektleri
    document.querySelectorAll('.card').forEach(card => {
        card.addEventListener('mousemove', e => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            card.style.setProperty('--mouse-x', `${x}px`);
            card.style.setProperty('--mouse-y', `${y}px`);
        });
    });
}); 