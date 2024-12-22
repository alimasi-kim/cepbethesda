// Animation de la citation au scroll
document.addEventListener('DOMContentLoaded', function() {
    const quote = document.querySelector('.bible-quote');
    
    function checkScroll() {
        const quoteTop = quote.getBoundingClientRect().top;
        const windowHeight = window.innerHeight;
        
        if (quoteTop < windowHeight * 0.75) {
            quote.classList.add('visible');
            window.removeEventListener('scroll', checkScroll);
        }
    }
    
    window.addEventListener('scroll', checkScroll);
    checkScroll(); // Vérifier au chargement initial
}); 

// Effet de scroll pour le header
document.addEventListener('DOMContentLoaded', function() {
    const header = document.querySelector('.header-modern');
    const navbar = header.querySelector('.navbar');
    
    function checkScroll() {
        if (window.scrollY > 100) {
            header.classList.add('scrolled');
            navbar.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
            navbar.classList.remove('scrolled');
        }
    }
    
    window.addEventListener('scroll', checkScroll);
    checkScroll(); // Vérifier au chargement initial
}); 