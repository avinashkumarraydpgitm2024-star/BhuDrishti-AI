/**
 * Alerts page
 * Keeps the demo unread state in localStorage and hides the badge at zero.
 */
document.addEventListener('DOMContentLoaded', () => {
  const alerts = [
    { id: 'a1', level: 'High', title: 'alert1Title', body: 'alert1Body', time: 'alert1Time' },
    { id: 'a2', level: 'Medium', title: 'alert2Title', body: 'alert2Body', time: 'alert2Time' },
    { id: 'a3', level: 'Low', title: 'alert3Title', body: 'alert3Body', time: 'alert3Time' },
    { id: 'a4', level: 'Medium', title: 'alert4Title', body: 'alert4Body', time: 'alert4Time' }
  ];

  const alertsList = document.getElementById('alertsList');
  const unreadSummary = document.getElementById('unreadSummary');
  const unreadCount = document.getElementById('unreadCount');
  const markAllButton = document.getElementById('markRead');

  function markSingleAlertRead(alertId) {
    const readIds = BhuApp.getReadIds();

    if (!readIds.includes(alertId)) {
      readIds.push(alertId);
      BhuApp.setReadIds(readIds);
    }
  }

  function createAlertCard(alert, isRead) {
    const card = document.createElement('article');
    card.className = `alert-item${isRead ? '' : ' unread'}`;

    card.innerHTML = `
      <span class="alert-dot ${alert.level.toLowerCase()}"></span>
      <div class="alert-copy">
        <div class="alert-title"></div>
        <div class="muted alert-body"></div>
        <div class="alert-time"></div>
      </div>
      <button class="read-toggle" type="button"></button>
    `;

    card.querySelector('.alert-title').textContent = BhuApp.t(alert.title);
    card.querySelector('.alert-body').textContent = BhuApp.t(alert.body);
    card.querySelector('.alert-time').textContent = BhuApp.t(alert.time);

    const readButton = card.querySelector('.read-toggle');
    readButton.textContent = isRead
      ? BhuApp.t('read')
      : BhuApp.t('markThisRead');
    readButton.disabled = isRead;

    readButton.addEventListener('click', () => {
      markSingleAlertRead(alert.id);
      renderAlerts();
    });

    return card;
  }

  function renderAlerts() {
    const readIds = new Set(BhuApp.getReadIds());
    alertsList.innerHTML = '';

    alerts.forEach((alert) => {
      alertsList.appendChild(
        createAlertCard(alert, readIds.has(alert.id))
      );
    });

    const unread = BhuApp.unreadCount();
    unreadCount.textContent = unread;

    // Do not show a "0" notification badge or summary.
    unreadSummary.style.display = unread ? 'flex' : 'none';
    markAllButton.style.display = unread ? 'inline-flex' : 'none';

    if (!unread) {
      const completeMessage = document.createElement('div');
      completeMessage.className = 'notice';
      completeMessage.textContent = BhuApp.t('allCaughtUp');
      alertsList.prepend(completeMessage);
    }

    BhuApp.updateAlertBadges();
  }

  markAllButton.addEventListener('click', () => {
    BhuApp.markAllRead();
    renderAlerts();
  });

  document.addEventListener('app:language', renderAlerts);
  renderAlerts();
});
