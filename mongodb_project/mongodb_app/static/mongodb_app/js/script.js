document.addEventListener('DOMContentLoaded', () => {
    const readMoreButtons = document.querySelectorAll('.read-more-btn');
    readMoreButtons.forEach(button => {
        button.addEventListener('click', () => {
            alert('Devamını oku butonuna tıklandı!');
            // Burada haber detay sayfasına yönlendirme yapabilirsiniz
        });
    });
});