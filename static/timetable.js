// Day-card filtering for the timetable views, plus a few small
// quality-of-life additions. All of this is progressive enhancement —
// if JS fails to load, forms and buttons still work exactly as before.

(function dayTabs() {
  const tabs = document.querySelector('[data-day-tabs]');
  const list = document.querySelector('[data-class-list]');
  if (!tabs || !list) return;

  const rows = Array.from(list.querySelectorAll('.class-row'));
  const emptyState = list.querySelector('.empty-state');
  const buttons = Array.from(tabs.querySelectorAll('button'));
  const storageKey = 'timesync:day:' + location.pathname + location.search;

  function countFor(day) {
    return rows.filter((row) => row.dataset.day === day).length;
  }

  buttons.forEach((btn) => {
    const n = countFor(btn.dataset.day);
    const countEl = btn.querySelector('.count');
    if (countEl) countEl.textContent = `(${n})`;
  });

  function selectDay(day, { persist = true } = {}) {
    buttons.forEach((btn) => {
      btn.setAttribute('aria-selected', String(btn.dataset.day === day));
    });

    let visible = 0;
    rows.forEach((row) => {
      const match = row.dataset.day === day;
      row.hidden = !match;
      if (match) visible += 1;
    });

    if (emptyState) {
      emptyState.hidden = visible !== 0;
      emptyState.innerHTML = `<span class="material-symbols-outlined">event_busy</span><span>No classes scheduled for ${day}</span>`;
    }

    if (persist) {
      try {
        sessionStorage.setItem(storageKey, day);
      } catch (e) {
        /* storage unavailable (private browsing etc.) — fine, just won't persist */
      }
    }
  }

  buttons.forEach((btn, i) => {
    btn.addEventListener('click', () => selectDay(btn.dataset.day));

    // Arrow-key navigation between tabs, wrapping at either end.
    btn.addEventListener('keydown', (e) => {
      if (e.key !== 'ArrowRight' && e.key !== 'ArrowLeft') return;
      e.preventDefault();
      const next = e.key === 'ArrowRight' ? (i + 1) % buttons.length : (i - 1 + buttons.length) % buttons.length;
      buttons[next].focus();
      selectDay(buttons[next].dataset.day);
    });
  });

  const today = new Date().toLocaleDateString('en-US', { weekday: 'long' });
  const todayBtn = buttons.find((b) => b.dataset.day === today);
  if (todayBtn) todayBtn.classList.add('is-today');

  let stored = null;
  try {
    stored = sessionStorage.getItem(storageKey);
  } catch (e) {
    /* ignore */
  }

  const defaultDay =
    (stored && buttons.some((b) => b.dataset.day === stored) && stored) ||
    (todayBtn && today) ||
    buttons[0]?.dataset.day;

  if (defaultDay) selectDay(defaultDay, { persist: false });

  // Confirm before a delete button actually submits, so a mis-tap on
  // mobile can't silently remove a class.
  list.addEventListener('click', (e) => {
    const btn = e.target.closest('button[formaction]');
    if (btn && btn.formAction && btn.formAction.includes('/delete/')) {
      if (!confirm('Delete this class?')) e.preventDefault();
    }
  });
})();

// Remember the last branch/section looked up (used by both the public
// home page and the admin "modify timetable" form, which share the
// same #table_selection id) so it's pre-filled next visit.
(function rememberSelection() {
  const form = document.getElementById('table_selection');
  if (!form) return;

  const branch = form.querySelector('[name="branch"]');
  const section = form.querySelector('[name="section"]');
  if (!branch || !section) return;

  const KEY = 'timesync:last-selection';

  try {
    const saved = JSON.parse(localStorage.getItem(KEY) || 'null');
    if (saved) {
      if (saved.branch) branch.value = saved.branch;
      if (saved.section) section.value = saved.section;
    }
  } catch (e) {
    /* ignore bad/missing storage */
  }

  form.addEventListener('submit', () => {
    try {
      localStorage.setItem(KEY, JSON.stringify({ branch: branch.value, section: section.value }));
    } catch (e) {
      /* ignore */
    }
  });
})();
