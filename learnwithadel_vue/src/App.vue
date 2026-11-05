<template>
  <Nav />
  <router-view />
  <Footer />
</template>

<script>
import axios from 'axios'
import Footer from './components/Footer.vue'
import Nav from '@/components/Nav.vue'
import './assets/custom-bulma.scss'

export default {
  name: 'App',
  components: { Nav, Footer },
  created() {
    const configuredApiUrl = (process.env.VUE_APP_API_URL || '').trim()
    const useInsecureApiInProduction =
      process.env.NODE_ENV === 'production' && /^http:\/\//i.test(configuredApiUrl)

    // GitHub Pages is HTTPS-only. Never ship an HTTP API endpoint in production.
    const apiUrl = configuredApiUrl && !useInsecureApiInProduction
      ? configuredApiUrl
      : '/api/v1/'

    axios.defaults.baseURL = apiUrl.endsWith('/') ? apiUrl : `${apiUrl}/`

    this.$store.commit('initializeStore')

    const token = this.$store.state.user.token
    if (token) {
      axios.defaults.headers.common.Authorization = 'Token ' + token
    } else {
      delete axios.defaults.headers.common.Authorization
    }
  }
}
</script>

<style lang="scss">
@import '../node_modules/bulma';

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

body {
  background-color: #000000;
  background-image: linear-gradient(180deg, #1a1a1a28 75%, #5e007384 100vh);
  background-size: cover;
  background-position: center center;
  background-attachment: fixed;
  background-repeat: no-repeat;
  min-height: 100vh;
  margin: 0;
  padding: 0;
}
</style>
