/**
 * Change Detection prototype
 * Shows uploaded image previews and a simple offline sample result.
 */
document.addEventListener('DOMContentLoaded', () => {
  const oldInput = document.getElementById('oldInput');
  const newInput = document.getElementById('newInput');
  const oldPreview = document.getElementById('oldPreview');
  const newPreview = document.getElementById('newPreview');

  const changeFill = document.getElementById('changeFill');
  const changeValue = document.getElementById('changeValue');
  const summary = document.getElementById('changeSummary');
  const action = document.getElementById('changeAction');
  const impact = document.getElementById('changeImpact');

  let hasOldImage = false;
  let hasNewImage = false;
  let mode = 'empty';

  function previewImage(input, image, side) {
    const file = input.files && input.files[0];
    if (!file) return;

    const reader = new FileReader();

    reader.addEventListener('load', () => {
      image.src = reader.result;
      image.hidden = false;

      if (side === 'old') {
        hasOldImage = true;
      } else {
        hasNewImage = true;
      }
    });

    reader.readAsDataURL(file);
  }

  function renderResult(percent) {
    mode = 'result';
    changeFill.style.width = `${percent}%`;
    changeValue.textContent = `${percent}%`;
    summary.textContent = BhuApp.t('sampleSummary');
    action.textContent = BhuApp.t('sampleAction');
    impact.innerHTML = `<strong>${BhuApp.t('possibleImpact')}</strong>: ${BhuApp.t('sampleImpact')}`;
  }

  function renderEmptyState() {
    mode = 'empty';
    summary.textContent = BhuApp.t('noImages');
    action.textContent = BhuApp.t('samplePrompt');
    impact.innerHTML = `<strong>${BhuApp.t('possibleImpact')}</strong>: ${BhuApp.t('samplePrompt')}`;
  }

  oldInput.addEventListener('change', () => {
    previewImage(oldInput, oldPreview, 'old');
  });

  newInput.addEventListener('change', () => {
    previewImage(newInput, newPreview, 'new');
  });

  document.getElementById('compareBtn').addEventListener('click', () => {
    if (!hasOldImage || !hasNewImage) {
      renderEmptyState();
      return;
    }

    renderResult(34);
  });

  document.getElementById('sampleBtn').addEventListener('click', () => {
    renderResult(28);
  });

  document.addEventListener('app:language', () => {
    if (mode === 'result') {
      renderResult(parseInt(changeValue.textContent, 10) || 28);
    } else {
      renderEmptyState();
    }
  });
});
