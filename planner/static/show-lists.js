document.querySelectorAll('.show-group-toggle').forEach(button => {
  const list = document.getElementById(button.getAttribute('aria-controls'));
  const label = button.querySelector('.show-group-toggle-label');

  button.addEventListener('click', () => {
    const expanded = button.getAttribute('aria-expanded') === 'true';
    list.hidden = expanded;
    button.setAttribute('aria-expanded', String(!expanded));
    label.textContent = expanded ? 'Expand' : 'Collapse';
  });
});
