<template>
  <div class="about">
    <div class="hero is-info">
      <div class="hero-body has-text-centered">
        <h1 class="title">My Account</h1>

        <h2 class="subtitle">Welcome to your Dashboard</h2>
      </div>
    </div>

    <section class="section">
      <div class="columns is-multiline">
        <div class="column is-12">
          <h2 class="subtitle is-size-2
                    has-text-weight-normal
                    has-text-primary
                    has-text-centered"
                    >Your Active Courses 
                    <i class="fa-solid fa-book-open">
              </i>
            </h2>
        </div>

        <div
          class="column is-4"
          v-for="course in courses"
          v-bind:key="course.id"
        >
          <CourseItem :course="course" />
        </div>
      </div>
      <button @click="logout()" class="button is-danger">Log Out</button>
    </section>
  </div>
</template>

<script>
import axios from 'axios'
import CourseItem from '@/components/CourseItem.vue';

export default {

  data() {
    return {
      courses: []
    }
  },
  components: {
    CourseItem
  },
  mounted() {
    document.title = 'Dashboard | LearnwithAdel'
    axios
      .get('activities/get_active_courses/')
      .then(response => {
        console.log(response.data)

        this.courses = response.data
      })
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