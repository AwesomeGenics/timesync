// Day-card filtering for the timetable views.
// Rows are rendered server-side with data-day on each <li>; this just
// shows/hides them per selected tab, so it works even if JS fails to load
// (all classes stay visible, just not split by day).

(function () {
  const tabs = document.querySelector('[data-day-tabs]');
  const list = document.querySelector('[data-class-list]');
  if (!tabs || !list) return;

  const rows = Array.from(list.querySelectorAll('.class-row'));
  const emptyState = list.querySelector('.empty-state');
  const buttons = Array.from(tabs.querySelectorAll('button'));

  function countFor(day) {
    return rows.filter((row) => row.dataset.day === day).length;
  }

  buttons.forEach((btn) => {
    const n = countFor(btn.dataset.day);
    const countEl = btn.querySelector('.count');
    if (countEl) countEl.textContent = n ? `(${n})` : '(0)';
  });

  function selectDay(day) {
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
      emptyState.textContent = `No classes scheduled for ${day}.`;
    }
  }

  buttons.forEach((btn) => {
    btn.addEventListener('click', () => selectDay(btn.dataset.day));
  });

  const today = new Date().toLocaleDateString('en-US', { weekday: 'long' });
  const defaultDay = buttons.some((b) => b.dataset.day === today)
    ? today
    : buttons[0]?.dataset.day;

  if (defaultDay) selectDay(defaultDay);
})();
