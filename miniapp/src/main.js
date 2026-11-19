import './style.css';

const app = document.getElementById('app');

// Проверяем, открыто ли приложение внутри Telegram
const isTelegram = window.location.href.includes('t.me') || 
                   window.location.href.includes('web.app');

let initDataRaw = 'initData отсутствует (открыто вне Telegram)';
let mockUser = null;

if (!isTelegram) {
  // Локальная разработка — создаём мок
  console.warn('🔧 Локальная разработка: используем мок-данные');
  mockUser = {
    id: 123456789,
    first_name: 'Test',
    last_name: 'User',
    username: 'testuser',
    language_code: 'ru',
  };
  initDataRaw = 'user=' + encodeURIComponent(JSON.stringify(mockUser)) + 
                '&auth_date=' + Math.floor(Date.now() / 1000) + 
                '&hash=mock_hash_for_local_development';
} else {
  // В Telegram — пробуем получить реальные данные
  try {
    import('@tma.js/sdk').then(({ retrieveLaunchParams }) => {
      const lp = retrieveLaunchParams();
      initDataRaw = lp.initDataRaw || 'initData пуст';
      renderApp(initDataRaw);
    });
  } catch (e) {
    console.error('Ошибка получения initData:', e);
  }
}

function renderApp(data) {
  app.innerHTML = `
    <h1>Connect Mini App</h1>
    <div class="card">
      <h3>initDataRaw (для авторизации на бэкенде)</h3>
      <pre>${data}</pre>
    </div>
    ${mockUser ? '<p style="color: orange; margin-top: 16px;">⚠️ Мок-режим (локальная разработка)</p>' : ''}
  `;
}

renderApp(initDataRaw);