var darkMode = (function () {
  var preferenceQuery = window.matchMedia('(prefers-color-scheme: dark)');

  return {
    isSet: function () {
      return localStorage.getItem('theme') === 'dark' || preferenceQuery.matches;
    },


    set: function (flag) {
      if (flag === undefined) {
        flag = darkMode.isSet();
      }
      document.documentElement.classList.toggle('dark', flag);
      localStorage.setItem('theme', flag ? 'dark' : 'light');
      var toggleButton = document.getElementById('theme-toggle');
      if (toggleButton) {
        toggleButton.checked = flag;
      }
    },


    addEventListeners: function () {
      var toggleButton = document.getElementById('theme-toggle');
      toggleButton.checked = darkMode.isSet();
      toggleButton.addEventListener('change', function () {
        darkMode.set(toggleButton.checked);
      });

      preferenceQuery.addEventListener('change', function (e) {
        darkMode.set(e.matches);
      });
    }

  };
})();

darkMode.set();
