/**
 * Research risk map
 * Markers are generated from the 30 researched locations.
 */
document.addEventListener('DOMContentLoaded', () => {
  const riskData = window.BHUDRISHTI_RISK_DATA || [];
  const mapShell = document.getElementById('mapShell');
  const filter = document.getElementById('mapFilter');
  const selectedName = document.getElementById('mapSelectedName');
  const selectedMeta = document.getElementById('mapSelectedMeta');
  const detailsButton = document.getElementById('mapDetails');

  let selectedLocation = null;

  function markerPosition(index) {
    return {
      x: 10 + ((index * 37) % 78),
      y: 12 + ((index * 29) % 68)
    };
  }

  function selectLocation(item) {
    selectedLocation = item;

    selectedName.textContent = item['Location Name'];
    selectedMeta.textContent = `${BhuApp.localizeRiskType(item['Risk Type'])} · ${BhuApp.localizeLevel(item['Risk Level'])} ${BhuApp.t('risk')}`;
    detailsButton.disabled = false;

    localStorage.setItem(
      'bhudrishtiSelectedRiskLocation',
      item['Location Name']
    );

    BhuApp.setArea(`${item['Location Name']}, Sikkim`);
  }

  function drawMarkers() {
    mapShell.querySelectorAll('.marker').forEach((marker) => marker.remove());

    const selectedLevel = filter.value;
    const visibleLocations = riskData.filter((item) => {
      return selectedLevel === 'all' || item['Risk Level'] === selectedLevel;
    });

    visibleLocations.forEach((item, index) => {
      const caseNumber = Number(item['Case ID'].split('-')[1]) || index;
      const position = markerPosition(caseNumber);
      const marker = document.createElement('button');

      marker.type = 'button';
      marker.className = `marker ${String(item['Risk Level']).toLowerCase()}`;
      marker.style.left = `${position.x}%`;
      marker.style.top = `${position.y}%`;
      marker.title = item['Location Name'];
      marker.setAttribute('aria-label', item['Location Name']);

      marker.addEventListener('click', () => selectLocation(item));
      mapShell.appendChild(marker);
    });
  }

  detailsButton.addEventListener('click', () => {
    if (selectedLocation) {
      window.location.href = 'area-safety.html';
    }
  });

  filter.addEventListener('change', drawMarkers);
  document.addEventListener('app:language', () => {
    if (selectedLocation) selectLocation(selectedLocation);
  });

  drawMarkers();
});
