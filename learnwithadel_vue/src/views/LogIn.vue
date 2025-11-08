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
                  <input type="email" class="input" v-model="username" />
                </div>
              </div>

              <div class="field">
                <label>Password</label>
                <div class="control">
                  <input type="password" class="input" v-model="password" />
                </div>
              </div>

              <div class="notification is-danger" v-if="errors.length">
                <p v-for="(error, idx) in errors" :key="idx">{{ error }}</p>
              </div>

              <div class="field">
                <div class="control">
                  <button type="submit" class="button is-dark">Log in</button>
                </div>
              </div>
            </form>

            <hr />
            Or <router-link to="/sign-up">Click Here</router-link> to Sign Up!
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
    };
  },
  mounted() {
  document.title = 'Log in | LearnwithAdel'
  },
  methods: {
    submitForm() {
      this.errors = [];

      // پاک‌سازی هدر قبلی (اگر وجود دارد)
      delete axios.defaults.headers.common['Authorization'];
      localStorage.removeItem('token');

      if (!this.username) this.errors.push('The username (email) is missing!');
      if (!this.password) this.errors.push('The password is missing!');

      if (this.errors.length) return;

      const formData = {
        username: this.username,
        password: this.password
      };

      // توجه: اگر هنوز baseURL تنظیم نکردی، ممکنه لازم باشه آدرس کامل بزنی:
      // axios.post('http://localhost:8000/api/v1/token/login/', formData)
      axios.post('token/login/', formData)
        .then(response => {
          // DRF token auth معمولاً auth_token برمی‌گرداند؛ اما بسته به بک‌اند ممکنه key متفاوت باشه
          const token = response.data.auth_token || response.data.token || response.data.key;
          if (!token) {
            this.errors.push('Login succeeded but no token returned by server.');
            console.error('Login response:', response.data);
            return;
          }

          // ذخیره در vuex و localStorage (مطمئن شو mutation setToken تو localStorage را هم انجام می‌دهد)
          this.$store.commit('setToken', token);
          localStorage.setItem('token', token);

          // ست‌کردن هدر برای درخواست‌های بعدی
          axios.defaults.headers.common['Authorization'] = 'Token ' + token;

          // هدایت کاربر
          this.$router.push('/dashboard/my-account');
        })
        .catch(error => {
          this.errors = [];

          if (error.response) {
            const data = error.response.data;
            // اگر پاسخ یک شیء است (مثلاً { non_field_errors: [...], username: [...] })
            if (data && typeof data === 'object') {
              for (const key in data) {
                const val = data[key];
                if (Array.isArray(val)) {
                  val.forEach(v => this.errors.push(`${key}: ${v}`));
                } else {
                  this.errors.push(`${key}: ${val}`);
                }
              }
            } else {
              // نمایش رشته یا مقدار ساده
              this.errors.push(String(data));
            }
            console.error('Server responded with', error.response.status, error.response.data);
          } else if (error.request) {
            // درخواست ارسال شد ولی پاسخی نیامد
            this.errors.push('No response from server — check backend is running, and proxy/CORS settings.');
            console.error('No response (request):', error.request);
          } else {
            this.errors.push('Error: ' + error.message);
            console.error('Request error:', error.message);
          }
        });
    }
  }
};
</script>
