/**
 * Login page behaviour
 * This is an offline prototype, so authentication is simulated locally.
 */
document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('loginForm');
  const emailInput = document.getElementById('email');
  const passwordInput = document.getElementById('password');
  const errorBox = document.getElementById('loginError');
  const demoButton = document.getElementById('demoLogin');

  function continueToVerification(email) {
    localStorage.setItem('bhudrishtiPendingEmail', email);
    localStorage.setItem(
      'bhudrishtiUser',
      JSON.stringify({ name: 'Rohit', email })
    );

    window.location.href = 'verify.html';
  }

  form.addEventListener('submit', (event) => {
    event.preventDefault();

    const email = emailInput.value.trim();
    const password = passwordInput.value;
    const isValidEmail = email.includes('@');
    const isValidPassword = password.length >= 4;

    if (!isValidEmail || !isValidPassword) {
      errorBox.textContent = BhuApp.t('loginError');
      return;
    }

    errorBox.textContent = '';
    continueToVerification(email);
  });

  demoButton.addEventListener('click', () => {
    continueToVerification('rohit@example.com');
  });

  document.addEventListener('app:language', () => {
    if (errorBox.textContent) {
      errorBox.textContent = BhuApp.t('loginError');
    }
  });
});
