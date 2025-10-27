<template>
  <div class="courses">
    <div class="hero is-info">
      <div class="hero-body has-text-centered">
        <h1 class="title is-3 has-text-weight-bold" v-if="course">{{ course.title }}</h1>
        <h1 class="title is-3 has-text-weight-bold" v-else>Loading...</h1>
        <h2 class="subtitle">An Online place for learning what you want</h2>
      </div>
    </div>

    <section class="section">
      <div class="container">
        <div class="columns content">
          <div class="column is-2">
            <h2>Table of Content</h2>
            <ul>
              <li
                v-for="lesson in lessons" 
                v-bind:key="lesson.id"
              >

                <a href="#">{{ lesson.title }}</a></li>
            </ul>
          </div>

          <div class="column is-10">
            <div v-if="loading">Loading...</div>

            <div v-else-if="error" class="notification is-danger">{{ error }}</div>


            <div v-else-if="course">
              <div v-if="isAuthenticated">

                <h2 v-if="activeLesson">{{ activeLesson.title }}</h2>

                <h2 v-else>Introduction</h2>
                
                <div v-if="course.long_description" v-html="course.long_description"></div>
                <div v-else-if="course.short_description">{{ course.short_description }}</div>
                <div v-else>No description available.</div>
              </div>

              <div v-else>
                <h2>Preview</h2>
                <p>{{ course.short_description || 'Preview not available.' }}</p>
                <p class="has-text-danger">Restricted Access! You need an account to view full content.</p>
                <router-link :to="{ name: 'SignUp' }" class="button is-info mr-3">Sign up</router-link>
                <router-link :to="{ name: 'LogIn' }" class="button is-info">Log in</router-link>
              </div>
            </div>


            <div v-else>
              <p>No course data available.</p>
            </div>
          </div>

        </div>
      </div>
    </section>
  </div>
</template>


<script>
import axios from 'axios'

export default {
  data() {
    return {
      course: {},
      lessons: [],
      loading: false,
      error: null
    }
  },
  computed: {
    isAuthenticated() {
      return this.$store?.state?.user?.isAuthenticated
    }
  },
  
  async mounted() {
    this.loading = true
    this.error = null

    const slug = this.$route.params.slug
    if (!slug) {
      this.error = 'Course slug missing.'
      this.loading = false
      return
    }

    try {
      const resp = await axios.get(`/api/v1/courses/${slug}/`)
      console.log('course fetch', resp.data)

      // اگر API ساختار { course: {...}, lesson: [...] } برگردانده
      if (resp.data && resp.data.course) {
        this.course = resp.data.course
        this.lessons = resp.data.lesson || []
      } else {
        // در حالت معمول که API مستقیم course برمی‌گرداند
        this.course = resp.data
        this.lessons = resp.data.lessons || resp.data.lesson || []
      }
      // مقداردهی پیش‌فرض activeLesson به اولین درس در صورت وجود
      this.activeLesson = (this.lessons && this.lessons.length) ? this.lessons[0] : null

    } catch (err) {
      console.error('Failed to load course:', err)
      if (err.response && err.response.status === 404) {
        this.error = 'Course not found.'
      } else if (err.response && (err.response.status === 401 || err.response.status === 403)) {
        // fallback: try to get preview from list
        try {
          const listResp = await axios.get('/api/v1/courses/')
          const found = listResp.data.find(c => c.slug === slug)
          if (found) this.course = found
          else this.error = 'Course not found.'
        } catch {
          this.error = 'Failed to load course preview.'
        }
      } else {
        this.error = 'Failed to load course. Please try again later.'
      }
    } finally {
      this.loading = false
    }
  }
}
</script>
