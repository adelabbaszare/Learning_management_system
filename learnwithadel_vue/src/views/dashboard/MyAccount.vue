<template>
  <div class="about">
    <div class="hero is-info">
      <div class="hero-body has-text-centered">
        <h1 class="subtitle">My Account💻</h1>

        <h2 class="subtitle">Welcome to your Dashboard</h2>
      </div>
    </div>
    <section class="section">
      <button @click="logout()" class="button is-danger">Log Out</button>
    </section>
  </div>
</template>

<script>
import axios from 'axios'

export default {

  mounted() {
    document.title = 'Dashboard | LearnwithAdel'
  },

  methods: {
    async logout() {
      console.log('logout')

      await axios
      .post('token/logout')
      .then(response => {
        console.log('Logged out')
      })

      axios.defaults.headers.common['Authorization'] = ""

      localStorage.removeItem('token');

      this.$store.commit('removeToken');
      
      this.$router.push('/log-in')

    }
  }
}
</script>