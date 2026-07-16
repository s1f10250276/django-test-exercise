(function () {
  const STORAGE_KEY = 'todo-theme';
  const THEMES = ['blue', 'red', 'yellow', 'green', 'white', 'black'];

  function getSystemTheme() {
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }

  function getStoredTheme() {
    const storedTheme = window.localStorage.getItem(STORAGE_KEY);
    return THEMES.includes(storedTheme) ? storedTheme : 'blue';
  }

  function applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    document.documentElement.style.colorScheme = getSystemTheme();
  }

  document.addEventListener('DOMContentLoaded', function () {
    const select = document.getElementById('theme-select');
    if (!select) {
      return;
    }

    const storedTheme = getStoredTheme();
    select.value = storedTheme;
    applyTheme(storedTheme);

    select.addEventListener('change', function () {
      const theme = this.value;
      window.localStorage.setItem(STORAGE_KEY, theme);
      applyTheme(theme);
    });

    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function () {
      applyTheme(getStoredTheme());
    });
  });
})();
