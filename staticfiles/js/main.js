/**
 * AUDE - Main JavaScript File
 * Gère les fonctionnalités communes à toutes les pages
 */

// ============================================
// GESTION DU THÈME (LIGHT/DARK MODE)
// ============================================
function getTheme() {
    return localStorage.getItem('aude-theme') || 'light';
}

function setTheme(theme) {
    localStorage.setItem('aude-theme', theme);
    document.documentElement.setAttribute('data-theme', theme);
    updateThemeIcons(theme);
}

function updateThemeIcons(theme) {
    const lightIcon = document.getElementById('light-icon');
    const darkIcon = document.getElementById('dark-icon');
    
    if (!lightIcon || !darkIcon) return;
    
    if (theme === 'dark') {
        lightIcon.style.display = 'none';
        darkIcon.style.display = 'inline-block';
    } else {
        lightIcon.style.display = 'inline-block';
        darkIcon.style.display = 'none';
    }
}

function toggleTheme() {
    const currentTheme = getTheme();
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';
    setTheme(newTheme);
}

// ============================================
// NAVIGATION ET SCROLL
// ============================================
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if (href.length > 1 && document.querySelector(href)) {
                e.preventDefault();
                
                // Animation de clic
                this.classList.add('clicking');
                setTimeout(() => {
                    this.classList.remove('clicking');
                }, 600);
                
                const target = document.querySelector(href);
                const navbar = document.querySelector('.navbar');
                const navbarHeight = navbar ? navbar.offsetHeight : 0;
                const targetPosition = target.offsetTop - navbarHeight - 20;
                
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
                
                // Fermer le menu mobile si ouvert
                const navbarCollapse = document.getElementById('navbarNav');
                if (navbarCollapse && navbarCollapse.classList.contains('show')) {
                    const bsCollapse = bootstrap.Collapse.getInstance(navbarCollapse);
                    if (bsCollapse) bsCollapse.hide();
                }
            }
        });
    });
}

function initNavbarScroll() {
    const navbar = document.querySelector('.navbar');
    if (!navbar) return;
    
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });
}

function updateActiveNavLink() {
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    
    if (sections.length === 0) return;
    
    let index = sections.length;
    while(--index && window.scrollY + 150 < sections[index].offsetTop) {}
    
    navLinks.forEach(link => link.classList.remove('active'));
    if (navLinks[index] && sections[index]) {
        const currentPage = window.location.pathname.split('/').pop() || 'index.html';
        const activeLink = document.querySelector(`.navbar-nav .nav-link[href="${currentPage}#${sections[index].id}"]`) ||
                          document.querySelector(`.navbar-nav .nav-link[href="#${sections[index].id}"]`);
        if (activeLink) activeLink.classList.add('active');
    } else if (window.scrollY < sections[0].offsetTop - 100) {
        const homeLink = document.querySelector('.navbar-nav .nav-link[href="index.html"]');
        if (homeLink) homeLink.classList.add('active');
    }
}

// ============================================
// ANIMATIONS ET EFFETS VISUELS
// ============================================
function initScrollReveal() {
    const scrollRevealElements = document.querySelectorAll('.scroll-reveal');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('active');
                observer.unobserve(entry.target);
            }
        });
    }, { 
        threshold: 0.1, 
        rootMargin: '0px 0px -50px 0px' 
    });
    
    scrollRevealElements.forEach(el => observer.observe(el));
}

function initCounters() {
    const animateCounter = (counter) => {
        const target = parseInt(counter.getAttribute('data-target'));
        const duration = 2000;
        const increment = target / (duration / 16);
        let current = 0;
        
        const updateCounter = () => {
            current += increment;
            if (current < target) {
                counter.textContent = Math.floor(current).toLocaleString();
                requestAnimationFrame(updateCounter);
            } else {
                counter.textContent = target.toLocaleString();
            }
        };
        updateCounter();
    };

    const statsObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const counters = entry.target.querySelectorAll('.counter');
                counters.forEach(counter => {
                    if (!counter.classList.contains('animated')) {
                        counter.classList.add('animated');
                        animateCounter(counter);
                    }
                });
            }
        });
    }, { threshold: 0.5 });

    document.querySelectorAll('.stat-item, .stats-grid').forEach(element => {
        statsObserver.observe(element);
    });
}

function initCardHoverEffects() {
    const cards = document.querySelectorAll('.modern-card, .pricing-card');
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-10px) scale(1.02)';
            this.style.transition = 'all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = '';
        });
    });
}

function initButtonRippleEffect() {
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.addEventListener('click', function(e) {
            const ripple = document.createElement('span');
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;
            
            ripple.style.cssText = `
                position: absolute;
                width: ${size}px;
                height: ${size}px;
                left: ${x}px;
                top: ${y}px;
                background: rgba(255,255,255,0.4);
                border-radius: 50%;
                transform: scale(0);
                animation: rippleEffect 0.6s ease-out;
                pointer-events: none;
                z-index: 0;
            `;
            
            this.appendChild(ripple);
            
            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
    });
}

// ============================================
// FAQ
// ============================================
function toggleFaq(button) {
    const answer = button.nextElementSibling;
    const icon = button.querySelector('i');
    
    // Fermer toutes les autres FAQ
    document.querySelectorAll('.faq-answer').forEach(otherAnswer => {
        if (otherAnswer !== answer && otherAnswer.classList.contains('active')) {
            otherAnswer.classList.remove('active');
            const otherButton = otherAnswer.previousElementSibling;
            const otherIcon = otherButton.querySelector('i');
            otherIcon.className = 'bi bi-plus-circle me-3 text-primary';
            
            otherAnswer.style.maxHeight = '0';
            otherAnswer.style.opacity = '0';
            setTimeout(() => {
                otherAnswer.style.display = 'none';
            }, 300);
        }
    });
    
    // Toggle FAQ actuelle
    if (answer.classList.contains('active')) {
        answer.classList.remove('active');
        icon.className = 'bi bi-plus-circle me-3 text-primary';
        answer.style.maxHeight = '0';
        answer.style.opacity = '0';
        setTimeout(() => {
            answer.style.display = 'none';
        }, 300);
    } else {
        answer.classList.add('active');
        icon.className = 'bi bi-dash-circle me-3 text-primary';
        answer.style.display = 'block';
        answer.style.maxHeight = answer.scrollHeight + 'px';
        answer.style.opacity = '1';
    }
}

// ============================================
// WHATSAPP
// ============================================
function openWhatsApp() {
    const phoneNumber = "22587168903";
    const message = encodeURIComponent(
        "Bonjour ! 👋\n\nJe suis intéressé(e) par Aude et j'aimerais en savoir plus sur vos solutions pour le BTP et l'architecture.\n\nPouvez-vous m'aider à démarrer mon essai gratuit de 30 jours ?\n\nMerci ! 😊"
    );
    
    const whatsappUrl = `https://wa.me/${phoneNumber}?text=${message}`;
    window.open(whatsappUrl, '_blank');
    
    const button = document.querySelector('.whatsapp-button');
    if (button) {
        button.style.transform = 'scale(0.9)';
        setTimeout(() => {
            button.style.transform = '';
        }, 150);
    }
}

function initWhatsAppButton() {
    const whatsappButton = document.querySelector('.whatsapp-button');
    if (whatsappButton) {
        whatsappButton.style.opacity = '0';
        whatsappButton.style.transform = 'scale(0)';
        
        setTimeout(() => {
            whatsappButton.style.transition = 'all 0.5s cubic-bezier(0.68, -0.55, 0.265, 1.55)';
            whatsappButton.style.opacity = '1';
            whatsappButton.style.transform = 'scale(1)';
        }, 2000);
    }
}

// ============================================
// MODALE VIDÉO
// ============================================
function initVideoModal() {
    const YOUTUBE_VIDEO_ID = 'VCvCNibMFuo';
    const videoModal = document.getElementById('videoModal');
    const youtubeIframe = document.getElementById('youtubeVideo');
    
    if (!videoModal || !youtubeIframe) return;
    
    const videoSrc = `https://www.youtube.com/embed/${YOUTUBE_VIDEO_ID}?autoplay=1&rel=0&modestbranding=1`;

    videoModal.addEventListener('show.bs.modal', function () {
        youtubeIframe.src = videoSrc;
    });

    videoModal.addEventListener('hide.bs.modal', function () {
        youtubeIframe.src = '';
    });
}

// ============================================
// UTILITAIRES
// ============================================
function debounce(func, wait = 20, immediate = true) {
    let timeout;
    return function() {
        const context = this, args = arguments;
        const later = function() {
            timeout = null;
            if (!immediate) func.apply(context, args);
        };
        const callNow = immediate && !timeout;
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
        if (callNow) func.apply(context, args);
    };
}

function initParallax() {
    window.addEventListener('scroll', debounce(function() {
        const heroImage = document.querySelector('.hero-image');
        if (heroImage) {
            const scrolled = window.pageYOffset;
            const parallax = scrolled * 0.05;
            heroImage.style.transform = `translateY(${parallax}px) scale(1.02)`;
        }
    }));
}

// ============================================
// INITIALISATION
// ============================================
document.addEventListener('DOMContentLoaded', function () {
    // Thème
    const savedTheme = getTheme();
    setTheme(savedTheme);
    
    // Navigation
    initSmoothScroll();
    initNavbarScroll();
    updateActiveNavLink();
    let navScrollTimeout;
    window.addEventListener('scroll', () => {
        if (navScrollTimeout) clearTimeout(navScrollTimeout);
        navScrollTimeout = setTimeout(updateActiveNavLink, 10);
    });
    
    // Animations
    initScrollReveal();
    initCounters();
    initCardHoverEffects();
    initButtonRippleEffect();
    initParallax();
    
    // WhatsApp
    initWhatsAppButton();
    
    // Vidéo
    initVideoModal();
    
    // Année actuelle
    const currentYearElement = document.getElementById('currentYear');
    if (currentYearElement) {
        currentYearElement.textContent = new Date().getFullYear();
    }
    
    // Style pour ripple effect
    const style = document.createElement('style');
    style.textContent = `
        @keyframes rippleEffect {
            to {
                transform: scale(2);
                opacity: 0;
            }
        }
        
        .btn {
            position: relative;
            overflow: hidden;
        }
        
        .btn span {
            position: relative;
            z-index: 1;
        }
    `;
    document.head.appendChild(style);
});

// Export des fonctions pour usage global
window.toggleTheme = toggleTheme;
window.toggleFaq = toggleFaq;
window.openWhatsApp = openWhatsApp;
