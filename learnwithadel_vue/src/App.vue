<template>
  <Nav/>
  <router-view/>
  <Footer/>
</template>

<script>
import axios from 'axios';
import Footer from './components/Footer.vue';
import Nav from '@/components/Nav.vue';
import './assets/custom-bulma.scss';

axios.defaults.baseURL = 'http://localhost:8000/api/v1/'
export default {
  name: 'App',
  components: { Nav, Footer },
  created() {

    const apiUrl = process.env.VUE_APP_API_URL || 'http://localhost:8000/api/v1/';

    axios.defaults.baseURL = apiUrl;

    this.$store.commit('initializeStore');

    const token = this.$store.state.user.token;
    if (token) {
      axios.defaults.headers.common['Authorization'] = 'Token ' + token;
    } else {

      delete axios.defaults.headers.common['Authorization'];
    }
  }
}
</script>



<style lang="scss">
@import '../node_modules/bulma';
//@import '../src/assets/custom-bulma.scss';

@keyframes heartbeat {
  0%, 20%, 40%, 60%, 80%, 100% {
    transform: scale(1);
  }
  10%, 30%, 50%, 70%, 90% {
    transform: scale(1.3);
  }
}

.purple-heart {
  display: inline-block;
  color: purple;
  animation: heartbeat 4s infinite;
}

.made-by {
  margin-bottom: 0.5rem;
  font-size: 1.1rem;
}
</style>