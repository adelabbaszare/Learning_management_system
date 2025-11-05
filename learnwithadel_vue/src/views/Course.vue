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

                <template v-if="activeLesson">
                  <template v-if="activeLesson.lesson_type === 'quiz'" >
                    <h3>{{ quiz.question }}</h3>

                    <div class="control">
                      <label class="radio">
                        <input type="radio" :value="quiz.op1" v-model="selectedAnswer">{{ quiz.op1 }}</input>
                      </label>
                    </div>

                    <div class="control">
                      <label class="radio">
                        <input type="radio" :value="quiz.op2" v-model="selectedAnswer">{{ quiz.op2 }}</input>
                      </label>
                    </div>

                    <div class="control">
                      <label class="radio">
                        <input type="radio" :value="quiz.op3" v-model="selectedAnswer">{{ quiz.op3 }}</input>
                      </label>
                    </div>

                    <div class="control mt-4">
                      <button class="button is-info" @click="sumbitQuiz">Submit</button>
                    </div>

                    <template v-if="quizResult == 'correct' ">
                      <div class="notification is-success mt-4">Correct✅</div>
                    </template>


                    <template v-if="quizResult == 'incorrect' ">
                      <div class="notification is-danger mt-4">Wrong❌, Please Try Again</div>
                    </template>
                  </template>
                

                  <template v-if="activeLesson.lesson_type === 'article'">
                    <CourseComment
                      v-for="comment in comments" 
                      v-bind:key="comment.id" 
                      v-bind:comment="comment"
                    />

                    <AddComment
                      v-bind:course="course"
                      v-bind:activeLesson="activeLesson"
                      v-on:submitComment="submitComment"
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

export default {
  components: {
    CourseComment,
    AddComment,
  },
  data() {
    return {
      course: null,
      lessons: [],
      comments: [],
      activeLesson: null,
      // comment: { name: '', content: '' },
      loading: false,
      error: null,
      quiz: {},
      selectedAnswer: '',
      quizResult: null
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

      document.title = this.course.title + ' | LearnwithAdel'

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
    submitComment(comment) {
      this.comments.push(comment)

    },

    sumbitQuiz() {
      this.quizResult = null

      if (this.selectedAnswer) {
        if (this.selectedAnswer === this.quiz.answer) {
          this.quizResult = 'correct'
        } else {
          this.quizResult = 'incorrect'
        }
      } else {
        alert('Select Answer First')
      }
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
    },

    getQuiz() {
      axios
        .get (`/api/v1/courses/${this.course.slug}/lessons/${this.activeLesson.slug}/get-quiz/`)
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

      const url = `/api/v1/courses/${this.course.slug}/lessons/${this.activeLesson.slug}/comments/get-comments`
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