module.exports = {
  parser: 'vue-eslint-parser',
  parserOptions: {
    parser: 'babel-eslint',  // Certifique-se de que o Babel está configurado
  },
  extends: [
    'eslint:recommended',
    'plugin:vue/vue3-recommended',
  ],
  env: {
    browser: true,
    node: true,
    es6: true,
  },
  rules: {
    // Adicione ou modifique as regras do ESLint aqui
  },
};
