/* Academy Formation – interactions (menu mobile, apparitions au scroll, formulaire) */
(function () {
  'use strict';

  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- Menu mobile ---------- */
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('nav');
  if (toggle && nav) {
    var setOpen = function (open) {
      toggle.setAttribute('aria-expanded', String(open));
      toggle.setAttribute('aria-label', open ? 'Fermer le menu' : 'Ouvrir le menu');
      nav.classList.toggle('is-open', open);
    };
    toggle.addEventListener('click', function () {
      setOpen(toggle.getAttribute('aria-expanded') !== 'true');
    });
    nav.addEventListener('click', function (e) {
      if (e.target.closest('a')) setOpen(false);
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && toggle.getAttribute('aria-expanded') === 'true') {
        setOpen(false);
        toggle.focus();
      }
    });
  }

  /* ---------- Apparitions au scroll ---------- */
  var reveals = document.querySelectorAll('.reveal');
  if (reduceMotion || !('IntersectionObserver' in window)) {
    reveals.forEach(function (el) { el.classList.add('is-visible'); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          io.unobserve(entry.target);
        }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.12 });
    reveals.forEach(function (el) { io.observe(el); });
  }

  /* ---------- Pré-sélection de la formation (?formation=…) ---------- */
  var select = document.getElementById('f-formation');
  if (select) {
    var wanted = new URLSearchParams(window.location.search).get('formation');
    if (wanted && select.querySelector('option[value="' + wanted + '"]')) select.value = wanted;
    document.querySelectorAll('[data-formation]').forEach(function (link) {
      link.addEventListener('click', function () { select.value = link.getAttribute('data-formation'); });
    });
  }

  /* ---------- Formulaire de contact ----------
     Si l'attribut data-endpoint est renseigné (ex. Formspree, Basin, script serveur),
     la demande est envoyée en POST JSON. Sinon, le client e-mail du visiteur s'ouvre
     avec un message pré-rempli adressé à data-mailto. */
  var form = document.getElementById('contact-form');
  if (!form) return;
  var status = form.querySelector('.form-status');

  var messages = {
    nom: 'Indiquez votre nom et prénom.',
    email: 'Indiquez une adresse e-mail valide (ex. nom@domaine.fr).',
    telephone: 'Indiquez un numéro de téléphone valide (10 chiffres).',
    formation: 'Choisissez la formation qui vous intéresse.',
    consentement: 'Votre accord est nécessaire pour que nous puissions vous recontacter.'
  };

  function fieldError(input) {
    var v = input.type === 'checkbox' ? input.checked : input.value.trim();
    if (input.required && !v) return messages[input.name];
    if (input.name === 'email' && v && !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v)) return messages.email;
    if (input.name === 'telephone' && v && v.replace(/[^\d]/g, '').length < 10) return messages.telephone;
    return '';
  }

  function showError(input, msg) {
    var err = document.getElementById(input.id + '-error');
    input.setAttribute('aria-invalid', msg ? 'true' : 'false');
    if (err) err.textContent = msg;
  }

  form.querySelectorAll('input, select, textarea').forEach(function (input) {
    if (!input.name || input.name === 'site') return;
    input.addEventListener('blur', function () {
      if (input.value || input.getAttribute('aria-invalid') === 'true') showError(input, fieldError(input));
    });
    input.addEventListener('input', function () {
      if (input.getAttribute('aria-invalid') === 'true') showError(input, fieldError(input));
    });
  });

  function setStatus(text, isError) {
    status.textContent = text;
    status.classList.toggle('is-error', !!isError);
  }

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    setStatus('');

    var firstInvalid = null;
    form.querySelectorAll('[required]').forEach(function (input) {
      var msg = fieldError(input);
      showError(input, msg);
      if (msg && !firstInvalid) firstInvalid = input;
    });
    ['email', 'telephone'].forEach(function (name) {
      var input = form.elements[name];
      var msg = fieldError(input);
      showError(input, msg);
      if (msg && !firstInvalid) firstInvalid = input;
    });
    if (firstInvalid) { firstInvalid.focus(); return; }

    // Champ piège anti-spam : rempli uniquement par les robots.
    if (form.elements.site && form.elements.site.value) return;

    var data = {
      nom: form.elements.nom.value.trim(),
      email: form.elements.email.value.trim(),
      telephone: form.elements.telephone.value.trim(),
      formation: form.elements.formation.options[form.elements.formation.selectedIndex].text,
      statut: form.elements.statut ? form.elements.statut.value : '',
      message: form.elements.message.value.trim()
    };

    var endpoint = form.getAttribute('data-endpoint');
    var button = form.querySelector('button[type="submit"]');

    if (endpoint) {
      button.disabled = true;
      setStatus('Envoi en cours…');
      fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
        body: JSON.stringify(data)
      }).then(function (res) {
        if (!res.ok) throw new Error(res.status);
        form.reset();
        setStatus('Merci ' + data.nom + ' ! Votre demande a bien été envoyée. Nous vous recontactons rapidement pour fixer votre entretien gratuit.');
      }).catch(function () {
        setStatus('L’envoi a échoué. Vous pouvez nous écrire directement à ' + form.getAttribute('data-mailto') + ' ou nous appeler.', true);
      }).finally(function () { button.disabled = false; });
      return;
    }

    var body = [
      'Bonjour,',
      '',
      'Je souhaite être recontacté(e) pour un entretien de préinscription.',
      '',
      'Nom : ' + data.nom,
      'E-mail : ' + data.email,
      'Téléphone : ' + data.telephone,
      'Formation souhaitée : ' + data.formation,
      data.statut ? 'Situation : ' + data.statut : '',
      data.message ? '\nMessage :\n' + data.message : ''
    ].join('\n');
    var subject = 'Demande d’information – ' + data.formation;
    window.location.href = 'mailto:' + form.getAttribute('data-mailto') +
      '?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
    setStatus('Votre messagerie s’ouvre avec votre demande pré-remplie : il ne vous reste qu’à l’envoyer. Rien ne s’ouvre ? Écrivez-nous à ' + form.getAttribute('data-mailto') + '.');
  });
})();
