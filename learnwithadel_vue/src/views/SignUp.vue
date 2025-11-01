<template>
  <div class="signup">
    <div class="hero is-info">
      <div class="hero-body has-text-centered">
        <h1 class="title">Sign Up</h1>
      </div>
    </div>

    <section class="section">
      <div class="container">
        <div class="columns">
          <div class="column is-4 is-offset-4">
            <form @submit.prevent="submitForm">
              <div class="field">
                <label>Email</label>
                <div class="control">
                  <input type="email" class="input" v-model="email" />
                </div>
              </div>

              <div class="field">
                <label>Password</label>
                <div class="control">
                  <input type="password" class="input" v-model="password" />
                </div>
              </div>

              <div class="field">
                <label>Repeat Password</label>
                <div class="control">
                  <input type="password" class="input" v-model="password2" />
                </div>
              </div>

              <div class="notification is-danger" v-if="errors.length">
                <p v-for="(error, idx) in errors" :key="idx">{{ error }}</p>
              </div>

              <div class="field">
                <div class="control">
                  <button type="submit" class="button is-dark">Sign Up</button>
                </div>
              </div>
            </form>

            <hr />
            Or <router-link to="/log-in">Click Here</router-link> to log in!
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      email: '',
      password: '',
      password2: '',
      errors: []
    }
  },
  mounted() {
  document.title = 'Sign Up | LearnwithAdel'
  },
  methods: {
    async submitForm() {
      this.errors = []

      if (!this.email) this.errors.push('The email is missing!')
      if (!this.password) this.errors.push('The password is missing!')
      if (this.password !== this.password2) this.errors.push('The Passwords are not matching!')

      if (this.errors.length) return

      const formData = {
        username: this.email,
        email: this.email,
        password: this.password
      }

      try {
        const regResp = await axios.post('/api/v1/users/', formData)

        const loginPayload = { username: this.email, password: this.password }
        const loginResp = await axios.post('/api/v1/token/login/', loginPayload)

        
        const token = loginResp.data.auth_token || loginResp.data.token || loginResp.data.key
        if (!token) {
          this.errors.push('Login succeeded but server did not return a token.')
          console.error('Login response:', loginResp.data)
          return
        }


        this.$store.commit('setToken', token)
        localStorage.setItem('token', token)
        axios.defaults.headers.common['Authorization'] = 'Token ' + token


        this.$router.push('/dashboard/my-account')
      } catch (error) {
        this.errors = []
        if (error.response) {
          const data = error.response.data
          if (data && typeof data === 'object') {
            for (const key in data) {
              const val = data[key]
              if (Array.isArray(val)) {
                val.forEach(v => this.errors.push(`${key}: ${v}`))
              } else {
                this.errors.push(`${key}: ${val}`)
              }
            }
          } else {
            this.errors.push(String(data))
          }
          console.error('Server responded:', error.response.status, error.response.data)
        } else if (error.request) {
          this.errors.push('No response from server — check backend is running and CORS settings.')
          console.error('No response:', error.request)
        } else {
          this.errors.push('Error: ' + error.message)
          console.error('Request error:', error.message)
        }
      }
    }
  }
}
</script>
