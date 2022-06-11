import Vue from 'vue';
import App from './App.vue';

import store from './store';
import router from './router';

import i18n from './i18n';

import Toast from 'vue-toast-notification';

import '@/assets/css/tailwind.css';
import 'vue-toast-notification/dist/theme-sugar.css';

import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

import { fas } from '@fortawesome/free-solid-svg-icons'
import { far } from '@fortawesome/free-regular-svg-icons'
import { fab } from '@fortawesome/free-brands-svg-icons'

Vue.use(Toast);
Vue.config.productionTip = false;

new Vue({
    router,
    i18n,
    store,
    render: h => h(App),
}).$mount('#app');

library.add(
    fas, far, fab
)

Vue.component('font-awesome-icon', FontAwesomeIcon)