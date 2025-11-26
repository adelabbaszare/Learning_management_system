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
            <div class="box profile-box has-background-light">
              <div class="media">
                <div class="media-left">
                  <figure class="image is-128x128">
                    <img :src="user.image" alt="Profile Picture" class="is-rounded profile-image">
                  </figure>
                </div>
                <div class="media-content">
                  <p class="title is-4 has-text-black">{{ user.first_name }} {{ user.last_name || user.username }}</p>
                  <p class="subtitle is-6 has-text-grey">Email: {{ user.email }}</p>
                  <p class="subtitle is-6 has-text-grey">Username: {{ user.username }}</p>

                  <span v-if="user.is_instructor" class="tag is-primary is-light is-medium mb-1">
                    <i class="fa-solid fa-graduation-cap mr-1"></i>
                    Author
                  </span>

                  <span v-else="user.is_instructor" class="tag is-secondary is-light is-medium mb-1">
                    <i class="fa-solid fa-graduation-cap mr-1"></i>
                    Student
                  </span>

                  <p class="content bio-text">
                    Bio: {{ user.bio || 'No bio available yet. Update your profile!' }}
                  </p>
                  
                  <div class="buttons mt-4">
                    <router-link to="/edit-profile" class="button is-info is-light is-small">
                      <i class="fa-solid fa-pen mr-1"></i> Edit Profile
                    </router-link>
                    <button @click="logout()" class="button is-danger is-small">
                      <i class="fa-solid fa-right-from-bracket mr-1"></i> Log Out
                    </button>
                  </div>
                </div>
              </div>
            </div>
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
        
        this.user = response.data
        
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
    border: 3px solid #7600d1;
}

.profile-box {
    box-shadow: 0 4px 6px rgba(10, 10, 10, 0.1);
    padding: 1.5rem;
    border-radius: 8px;
}

.bio-text {
    white-space: pre-wrap;
    font-style: italic;
    color: #4a4a4a;
}
</style>