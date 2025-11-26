<template>
  <div class="my-account-dashboard">
    <div class="hero is-info">
      <div class="hero-body has-text-centered">
        <h1 class="title is-2">👋 Welcome, {{ user.first_name || user.username }}!</h1>
        <h2 class="subtitle is-5">This is your Learning Dashboard</h2>
      </div>
    </div>

    <section class="section">
      <div class="container">
        
        <div class="columns is-centered mb-6">
          <div class="column is-8">
            
            <article class="panel is-primary profile-panel">
              <p class="panel-heading is-size-5 has-text-weight-semibold">
                <i class="fa-solid fa-user-circle mr-2"></i> Profile Overview
              </p>
              
              <div class="panel-block media is-align-items-center p-4">
                <div class="media-left">
                  <figure class="image is-128x128">
                    <img :src="user.image" alt="Profile Picture" class="is-rounded profile-image">
                  </figure>
                </div>
                <div class="media-content has-text-left ml-4">
                  <p class="title is-4 mb-1 has-text-white">{{ user.first_name }} {{ user.last_name || user.username }}</p>
                  
                  <span v-if="user.is_instructor" class="tag is-primary is-medium mb-1">
                    <i class="fa-solid fa-graduation-cap mr-1"></i> Author
                  </span>
                  <span v-else class="tag is-info is-medium mb-1">
                    <i class="fa-solid fa-user-graduate mr-1"></i> Student
                  </span>
                </div>
              </div>

              <p class="panel-tabs has-text-weight-bold">
                <a class="is-active">Details</a>
                <a>Actions</a>
              </p>
              
              <a class="panel-block">
                <span class="panel-icon">
                  <i class="fa-solid fa-envelope" aria-hidden="true"></i>
                </span>
                Email: <strong class="ml-2">{{ user.email }}</strong>
              </a>
              
              <a class="panel-block">
                <span class="panel-icon">
                  <i class="fa-solid fa-id-card" aria-hidden="true"></i>
                </span>
                Username: <strong class="ml-2">{{ user.username }}</strong>
              </a>

              <div class="panel-block is-block">
                <p class="subtitle is-7 has-text-grey mb-1">Bio:</p>
                <p class="content bio-text pt-1 pb-1">
                  {{ user.bio || 'No bio available yet. Update your profile!' }}
                </p>
              </div>

              <div class="panel-block buttons is-justify-content-space-between pt-4 pb-4">
                <router-link to="/edit-profile" class="button is-info is-light is-fullwidth mr-2">
                  <i class="fa-solid fa-pen mr-1"></i> Edit Profile
                </router-link>
                <button @click="logout()" class="button is-danger is-fullwidth ml-2">
                  <i class="fa-solid fa-right-from-bracket mr-1"></i> Log Out
                </button>
              </div>
            </article>

          </div>
        </div>
        
        <hr>

        <h2 class="subtitle is-size-3 has-text-weight-bold has-text-info has-text-centered mb-5">
          Your Active Courses 
          <i class="fa-solid fa-book-open ml-2"></i>
        </h2>

        <div v-if="courses.length" class="columns is-multiline">
          <div
            class="column is-12-mobile is-6-tablet is-4-desktop"
            v-for="course in courses"
            :key="course.id"
          >
            <CourseItem :course="course" />
          </div>
        </div>
        
        <div v-else class="notification is-warning has-text-centered">
            You are not enrolled in any active courses yet.
        </div>
      </div>
    </section>
  </div>
</template>

<script>

import axios from 'axios'
import CourseItem from '@/components/CourseItem.vue'

export default {
  data() {
    return {
      courses: [],
      user: {
        username: 'Loading...', 
        image: '/static/img/default-user.png', 
        email: '',
        bio: '',
        first_name: '',
        last_name: '',
        is_instructor: false,
      },
    }
  },
  components: {
    CourseItem
  },
  mounted() {
    document.title = 'Dashboard | LearnwithAdel'
    this.getUserDetails()
    this.getActiveCourses()
  },
  
  methods: {
    async getUserDetails() {
      const meUrl = '/accounts/me/' 
      
      try {
        const response = await axios.get(meUrl)
        this.$store.commit('setUserData', response.data);
        this.user = this.$store.state.user
      } catch (error) {
        console.error('Failed to load user details. Redirecting to login.', error)
        this.$router.push('/log-in') 
      }
    },
    
    getActiveCourses() {
      axios
        .get('/activities/get_active_courses/')
        .then(response => {
          this.courses = response.data
        })
        .catch(error => {
            console.error('Failed to load active courses:', error)
        })
    },

    async logout() {
      console.log('logout attempt')
      axios.defaults.headers.common['Authorization'] = ''
      localStorage.removeItem('token')
      this.$store.commit('removeToken')
      this.$router.push('/log-in')
    }
  }
}
</script>

<style scoped>
.profile-image {
    object-fit: cover;
    width: 128px;
    height: 128px;
    border: 3px solid #00d1b2;
}

.profile-panel {
    border-radius: 8px;
}

.bio-text {
    white-space: pre-wrap;
    color: #4a4a4a;
}
.panel-block {
    padding: 0.75em 1em;
}
</style>