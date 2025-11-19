// JS propio 
// Marcar filas de riesgo en reportes (usa data-porcentaje del template)
document.querySelectorAll('tr[data-porcentaje]').forEach(tr => {
  const p = parseFloat(tr.dataset.porcentaje || '0');
  if (!isNaN(p) && p < 75) tr.classList.add('riesgo');
});

// Confirmación al cerrar sesión
document.querySelectorAll('form[action$="logout"]').forEach(form => {
  form.addEventListener('submit', (e) => {
    if (!confirm('¿Seguro que querés cerrar sesión?')) e.preventDefault();
  });
});
