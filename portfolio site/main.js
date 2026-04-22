document.addEventListener('DOMContentLoaded', () => {
    // Current Year for Footer
    document.getElementById('current-year').textContent = new Date().getFullYear();

    // Scroll Header Style
    const header = document.querySelector('header');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
    });

    // Mouse Parallax Effect
    document.addEventListener('mousemove', (e) => {
        // Normalized coordinates (-1 to 1) for the CSS translate calculations
        const x = (e.clientX / window.innerWidth) * 2 - 1;
        const y = (e.clientY / window.innerHeight) * 2 - 1;
        
        document.body.style.setProperty('--mouse-x', x);
        document.body.style.setProperty('--mouse-y', y);
    });

    // True SVG Winding Snake Scrollbar Logic
    const snakeBody = document.getElementById('snake-body');
    const snakeTrack = document.getElementById('snake-track');
    const snakeSvg = document.getElementById('snake-svg');

    function drawSVGPath() {
        if (!snakeBody || !snakeSvg) return null;
        const H = window.innerHeight;
        // Lock coordinate space to the screen's literal pixel height
        snakeSvg.setAttribute('viewBox', `0 0 20 ${H}`);
        
        // Dynamically draw a curved wave path down the whole height
        const segments = 8;
        const jump = H / segments;
        let d = `M 10 0 `;
        for(let i=0; i<segments; i++) {
            const endY = jump * (i + 1);
            const bulge = (i % 2 === 0) ? 25 : -5;
            d += `S ${bulge} ${endY - jump/2}, 10 ${endY} `;
        }
        
        if(snakeTrack) snakeTrack.setAttribute('d', d);
        snakeBody.setAttribute('d', d);
        
        // Now calculate lengths in perfectly matched units
        const length = snakeBody.getTotalLength();
        const snakeLength = Math.max(60, H * 0.1); // ~10% of screen height
        
        // Setting a massive empty gap avoids the segments multiplying
        snakeBody.style.strokeDasharray = `${snakeLength} ${length*2}`;
        return { length, snakeLength };
    }

    if (snakeBody) {
        let pathMetrics = drawSVGPath();
        
        function updateSVGScrollbar() {
            if (!pathMetrics) return;
            const scrollRect = document.documentElement.scrollHeight - window.innerHeight;
            let scrollPercent = scrollRect > 0 ? window.scrollY / scrollRect : 0;
            if (scrollPercent < 0) scrollPercent = 0;
            if (scrollPercent > 1) scrollPercent = 1;
            
            // Map the offset to push the snake down the exact path length
            const draw = -(scrollPercent * (pathMetrics.length - pathMetrics.snakeLength));
            snakeBody.style.strokeDashoffset = draw;
        }

        updateSVGScrollbar();
        window.addEventListener('scroll', updateSVGScrollbar, { passive: true });
        window.addEventListener('resize', () => {
            pathMetrics = drawSVGPath();
            updateSVGScrollbar();
        }, { passive: true });
    }

    // Code Particles Animation
    function createParticles() {
        const particlesContainer = document.getElementById('code-particles');
        const symbols = ['{', '}', '/>', '<>', '();', '[]', '=>', '&&', '||', '!='];
        
        if (!particlesContainer) return;
        
        for (let i = 0; i < 20; i++) {
            const particle = document.createElement('div');
            particle.className = 'particle';
            particle.textContent = symbols[Math.floor(Math.random() * symbols.length)];
            
            // Random styling
            particle.style.left = `${Math.random() * 100}vw`;
            particle.style.fontSize = `${Math.random() * 20 + 10}px`;
            particle.style.animationDuration = `${Math.random() * 15 + 10}s`;
            particle.style.animationDelay = `${Math.random() * 15}s`;
            
            particlesContainer.appendChild(particle);
        }
    }
    createParticles();

    // GitHub Repo Fetching & Carousel
    const githubUsername = '28promad';
    const projectsTrack = document.getElementById('projects-track');
    const indicatorsContainer = document.getElementById('carousel-indicators');
    const prevBtn = document.querySelector('.prev-btn');
    const nextBtn = document.querySelector('.next-btn');

    let currentSlide = 0;
    let totalCards = 0;
    let cardsPerView = getCardsPerView();

    // Responsive Carousel
    window.addEventListener('resize', () => {
        const newCardsPerView = getCardsPerView();
        if (newCardsPerView !== cardsPerView) {
            cardsPerView = newCardsPerView;
            updateCarousel();
        }
    });

    function getCardsPerView() {
        if (window.innerWidth <= 768) return 1;
        if (window.innerWidth <= 992) return 2;
        return 3;
    }

    // Helper to format language to display tag
    function getTechTags(language, topics = []) {
        let tagsHTML = '';
        if (language) {
            tagsHTML += `<span class="tech-tag">${language}</span>`;
        }
        // Slice topics to show max 3 to prevent overflow
        topics.slice(0, 3).forEach(topic => {
            tagsHTML += `<span class="tech-tag">${topic}</span>`;
        });
        return tagsHTML || `<span class="tech-tag">Code</span>`;
    }

    async function fetchGitHubProjects() {
        try {
            const response = await fetch(`https://api.github.com/users/${githubUsername}/repos?sort=updated`);
            
            if (!response.ok) {
                throw new Error('Failed to fetch from GitHub');
            }

            const repos = await response.json();
            
            // Filter out forks or specific repos if needed, and take top ones
            const selectedRepos = repos
                .filter(repo => !repo.fork) // Don't show forked repos
                .slice(0, 9); // Show up to 9 recent non-forked projects

            if (selectedRepos.length === 0) {
                projectsTrack.innerHTML = '<p style="text-align: center; width: 100%;">No projects found.</p>';
                return;
            }

            // Clear loading skeleton
            projectsTrack.innerHTML = '';
            indicatorsContainer.innerHTML = '';

            selectedRepos.forEach((repo, index) => {
                // Determine icon based on language/content
                let iconClass = 'fa-code';
                if (repo.language === 'Python') iconClass = 'fa-python';
                else if (repo.language === 'JavaScript' || repo.language === 'TypeScript') iconClass = 'fa-js';
                else if (repo.language === 'HTML' || repo.language === 'CSS') iconClass = 'fa-html5';

                const card = document.createElement('div');
                card.className = 'glass-card project-card';
                card.innerHTML = `
                    <i class="fab ${iconClass} project-icon"></i>
                    <h3 class="project-title">${repo.name.replace(/[-_]/g, ' ')}</h3>
                    <p class="project-desc">${repo.description || 'A super cool project by Phillip Madadangoma.'}</p>
                    <div class="project-tech">
                        ${getTechTags(repo.language, repo.topics)}
                    </div>
                    <div class="project-links">
                        <a href="${repo.html_url}" target="_blank" rel="noopener noreferrer"><i class="fab fa-github"></i> Repository</a>
                        ${repo.homepage ? `<a href="${repo.homepage}" target="_blank" rel="noopener noreferrer"><i class="fas fa-external-link-alt"></i> Live Demo</a>` : ''}
                    </div>
                `;
                projectsTrack.appendChild(card);

                // Create Indicator (1 per slide logic)
                // If 9 projects and 3 per view = 7 slides max (0 to 6)
            });

            totalCards = selectedRepos.length;
            createIndicators();
            updateCarousel();

        } catch (error) {
            console.error('Error fetching projects:', error);
            projectsTrack.innerHTML = '<p style="text-align: center; width: 100%; color: #ff6b6b;">Failed to load projects. Please try again later.</p>';
        }
    }

    function createIndicators() {
        indicatorsContainer.innerHTML = '';
        const maxScrolls = Math.max(0, totalCards - cardsPerView);
        
        for (let i = 0; i <= maxScrolls; i++) {
            const dot = document.createElement('div');
            dot.className = `indicator ${i === 0 ? 'active' : ''}`;
            dot.addEventListener('click', () => {
                currentSlide = i;
                updateCarousel();
            });
            indicatorsContainer.appendChild(dot);
        }
    }

    function updateCarousel() {
        if (totalCards === 0) return;
        
        const maxScrolls = Math.max(0, totalCards - cardsPerView);
        if (currentSlide > maxScrolls) currentSlide = maxScrolls;
        
        const cardWidth = projectsTrack.children[0].offsetWidth;
        const gap = parseInt(window.getComputedStyle(projectsTrack).gap) || 32; // 2rem = 32px based on CSS
        
        // Calculate translation
        const translateValue = currentSlide * (cardWidth + gap);
        projectsTrack.style.transform = `translateX(-${translateValue}px)`;

        // Update Buttons
        prevBtn.style.opacity = currentSlide === 0 ? '0.5' : '1';
        prevBtn.style.cursor = currentSlide === 0 ? 'default' : 'pointer';
        
        nextBtn.style.opacity = currentSlide >= maxScrolls ? '0.5' : '1';
        nextBtn.style.cursor = currentSlide >= maxScrolls ? 'default' : 'pointer';

        // Update Indicators
        const indicators = indicatorsContainer.querySelectorAll('.indicator');
        indicators.forEach((ind, idx) => {
            if (idx === currentSlide) ind.classList.add('active');
            else ind.classList.remove('active');
        });
    }

    prevBtn.addEventListener('click', () => {
        if (currentSlide > 0) {
            currentSlide--;
            updateCarousel();
        }
    });

    nextBtn.addEventListener('click', () => {
        const maxScrolls = Math.max(0, totalCards - cardsPerView);
        if (currentSlide < maxScrolls) {
            currentSlide++;
            updateCarousel();
        }
    });

    // Auto play (optional, uncomment to enable)
    // setInterval(() => {
    //     const maxScrolls = Math.max(0, totalCards - cardsPerView);
    //     if (currentSlide < maxScrolls) {
    //         currentSlide++;
    //     } else {
    //         currentSlide = 0;
    //     }
    //     updateCarousel();
    // }, 5000);

    // Initialize
    fetchGitHubProjects();
});
