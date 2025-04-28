document.addEventListener('DOMContentLoaded', () => {
  const cards = document.querySelectorAll('.card');
  const appearOptions = { threshold: 0.3 };
  const appearOnScroll = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      entry.target.classList.add('appear');
      observer.unobserve(entry.target);
    });
  }, appearOptions);
  cards.forEach(card => { appearOnScroll.observe(card); });
});