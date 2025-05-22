document.addEventListener('DOMContentLoaded', () => {
    const canvas = document.getElementById('particle-canvas');
    if (!canvas) {
        console.error('Particle canvas element not found');
        return;
    }
    const ctx = canvas.getContext('2d');

    let particlesArray;

    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    class Particle {
        constructor(x, y, size, color, speedX, speedY) {
            this.x = x;
            this.y = y;
            this.size = size;
            this.color = color;
            this.speedX = speedX;
            this.speedY = speedY;
        }

        draw() {
            ctx.fillStyle = this.color;
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2, false);
            ctx.fill();
        }

        update() {
            if (this.x + this.size > canvas.width || this.x - this.size < 0) {
                this.speedX = -this.speedX;
            }
            if (this.y + this.size > canvas.height || this.y - this.size < 0) {
                this.speedY = -this.speedY;
            }

            this.x += this.speedX;
            this.y += this.speedY;

            this.draw();
        }
    }

    function init() {
        particlesArray = [];
        let numberOfParticles = (canvas.height * canvas.width) / 15000; 
        numberOfParticles = Math.min(numberOfParticles, 75); 
        for (let i = 0; i < numberOfParticles; i++) {
            let size = (Math.random() * 2) + 1; 
            let x = (Math.random() * ((innerWidth - size * 2) - (size * 2)) + size * 2);
            let y = (Math.random() * ((innerHeight - size * 2) - (size * 2)) + size * 2);
            let directionX = (Math.random() * .3) - .15; 
            let directionY = (Math.random() * .3) - .15;
            let color = 'rgba(180, 180, 180, 0.4)'; 

            particlesArray.push(new Particle(x, y, size, color, directionX, directionY));
        }
    }

    function animate() {
        requestAnimationFrame(animate);
        ctx.clearRect(0, 0, innerWidth, innerHeight); 

        for (let i = 0; i < particlesArray.length; i++) {
            particlesArray[i].update();
        }
    }

    window.addEventListener('resize', () => {
        canvas.width = innerWidth;
        canvas.height = innerHeight;
        init(); 
    });

    init();
    animate();
});