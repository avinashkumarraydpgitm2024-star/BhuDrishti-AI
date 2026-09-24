/**
 * Offline AI Assistant demo
 * Uses keyword matching so the prototype keeps working without an API.
 */
document.addEventListener('DOMContentLoaded', () => {
  const messages = document.getElementById('messages');
  const form = document.getElementById('chatForm');
  const input = document.getElementById('chatInput');

  let history = [];

  function renderMessages() {
    messages.innerHTML = '';

    history.forEach((message) => {
      const bubble = document.createElement('div');
      bubble.className = `bubble ${message.role}`;
      bubble.textContent = message.text;
      messages.appendChild(bubble);
    });

    messages.scrollTop = messages.scrollHeight;
  }

  function addMessage(role, text) {
    history.push({ role, text });
    renderMessages();
  }

  function getOfflineResponse(question) {
    const text = question.toLowerCase();

    if (/flood|बाढ़|paani|water/.test(text)) {
      return BhuApp.t('aiFlood');
    }

    if (/landslide|भूस्खलन|slope|slide/.test(text)) {
      return BhuApp.t('aiLandslide');
    }

    if (/route|मार्ग|rasta|map/.test(text)) {
      return BhuApp.t('aiRoute');
    }

    if (/emergency|help|खतरा|danger/.test(text)) {
      return BhuApp.t('aiEmergency');
    }

    return BhuApp.t('aiFallback');
  }

  function ask(question) {
    const cleanQuestion = question.trim();
    if (!cleanQuestion) return;

    addMessage('user', cleanQuestion);

    // Tiny delay makes the demo feel like a real chat without slowing it down.
    window.setTimeout(() => {
      addMessage('ai', getOfflineResponse(cleanQuestion));
    }, 80);
  }

  form.addEventListener('submit', (event) => {
    event.preventDefault();
    ask(input.value);
    input.value = '';
  });

  document.querySelectorAll('[data-quick]').forEach((button) => {
    button.addEventListener('click', () => {
      const quickKey = button.dataset.quick === 'landslide'
        ? 'quick1'
        : button.dataset.quick === 'flood'
          ? 'quick2'
          : 'quick3';

      ask(BhuApp.t(quickKey));
    });
  });

  function resetGreeting() {
    history = [{ role: 'ai', text: BhuApp.t('aiGreeting') }];
    renderMessages();
  }

  document.addEventListener('app:language', resetGreeting);
  resetGreeting();
});
