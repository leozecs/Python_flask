// theme.js - Suporte para index.html e agenda.html

document.addEventListener('DOMContentLoaded', () => {
  const body = document.body;
  const themeToggle = document.getElementById('themeToggle');
  const savedTheme = localStorage.getItem('theme') || 'light';

  function setTheme(theme) {
    body.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
    if (themeToggle) themeToggle.textContent = theme === 'dark' ? '🌙' : '🌞';
  }

  if (themeToggle) {
    themeToggle.addEventListener('click', () => {
      const current = body.getAttribute('data-theme');
      setTheme(current === 'light' ? 'dark' : 'light');
    });
  }

  setTheme(savedTheme);

  // Controle de abas no index.html
  const tabs = document.querySelectorAll('[role="tab"]');
  const loginForm = document.getElementById('form-login');
  const registerForm = document.getElementById('form-register');

  if (tabs.length && loginForm && registerForm) {
    tabs.forEach(tab => {
      tab.addEventListener('click', () => switchTab(tab.dataset.tab));
    });

    function switchTab(tab) {
      tabs.forEach(t => {
        const isActive = t.dataset.tab === tab;
        t.classList.toggle('active', isActive);
        t.setAttribute('aria-selected', isActive);
      });
      loginForm.classList.toggle('active', tab === 'login');
      registerForm.classList.toggle('active', tab === 'register');
    }
  }

  // Dropdown de usuário no agenda.html
  const userButton = document.getElementById('userButton');
  const dropdownMenu = document.getElementById('dropdownMenu');

  if (userButton && dropdownMenu) {
    userButton.addEventListener('click', () => {
      const isOpen = dropdownMenu.style.display === 'block';
      dropdownMenu.style.display = isOpen ? 'none' : 'block';
    });

    document.addEventListener('click', (e) => {
      if (!userButton.contains(e.target) && !dropdownMenu.contains(e.target)) {
        dropdownMenu.style.display = 'none';
      }
    });
  }

  // Modal de adicionar contato no agenda.html
  const openModal = document.getElementById('btnAddContact');
  const cancelModal = document.getElementById('cancelModal');
  const modal = document.getElementById('modalAddContact');

  if (openModal && cancelModal && modal) {
    openModal.addEventListener('click', () => {
      modal.classList.add('active');
    });

    cancelModal.addEventListener('click', () => {
      modal.classList.remove('active');
    });
  }
});