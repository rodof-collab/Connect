import { init, retrieveLaunchParams, mockTelegramEnv, isTMA, retrieveRawInitData } from '@tma.js/sdk';
import './style.css';

const app = document.getElementById('app');

function renderApp(initDataRaw, isMock = false) {
  if (!app) return;

  app.innerHTML = `
    <h1>Connect Mini App</h1>
    <div class="card">
      <h3>initDataRaw (для авторизации на бэкенде)</h3>
      <pre id="init-data"></pre>
    </div>
    ${isMock ? '<p style="color:#f59e0b;margin-top:16px;font-weight:500">⚠️ Мок-режим (локальная разработка)</p>' : ''}
  `;

  const initDataElement = document.getElementById('init-data');
  if (initDataElement) {
    initDataElement.textContent = initDataRaw;
  }
}

// Если не в Telegram — создаём мок-окружение
if (!isTMA()) {
  mockTelegramEnv({
    initData: {
      user: {
        id: 123456789,
        firstName: 'Test',
        username: 'testuser',
        languageCode: 'ru',
      },
      authDate: new Date(),
      hash: 'mock_hash_for_local_development',
    },
    themeParams: { bgColor: '#ffffff', textColor: '#000000' },
    version: '6.9',
    platform: 'tdesktop',
  });
  console.warn('🔧 Локальная разработка: мок-окружение Telegram');
}

try {
  init();  // просто вызываем, возвращает cleanup-функцию
  const rawData = retrieveRawInitData() || 'initData пуст';
  renderApp(rawData, !isTMA());
} catch (error) {
  console.error('Ошибка инициализации:', error.message);
  renderApp('Ошибка получения initData', true);
}
