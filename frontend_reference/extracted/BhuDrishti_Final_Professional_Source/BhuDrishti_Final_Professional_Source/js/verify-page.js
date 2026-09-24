/**
 * OTP verification for the offline prototype.
 * Demo code: 123456
 */
document.addEventListener('DOMContentLoaded', () => {
  const inputs = Array.from(document.querySelectorAll('.otp'));
  const form = document.getElementById('verifyForm');
  const errorBox = document.getElementById('verifyError');
  const email = document.getElementById('verifyEmail');
  let messageKey = '';

  email.textContent = localStorage.getItem('bhudrishtiPendingEmail') || 'rohit@example.com';

  function currentCode() {
    return inputs.map((input) => input.value).join('');
  }

  function fillCode(value) {
    const digits = String(value).replace(/\D/g, '').slice(0, 6);

    inputs.forEach((input, index) => {
      input.value = digits[index] || '';
    });

    const nextEmpty = inputs.find((input) => !input.value);
    (nextEmpty || inputs[inputs.length - 1]).focus();
  }

  inputs.forEach((input, index) => {
    input.addEventListener('input', () => {
      input.value = input.value.replace(/\D/g, '').slice(-1);

      if (input.value && inputs[index + 1]) {
        inputs[index + 1].focus();
      }
    });

    input.addEventListener('keydown', (event) => {
      if (event.key === 'Backspace' && !input.value && inputs[index - 1]) {
        inputs[index - 1].focus();
      }
    });

    input.addEventListener('paste', (event) => {
      event.preventDefault();
      fillCode(event.clipboardData.getData('text'));
    });
  });

  form.addEventListener('submit', (event) => {
    event.preventDefault();

    if (currentCode() !== '123456') {
      messageKey = 'verifyError';
      errorBox.textContent = BhuApp.t(messageKey);
      return;
    }

    messageKey = '';
    errorBox.textContent = '';
    localStorage.setItem('bhudrishtiVerified', 'true');
    window.location.href = 'home.html';
  });

  document.getElementById('resendBtn').addEventListener('click', () => {
    messageKey = 'resendDone';
    errorBox.textContent = BhuApp.t(messageKey);
  });

  document.addEventListener('app:language', () => {
    if (messageKey) {
      errorBox.textContent = BhuApp.t(messageKey);
    }
  });
});
