// theme/tailwind.config.js
module.exports = {
  content: [
    // 🧩 HTML-шаблони з самої theme app
    '../templates/**/*.html',

    // 🧩 Глобальні шаблони (base.html і т.п.)
    '../../templates/**/*.html',

    // 🧩 Шаблони з інших Django-додатків (users, catalog тощо)
    '../../**/templates/**/*.html',

    // 🧩 JS або React-компоненти всередині theme/static_src/src/
    './src/**/*.js',
  ],
  theme: {
    extend: {}, // тут зможете додавати кастомні кольори, шрифти тощо
  },
  plugins: [
    require('@tailwindcss/forms'), // 🎨 автоматичне стилювання форм
    require('daisyui'),            // 💎 набір готових Tailwind-компонентів
  ],
}
