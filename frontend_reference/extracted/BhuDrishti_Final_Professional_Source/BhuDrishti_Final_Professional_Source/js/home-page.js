/**
 * Home page risk preview
 * Reads the selected researched location and shows a compact safety summary.
 */
document.addEventListener('DOMContentLoaded', () => {
  const riskData = window.BHUDRISHTI_RISK_DATA || [];

  function renderHomeRisk() {
    const savedLocation = localStorage.getItem('bhudrishtiSelectedRiskLocation');
    const item = riskData.find(
      (location) => location['Location Name'] === savedLocation
    ) || riskData[0];

    if (!item) return;

    const score = item['Risk Score'] || 80;
    const level = item['Risk Level'] || 'High';

    const scoreElement = document.getElementById('homeRiskScore');
    const ring = document.getElementById('homeRiskRing');
    const locationElement = document.getElementById('homeRiskLocation');
    const typeElement = document.getElementById('homeRiskType');
    const chip = document.getElementById('homeRiskChip');

    scoreElement.textContent = score;
    locationElement.textContent = item['Location Name'];
    typeElement.textContent = BhuApp.localizeRiskType(item['Risk Type']);

    ring.style.setProperty('--score', score);
    ring.style.setProperty(
      '--ring',
      level === 'High'
        ? 'var(--danger)'
        : level === 'Medium'
          ? 'var(--warn)'
          : 'var(--brand)'
    );

    chip.textContent = `${BhuApp.localizeLevel(level)} ${BhuApp.t('risk')}`;
    chip.className = `status-chip ${
      level === 'High'
        ? 'chip-high'
        : level === 'Medium'
          ? 'chip-medium'
          : 'chip-low'
    }`;
  }

  renderHomeRisk();
  document.addEventListener('app:language', renderHomeRisk);
});
