document.getElementById("year").textContent = new Date().getFullYear();

// Reveal content as it enters the viewport.
const revealItems = document.querySelectorAll(
  ".section > .eyebrow, .section h2, .section-grid > *, .card, .note, .contact-box, footer"
);
revealItems.forEach((item, index) => {
  item.classList.add("reveal");
  if (item.classList.contains("card")) {
    item.style.transitionDelay = `${(index % 3) * 100}ms`;
  }
});

if ("IntersectionObserver" in window) {
  const observer = new IntersectionObserver((entries, currentObserver) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add("is-visible");
        currentObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12 });

  revealItems.forEach(item => observer.observe(item));
} else {
  revealItems.forEach(item => item.classList.add("is-visible"));
}
