<template>
  <div class="container">
    <section 
      class="caixa-search" 
      :class="{ 'focused': isFocused }"
    >
      <input 
        v-model="searchTerm" 
        type="text" 
        placeholder="Pesquisar..." 
        class="caixa-texto"
        @focus="handleFocus" 
        @blur="handleBlur"
      >
      <button 
        class="botao-search" 
        @click="searchData"
      >
        <i class="fas fa-search" />
      </button>
    </section>
    <div class="resultContainer">
      <div 
        v-if="results.length"
      >
        <div
          v-for="(item, index) in results" 
          :key="index"
        >
          <div 
            v-for="(value, key) in item" 
            :key="key"
            class="results" 
          >
            <p v-if="key !== 'Endereco_eletronico' && key !== 'id'">
              <strong>{{ formatKey(key) }}:</strong> {{ value }}
            </p>
            <p v-else-if="key === 'Endereco_eletronico'">
              <strong>{{ formatKey(key) }}:</strong>
              <a :href="'mailto:' + value">{{ value }}</a>
            </p>
          </div>
        </div>
      </div>

      <div v-else>
        <p class="noResponse">
          Sem resultados para exibir!
        </p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      searchTerm: "",
      results: [],
      isFocused: false, // Novo estado para controlar o foco
    };
  },
  methods: {
    async searchData() {
      try {
        const response = await fetch(`http://127.0.0.1:5000/search?q=${this.searchTerm}`);
        const data = await response.json();

        this.results = Array.isArray(data) && data.length > 0 ? data : [];
      } catch (error) {
        console.error("Erro ao realizar a busca:", error);
        this.results = [];
      }
    },
    formatKey(key) {
      return key.replace(/_/g, ' ').replace(/\b\w/g, char => char.toUpperCase());
    },
    handleFocus() {
      this.isFocused = true;
    },
    handleBlur() {
      // Mantém o estado caso tenha conteúdo
      if (!this.searchTerm) {
        this.isFocused = false;
      }
    },
  },
};

</script>

<style scoped> 
*{
  margin: 0;
  padding: 0;
}
.container{
  height: 100vh;
  width: 100vw;
  background: #bfd0fc;
  display: flex; 
  align-items: center;
  justify-content: center; 
}
.resultContainer{
  height: 34.375rem;
  max-height: 100vh;
  margin-top: 4.0625rem;
  width: 34.25rem;
  display: flex;
  justify-content: center;
  align-items: center;
  background: rgba(255, 255, 255, 0.07);
  border-radius: 1rem;
  box-shadow: 0 0.25rem 30px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(0rem);
  -webkit-backdrop-filter: blur(0rem);
  overflow: auto;
}
.results{
  font-family: Arial, Helvetica, sans-serif;
}
.results p {
  margin-top: 0.3125rem;
}
.noResponse{
  font-family: Arial, Helvetica, sans-serif;
  font-size: 1.25rem;
  padding: 0.625rem;
  background: rgba(255, 255, 255, 0.07);
  border-radius: 1rem;
  box-shadow: 0 0.25rem 30px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(0rem);
  -webkit-backdrop-filter: blur(0rem);
}
.caixa-search {
    position: absolute;
    top: 2%; 
    left: 50%; 
    transform: translateX(-50%);
    background-color: #333;
    height: 2.5rem;
    border-radius: 2.5rem;
    padding: 0.625rem;
    transition: width 0.4s;
}
.caixa-search.focused > .caixa-texto,
.caixa-search:hover > .caixa-texto {
    width: 15rem;
    padding: 0 0.375rem;
}
.caixa-search.focused > .botao-search,
.caixa-search:hover > .botao-search {
    background-color: #8b8b8b;
    margin-left: 0.1875rem;
}
.caixa-texto {
    border: none;
    background-color: #333;
    outline: none;
    float: left;
    padding: 0;
    color: #fff;
    font-size: 1rem;
    transition: 0.4s;
    line-height: 2.5rem;
    width: 0rem;
    cursor: pointer;
}
.botao-search {
    color: #e84118;
    float: right;
    width: 2.5rem;
    height: 2.5rem;
    border-radius: 50%;
    background-color: #333;
    display: flex;
    justify-content: center;
    text-decoration: none;
    align-items: center;
    transition: 0.4s;
}
</style>
