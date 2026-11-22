import { retrieveLaunchParams, init } from '@telegram-apps/sdk';
import './style.css';

const app = document.getElementById('app');

function renderApp(initDataRaw, isMock = false) {
  if (!app) return;
  app.innerHTML = `
    <h1>Connect Mini App</h1>
    <div class="card">
      <h3>initDataRaw (для авторизации на бэкенде)</h3>
      <pre id ="init-data"></pre>
    </div>
    ${isMock ? '<p style="color: #f59e0b; margin-top: 16px; font-weight: 500;">⚠️ Мок-режим (локальная разработка)</p>' : ''}
  `;
  const initDataElement = document.getElementById('init-data');
  if (initDtaElement) {
    initDataElement.textContent = initDtaRaw;
  }
}

try {
  const launchParams = retrieveLaunchParams();
  const sdk = init(launchParams);
  sdk.mount();
  const rawData = launchParams.initDataRaw || 'initData пуст';
  renderApp(rawData, false);
} catch (error) {
  console.warn('🔧 Локальная разработка: используем мок-данные.', error.message);
  const mockInitData = 'user=%7B%22id%22%3A123456789%2C%22first_name%22%3A%22Test%22%2C%22username%22%3A%22testuser%22%7D&auth_date=1700000000&hash=mock_hash_for_local_development';
  renderApp(mockInitData, true);
}
