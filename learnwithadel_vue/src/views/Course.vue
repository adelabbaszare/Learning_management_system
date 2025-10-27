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
              <li v-for="lesson in lessons" :key="lesson.id">
                <a href="#" @click.prevent="setActiveLesson(lesson)">{{ lesson.title }}</a>
              </li>
            </ul>
          </div>

          <div class="column is-10">
            <div v-if="loading">Loading...</div>

            <div v-else-if="error" class="notification is-danger">{{ error }}</div>

            <div v-else-if="course">
              <div v-if="isAuthenticated">

                <h2 v-if="activeLesson">{{ activeLesson.title }}</h2>
                <h2 v-else>Introduction</h2>

                <div v-if="activeLesson && activeLesson.long_description" v-html="activeLesson.long_description"></div>
                <div v-else-if="course.long_description" v-html="course.long_description"></div>
                <div v-else-if="course.short_description">{{ course.short_description }}</div>
                <div v-else>No description available.</div>

                <hr />

                <form @submit.prevent="submitComment">
                  <div class="field">
                    <label class="label">Name</label>
                    <div class="control">
                      <input type="text" class="input" v-model="comment.name" />
                    </div>
                  </div>

                  <div class="field">
                    <label class="label">Content</label>
                    <div class="control">
                      <textarea class="textarea" v-model="comment.content"></textarea>
                    </div>
                  </div>

                  <div class="field">
                    <div class="control">
                      <button type="submit" class="button is-link">Submit</button>
                    </div>
                  </div>
                </form>

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
      course: null,
      lessons: [],
      activeLesson: null,
      comment: { name: '', content: '' },
      loading: false,
      error: null
    }
  },
  computed: {
    isAuthenticated() {
      return this.$store?.state?.user?.isAuthenticated || false
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

      if (resp.data && resp.data.course) {
        this.course = resp.data.course
        this.lessons = resp.data.lesson || []
      } else {
        this.course = resp.data
        this.lessons = resp.data.lessons || resp.data.lesson || []
      }

      this.activeLesson = (this.lessons && this.lessons.length) ? this.lessons[0] : null

    } catch (err) {
      console.error('Failed to load course:', err)
      if (err.response && err.response.status === 404) {
        this.error = 'Course not found.'
      } else if (err.response && (err.response.status === 401 || err.response.status === 403)) {
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
  },

  methods: {
    setActiveLesson(lesson) {
      this.activeLesson = lesson
      console.log('setActiveLesson ->', lesson)
    },

    async submitComment() {
      console.log('submitComment called', { comment: this.comment, activeLesson: this.activeLesson, course: this.course })

      if (!this.course || !this.course.slug) {
        alert('Course not loaded correctly.')
        return
      }
      if (!this.activeLesson || !this.activeLesson.slug) {
        alert('Please select a lesson first.')
        return
      }
      if (!this.comment.name || !this.comment.content) {
        alert('Please fill both name and content.')
        return
      }

      const url = `/api/v1/courses/${this.course.slug}/lessons/${this.activeLesson.slug}/comments/`
      console.log('POST URL:', url)

      const token = localStorage.getItem('token')
      const headers = { 'Content-Type': 'application/json' }
      if (token) headers['Authorization'] = 'Token ' + token

      try {
        const resp = await axios.post(url, this.comment, { headers })
        console.log('comment created:', resp.data)
        this.comment.name = ''
        this.comment.content = ''
        alert('The comment was added!')
      } catch (err) {
        console.error('Failed to submit comment:', err, err.response && err.response.data)
        if (err.response) {
          alert('Server error: ' + JSON.stringify(err.response.data))
        } else {
          alert('Network error while submitting comment.')
        }
      }
    }
  }
}
</script>
