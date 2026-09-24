/**
 * Saved Places
 * Stores selected researched locations in the browser for the offline demo.
 */
document.addEventListener('DOMContentLoaded', () => {
  const riskData = window.BHUDRISHTI_RISK_DATA || [];
  const storageKey = 'bhudrishtiSavedPlaces';
  const searchInput = document.getElementById('placeSearch');
  const grid = document.getElementById('savedGrid');
  const datalist = document.getElementById('allRiskPlaces');

  riskData.forEach((item) => {
    const option = document.createElement('option');
    option.value = item['Location Name'];
    datalist.appendChild(option);
  });

  function getSavedPlaces() {
    try {
      return JSON.parse(localStorage.getItem(storageKey) || '[]');
    } catch (error) {
      return [];
    }
  }

  function savePlaces(places) {
    localStorage.setItem(storageKey, JSON.stringify(places));
    renderSavedPlaces();
  }

  function riskChipClass(level) {
    if (level === 'High') return 'chip-high';
    if (level === 'Medium') return 'chip-medium';
    return 'chip-low';
  }

  function renderEmptyState() {
    const card = document.createElement('div');
    card.className = 'card';

    const message = document.createElement('p');
    message.className = 'muted';
    message.textContent = BhuApp.t('noSaved');

    card.appendChild(message);
    grid.appendChild(card);
  }

  function createPlaceCard(name) {
    const item = riskData.find(
      (location) => location['Location Name'] === name
    );

    if (!item) return null;

    const card = document.createElement('article');
    card.className = 'place-card';
    card.innerHTML = `
      <div class="place-head">
        <div>
          <div class="place-name"></div>
          <div class="muted place-type"></div>
        </div>
        <span class="status-chip"></span>
      </div>
      <div class="place-actions">
        <button class="mini-btn view" type="button"></button>
        <button class="mini-btn remove" type="button"></button>
      </div>
    `;

    card.querySelector('.place-name').textContent = name;
    card.querySelector('.place-type').textContent = BhuApp.localizeRiskType(
      item['Risk Type']
    );

    const chip = card.querySelector('.status-chip');
    chip.textContent = `${BhuApp.localizeLevel(item['Risk Level'])} ${BhuApp.t('risk')}`;
    chip.classList.add(riskChipClass(item['Risk Level']));

    const viewButton = card.querySelector('.view');
    const removeButton = card.querySelector('.remove');

    viewButton.textContent = BhuApp.t('viewDetails');
    removeButton.textContent = BhuApp.t('remove');

    viewButton.addEventListener('click', () => {
      localStorage.setItem('bhudrishtiSelectedRiskLocation', name);
      window.location.href = 'area-safety.html';
    });

    removeButton.addEventListener('click', () => {
      savePlaces(getSavedPlaces().filter((savedName) => savedName !== name));
    });

    return card;
  }

  function renderSavedPlaces() {
    const savedPlaces = getSavedPlaces();
    grid.innerHTML = '';

    if (!savedPlaces.length) {
      renderEmptyState();
      return;
    }

    savedPlaces.forEach((name) => {
      const card = createPlaceCard(name);
      if (card) grid.appendChild(card);
    });
  }

  document.getElementById('addPlace').addEventListener('click', () => {
    const name = searchInput.value.trim();
    const existsInResearch = riskData.some(
      (item) => item['Location Name'] === name
    );

    if (!existsInResearch) return;

    const savedPlaces = getSavedPlaces();
    if (!savedPlaces.includes(name)) {
      savedPlaces.push(name);
    }

    savePlaces(savedPlaces);
    searchInput.value = '';
  });

  document.addEventListener('app:language', renderSavedPlaces);
  renderSavedPlaces();
});
