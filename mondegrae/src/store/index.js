import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    dark: true,
  },
  getters: {
    dark(state) {
      return state.dark;
    }
  },
  mutations: {
    toggleTheme(state) {
      state.dark = !state.dark;
      localStorage.setItem('preferedTheme', state.dark ? 'dark' : 'light');
    }
  },
  actions: {
    toggleTheme({ commit }) {
      commit('toggleTheme')
    },
    setPreferedTheme() {
      const theme = localStorage.getItem('preferedTheme');
      if (!theme)
        return;
      this.state.dark = theme === 'dark';
    }
  }
});