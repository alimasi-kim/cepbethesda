function createParticle() {
    const particles = document.querySelector('.particles');
    const particle = document.createElement('div');
    particle.className = 'particle';
    
    // Position aléatoire
    const x = Math.random() * 100;
    const size = Math.random() * 3 + 1;
    
    particle.style.left = x + 'vw';
    particle.style.width = size + 'px';
    particle.style.height = size + 'px';
    
    particles.appendChild(particle);
    
    // Supprimer la particule après l'animation
    setTimeout(() => {
        particle.remove();
    }, 20000);
}

// Créer des particules à intervalles réguliers
setInterval(createParticle, 500); 