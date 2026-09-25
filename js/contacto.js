/* Apheloria — formulario de contacto (envío vía Web3Forms, sin salir de la página). */

// ── Formulario de contacto: envío real vía Web3Forms (sin salir de la página) ──
const contactForm = document.getElementById('contactForm');
const contactFeedback = document.getElementById('conFeedback');
const contactSendBtn = contactForm ? contactForm.querySelector('.con-send') : null;

function showContactFeedback(message, ok) {
  contactFeedback.textContent = message;
  contactFeedback.classList.remove('is-ok', 'is-error');
  contactFeedback.classList.add(ok ? 'is-ok' : 'is-error');
  contactFeedback.hidden = false;
  requestAnimationFrame(() => contactFeedback.classList.add('visible'));
}

if (contactForm) {
  contactForm.addEventListener('submit', async e => {
    e.preventDefault();
    // Honeypot: si un bot ha rellenado este campo oculto, no enviamos nada
    if (contactForm.botcheck && contactForm.botcheck.checked) return;

    contactSendBtn.disabled = true;
    const originalLabel = contactSendBtn.textContent;
    contactSendBtn.textContent = 'Enviando…';

    try {
      const res = await fetch(contactForm.action, {
        method: 'POST',
        body: new FormData(contactForm),
        headers: { 'Accept': 'application/json' }
      });
      const data = await res.json();
      if (data.success) {
        showContactFeedback('Mensaje enviado. Te responderemos lo antes posible.', true);
        contactForm.reset();
      } else {
        showContactFeedback('No se ha podido enviar. Escríbenos a info@apheloria.es.', false);
      }
    } catch (err) {
      showContactFeedback('No se ha podido enviar. Escríbenos a info@apheloria.es.', false);
    } finally {
      contactSendBtn.disabled = false;
      contactSendBtn.textContent = originalLabel;
    }
  });
}
