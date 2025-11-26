<template>
  <div class="courses">
    <div class="hero is-info">
      <div class="hero-body has-text-centered">
        <h1 class="title is-3 has-text-weight-bold" v-if="course">{{ course.title }} 
          <router-link
            :to="{name: 'Author', params: {id: course.created_by.id}}"
            class="subtitle is-5 has-text-weight-bold">
            Author : {{ course.created_by.first_name + ' ' + course.created_by.last_name }}
          </router-link>
        </h1>
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

                
                <template v-if="activeLesson">
                  <h2>{{ activeLesson.title }}</h2>
                  
                  <span 
                      class="tag is-warning" 
                      v-if="activity && activity.status === 'started'"
                      @click="markAsDone"
                    >
                    Started (mark as done)
                  </span>

                  <span class="tag is-success" v-else>Done</span>
                </template>

                <template v-else>
                  <h2>Introduction</h2>
                </template>

                <div v-if="activeLesson && activeLesson.long_description" v-html="activeLesson.long_description"></div>
                <div v-else-if="course.long_description" v-html="course.long_description"></div>
                <div v-else-if="course.short_description">{{ course.short_description }}</div>
                <div v-else>No description available.</div>

                <hr />

                <template v-if="activeLesson">
                  <template v-if="activeLesson.lesson_type === 'quiz'">
                    <Quiz :quiz="quiz" />
                  </template>

                  <template v-if="activeLesson.lesson_type === 'video'">
                    <Video :youtube_id="activeLesson.youtube_id" />
                  </template>

                  <template v-if="activeLesson.lesson_type === 'article'">
                    <CourseComment
                      v-for="comment in comments"
                      :key="comment.id"
                      :comment="comment"
                    />
                    <AddComment
                      :course="course"
                      :activeLesson="activeLesson"
                      :isAuthenticated="isAuthenticated"   :currentUser="currentUser"         @submitComment="submitComment"
                    />
                  </template>
                </template>

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

import CourseComment from '@/components/CourseComment.vue';
import AddComment from '@/components/AddComment.vue';
import Quiz from '@/components/Quiz.vue';
import Video from '@/components/Video.vue';

export default {
  components: {
    CourseComment,
    AddComment,
    Quiz,
    Video,
  },
  data() {
    return {
      course: {
        created_by: {
          id: 0
        }
      },
      lessons: [],
      comments: [],
      activeLesson: null,
      loading: false,
      error: null,
      quiz: {},
      activity: {}
    }
  },
  computed: {
    isAuthenticated() {
      return this.$store?.state?.user?.isAuthenticated || false
    },
    currentUser() {
    return this.$store?.state?.user || {} 
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
      const resp = await axios.get(`courses/${slug}/`)
      console.log('course fetch', resp.data)

      if (resp.data && resp.data.course) {
        this.course = resp.data.course
        this.lessons = resp.data.lesson || []
      } else {
        this.course = resp.data
        this.lessons = resp.data.lessons || resp.data.lesson || []
      }

      this.activeLesson = (this.lessons && this.lessons.length) ? this.lessons[0] : null

      if (this.activeLesson && this.activeLesson.lesson_type === 'article') {
          this.getComments() 
      }

      document.title = this.course.title + ' | LearnwithAdel'

    } catch (err) {
      console.error('Failed to load course:', err)
      if (err.response && err.response.status === 404) {
        this.error = 'Course not found.'
      } else if (err.response && (err.response.status === 401 || err.response.status === 403)) {
        try {
          const listResp = await axios.get('courses/')
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
    submitComment(comment) {
      this.comments.push(comment)
    },


    setActiveLesson(lesson) {
      this.activeLesson = lesson
      console.log('setActiveLesson ->', lesson)

      // Reset
      this.quizResult = null
      this.selectedAnswer = ''
      this.quiz = {} // Delete Previous Quiz
      this.comments = [] // Delete Previous Comments

      if (lesson.lesson_type === 'quiz') {  
        this.getQuiz()
      } else {
      // get comments for the selected lesson and article type, not quiz
      this.getComments()
      }

      this.trackSatrted()
    },


    trackSatrted() {
      const token = localStorage.getItem('token')
      const headers = {}
      if (token) headers['Authorization'] = 'Token ' + token

      axios
        .post(`activities/track_started/${this.$route.params.slug}/lessons/${this.activeLesson.slug}/`)
        .then(response => {
          console.log(response.data)

          this.activity = response.data
        })
    },
    

    markAsDone() {
      const token = localStorage.getItem('token')
      const headers = {}
      if (token) headers['Authorization'] = 'Token ' + token
      
      axios
        .post(`activities/mark_as_done/${this.$route.params.slug}/lessons/${this.activeLesson.slug}/`)
        .then(response => {
          console.log(response.data)

          this.activity = response.data
        })
    },


    getQuiz() {
      axios
        .get (`courses/${this.course.slug}/lessons/${this.activeLesson.slug}/get-quiz/`)
        .then(response => {
          console.log(response.data)

          this.quiz = response.data
        })
    },

    getComments() {
      // make sure course and activeLesson are set
      if (!this.course || !this.course.slug || !this.activeLesson || !this.activeLesson.slug) {
        console.warn('getComments: course or lesson not ready yet')
        this.comments = []
        return
      }

      const url = `courses/${this.course.slug}/lessons/${this.activeLesson.slug}/comments/get-comments/`
      console.log('GET comments URL:', url)

      const token = localStorage.getItem('token')
      const headers = {}
      if (token) headers['Authorization'] = 'Token ' + token

      axios
        .get(url, { headers })
        .then(response => {
          console.log('getComments response:', response.data)
          this.comments = response.data
        })
        .catch(err => {
          console.error('Failed to fetch comments:', err, err?.response?.data)
          // fallback: clear comments and optionally show a message
          this.comments = []
        })
    },
  }
}
</script>