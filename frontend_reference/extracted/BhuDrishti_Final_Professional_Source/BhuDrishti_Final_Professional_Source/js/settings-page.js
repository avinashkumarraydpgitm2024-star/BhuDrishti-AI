/**
 * Settings page
 * Persists profile, theme and notification preferences in localStorage.
 */
document.addEventListener('DOMContentLoaded', () => {
  const displayName = document.getElementById('displayName');
  const riskAlerts = document.getElementById('riskAlerts');
  const weatherAlerts = document.getElementById('weatherAlerts');

  const riskAlertKey = 'bhudrishtiRiskAlerts';
  const weatherAlertKey = 'bhudrishtiWeatherAlerts';

  displayName.value = BhuApp.userName();

  function syncThemeButtons() {
    document.querySelectorAll('[data-set-theme]').forEach((button) => {
      button.classList.toggle(
        'active',
        button.dataset.setTheme === BhuApp.theme()
      );
    });
  }

  document.querySelectorAll('[data-set-theme]').forEach((button) => {
    button.addEventListener('click', () => {
      BhuApp.setTheme(button.dataset.setTheme);
      syncThemeButtons();
    });
  });

  document.getElementById('saveProfile').addEventListener('click', () => {
    const currentUser = BhuApp.user();
    currentUser.name = displayName.value.trim() || 'Rohit';

    localStorage.setItem('bhudrishtiUser', JSON.stringify(currentUser));
    window.location.reload();
  });

  riskAlerts.checked = localStorage.getItem(riskAlertKey) !== 'false';
  weatherAlerts.checked = localStorage.getItem(weatherAlertKey) !== 'false';

  riskAlerts.addEventListener('change', () => {
    localStorage.setItem(riskAlertKey, String(riskAlerts.checked));
  });

  weatherAlerts.addEventListener('change', () => {
    localStorage.setItem(weatherAlertKey, String(weatherAlerts.checked));
  });

  syncThemeButtons();
});
