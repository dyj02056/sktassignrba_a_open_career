const motionButton = document.querySelector('.motion');
const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

function setMotion(value) {
  document.body.classList.toggle('reduce-motion', value);
  motionButton.setAttribute('aria-pressed', value);
  motionButton.textContent = `모션 줄이기: ${value ? 'ON' : 'OFF'}`;
}

/* CLI 타이핑 — 줄마다 순차 등장 */
function runStoryTyping(pageEl) {
  const lines = pageEl.querySelectorAll('.story-body .cli-line');
  if (!lines.length) return;

  lines.forEach(l => l.style.animation = 'none');

  if (document.body.classList.contains('reduce-motion')) {
    lines.forEach(l => { l.style.opacity = 1; l.style.transform = 'none'; });
    return;
  }

  lines.forEach((l, i) => {
    l.style.opacity = 0;
    l.style.transform = 'translateY(4px)';
    setTimeout(() => {
      l.style.animation = '';
      l.style.opacity = '';
      l.style.transform = '';
    }, i * 220);
  });
}

function openPage(id) {
  const current = document.querySelector('.screen.active');
  const next = document.getElementById(id);
  if (!next || next === current) return;

  const reveal = () => {
    if (current) current.classList.remove('active', 'leaving');
    next.classList.add('active');
    next.scrollTop = 0;
    runStoryTyping(next);
  };

  if (document.body.classList.contains('reduce-motion') || !current) {
    reveal();
  } else {
    current.classList.add('leaving');
    setTimeout(reveal, 220);
  }
}

document.addEventListener('click', event => {
  const control = event.target.closest('[data-page]');
  if (control) openPage(control.dataset.page);
});

motionButton.addEventListener('click', () =>
  setMotion(!document.body.classList.contains('reduce-motion'))
);
setMotion(reduced);