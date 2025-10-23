<template>
  <div class="login">
    <div class="hero is-info">
      <div class="hero-body has-text-centered">
        <h1 class="title">Log In</h1>

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
                            <input type="email" class="input" v-model="username"></input>
                        </div>
                    </div>

                    <div class="field">
                        <label>Password</label>
                        <div class="control">
                            <input type="password" class="input" v-model="password"></input>
                        </div>
                    </div>

                    <div class="notification is-danger" v-if="errors.length">
                        <p
                            v-for="error in errors"
                            :key="error"
                        >
                            {{ error }}
                        </p>
                    </div>

                    <div class="filed">
                        <div class="control">
                            <div class="button is-dark">Log in</div>
                        </div>
                    </div>

                </form>

                <hr>
                Or <router-link to="/sign-up">Click Here</router-link> to Sign Up!
            </hr>
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
      username: '',
      password: '',
      errors: []
    }
  },
  methods: {
    submitForm() {
      console.log('submitForm')

      axios.defaults.headers.common['Authorization'] = ""

      localStorage.removeItem('token')

      this.errors = []

      if (this.username === '') {
        this.errors.push('The username is missing!')
      }

      if (this.password === '') {
        this.errors.push('The password is missing!')
      }

      if (!this.errors.length){
        const formData = {
            username: this.username,
            password: this.password
        }

        axios
            .post('/api/v1/token/login/', formData)
            .then(response => {
                const token = response.data.auth_token

                this.$store.commit('setToken', token)

                axios.defaults.headers.common['Authorization'] = "Token " + token

                localStorage.setItem('token', token)

                this.$router.push('/dashboard/my-account')
            })
            .catch(error => {
                if (error.response) {
                    for (const property in error.response.data) {
                    this.errors.push(`${property}: ${error.response.data[property]}`)  
                    }

                    console.log(JSON.stringify(error))
                } else if (error.message) {
                    this.errors.push('Something went wrong.Please try again')

                    console.log(JSON.stringify(error))
                }
            })
      }
    }
  }
}
</script>
