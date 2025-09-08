// document.addEventListener('DOMContentLoaded', function() {
//     const navToggle = document.querySelector('.nav-toggle');
//     const navMenu = document.querySelector('.nav-menu');
    
//     if (navToggle && navMenu) {
//         navToggle.addEventListener('click', function() {
//             navMenu.classList.toggle('active');
//             navToggle.classList.toggle('active');
//         });
        
//         // Close menu when clicking on a link (mobile)
//         const navLinks = document.querySelectorAll('.nav-link');
//         navLinks.forEach(link => {
//             link.addEventListener('click', () => {
//                 navMenu.classList.remove('active');
//                 navToggle.classList.remove('active');
//             });
//         });
        
//         // Close menu when clicking outside (mobile)
//         document.addEventListener('click', function(event) {
//             const isClickInsideNav = navMenu.contains(event.target) || navToggle.contains(event.target);
            
//             if (!isClickInsideNav && navMenu.classList.contains('active')) {
//                 navMenu.classList.remove('active');
//                 navToggle.classList.remove('active');
//             }
//         });
//     }
// });


document.addEventListener('DOMContentLoaded', () => {
    // Your existing navigation toggle code
    const toggle = document.querySelector('.nav-toggle');
    const menu   = document.querySelector('.nav-menu');

    if (!toggle || !menu) return;

    // open / close
    toggle.addEventListener('click', e => {
        e.stopPropagation();
        toggle.classList.toggle('active');
        menu.classList.toggle('active');
    });

    // close when a link is clicked
    const links = document.querySelectorAll('.nav-menu .nav-link');
    links.forEach(link =>
        link.addEventListener('click', () => {
            toggle.classList.remove('active');
            menu.classList.remove('active');
        })
    );

    // close when you tap outside the menu
    document.addEventListener('click', e => {
        if (!menu.contains(e.target) && !toggle.contains(e.target)) {
            toggle.classList.remove('active');
            menu.classList.remove('active');
        }
    });

    // AUTO-SLIDE CAROUSEL FUNCTIONALITY
    const carousel = document.querySelector('#carouselExample'); // Replace with your carousel ID
    
    if (carousel) {
        // Initialize Bootstrap carousel with auto-slide
        const bootstrapCarousel = new bootstrap.Carousel(carousel, {
            interval: 1000,  // 3 seconds between slides
            ride: 'carousel',
            pause: 'hover',  // Pause on hover
            wrap: true       // Infinite loop
        });

        // Optional: Pause auto-slide when user interacts with navigation
        const carouselControls = carousel.querySelectorAll('.carousel-control-prev, .carousel-control-next, .carousel-indicators button');
        
        carouselControls.forEach(control => {
            control.addEventListener('click', () => {
                // Pause for a longer time after manual interaction
                bootstrapCarousel.pause();
                setTimeout(() => {
                    bootstrapCarousel.cycle(); // Resume auto-slide after 5 seconds
                }, 5000);
            });
        });
    }
});








document.addEventListener('DOMContentLoaded', function () {
    const carousel = document.getElementById('differentiatorCarousel');
    const indicators = document.querySelectorAll('#differentiatorIndicators .indicator');
    if (carousel && indicators.length) {
        carousel.addEventListener('slide.bs.carousel', function (event) {
            indicators.forEach(btn => btn.classList.remove('active'));
            indicators[event.to].classList.add('active');
        });
        indicators.forEach((btn, i) => {
            btn.addEventListener('click', function() {
                var car = bootstrap.Carousel.getInstance(carousel);
                car.to(i);
            });
        });
    }
});




var swiper = new Swiper(".mySwiper", {
  slidesPerView: 3,   // Number of slides visible
  spaceBetween: 30,
  navigation: {
    nextEl: ".swiper-button-next",
    prevEl: ".swiper-button-prev",
  },
  pagination: {
    el: ".swiper-pagination",
    clickable: true,
  },
  loop: true,
  autoplay: {
    delay: 2500,    // Time between slides in milliseconds (e.g., 2500ms = 2.5 seconds)
    disableOnInteraction: false,  // Continue autoplay even after user interaction
  },
});




// FAQ Toggle
    const faqQuestions = document.querySelectorAll('.faq-question');
    faqQuestions.forEach((q) => {
      q.addEventListener('click', function() {
        faqQuestions.forEach((otherQ) => {
          if (otherQ !== q) {
            otherQ.classList.remove('active');
            otherQ.parentElement.querySelector('.faq-answer').classList.remove('show');
          }
        });
        q.classList.toggle('active');
        q.parentElement.querySelector('.faq-answer').classList.toggle('show');
      });
    });