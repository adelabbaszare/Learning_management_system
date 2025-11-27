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
              <!-- استفاده از sortedLessons به جای lessons برای اعمال ترتیب جدید -->
              <li v-for="lesson in sortedLessons" :key="lesson.id">
                <a href="#" @click.prevent="setActiveLesson(lesson)">
                  
                  <!-- منطق نمایش آیکون بر اساس lesson_type -->
                  <span v-if="lesson.lesson_type === 'article'" class="icon is-small has-text-info mr-2">
                    <i class="fas fa-book-open"></i> 
                  </span>
                  <span v-else-if="lesson.lesson_type === 'quiz'" class="icon is-small has-text-warning mr-2">
                    <i class="fas fa-question-circle"></i>
                  </span>
                  <span v-else-if="lesson.lesson_type === 'video'" class="icon is-small has-text-danger mr-2">
                    <i class="fas fa-video"></i>
                  </span>
                  
                  {{ lesson.title }}
                  
                </a>
              </li>
            </ul>
          </div>

          <div class="column is-10">
            <div v-if="loading">Loading...</div>
            <div v-else-if="error" class="notification is-danger">{{ error }}</div>

            <div v-else-if="course">
              <div v-if="isAuthenticated">

                
                <template v-if="activeLesson">
                  
                  <!-- نوار عنوان و ابزار (Action Bar) جدید -->
                  <div class="is-flex is-justify-content-space-between is-align-items-center mb-4">
                      <h2>{{ activeLesson.title }}</h2>
                      
                      <div class="buttons is-flex is-align-items-center">
                          <!-- دکمه وضعیت (Mark as Done) -->
                          <span 
                              class="tag is-small is-rounded is-clickable mr-3" 
                              :class="{'is-warning': activity && activity.status === 'started', 'is-success': activity && activity.status === 'done'}"
                              @click="markAsDone"
                              v-if="activity"
                              style="line-height: 24px;"
                          >
                            {{ activity && activity.status === 'started' ? 'شروع شده (بزن برای اتمام)' : 'تکمیل شده' }}
                          </span>
                          
                          <!-- آیکون گیت‌هاب -->
                          <a href="#" target="_blank" title="مشاهده کد در گیت‌هاب" class="action-icon">
                              <span class="icon is-medium">
                                  <i class="fab fa-github"></i>
                              </span>
                          </a>

                          <!-- آیکون گوگل کولب (Notebook) -->
                          <a href="#" target="_blank" title="اجرای نوت‌بوک در Google Colab" class="action-icon">
                              <span class="icon is-medium">
                                  <i class="fas fa-laptop-code"></i>
                              </span>
                          </a>

                          <!-- آیکون اشتراک‌گذاری -->
                          <a href="#" @click.prevent="shareLesson" title="به اشتراک‌گذاری" class="action-icon">
                              <span class="icon is-medium">
                                  <i class="fas fa-share-alt"></i>
                              </span>
                          </a>
                      </div>
                  </div>

                  <!-- متن اصلی درس -->
                  <div v-if="activeLesson && activeLesson.long_description" v-html="activeLesson.long_description"></div>
                
                </template>

                <template v-else>
                  <h2>Introduction</h2>
                  <div v-if="course.long_description" v-html="course.long_description"></div>
                  <div v-else-if="course.short_description">{{ course.short_description }}</div>
                  <div v-else>No description available.</div>
                </template>

                <hr />
                <!-- ادامه محتوای درس (Quiz, Video, Comments) -->
                <template v-if="activeLesson">

                  <template v-if="activeLesson.lesson_type === 'quiz'">
                    <div v-if="quizQuestions && quizQuestions.length > 0 && activeLesson" class="mt-6">
                      <h3 class="title is-3 has-text-info">تست درک مطلب</h3>
                      <!-- استفاده از key برای اجبار به ری‌رندر شدن کامپوننت Quiz برای سوال جدید -->
                      <Quiz
                          v-if="currentQuestionIndex < quizQuestions.length"
                          :key="currentQuestionIndex" 
                          :quiz="quizQuestions[currentQuestionIndex]"
                          :question-index="currentQuestionIndex"
                          :total-questions="quizQuestions.length"
                          @next="handleNextQuestion"
                      />
                      <!-- نمایش نتیجه نهایی کوییز -->
                      <div v-else class="box notification is-primary has-text-centered p-6">
                          <p class="title is-2 mb-4">نتایج کوییز</p>
                          <p class="subtitle is-4">
                              شما به **{{ score }}** سوال از **{{ quizQuestions.length }}** سوال پاسخ صحیح دادید.
                          </p>
                          <progress 
                              class="progress is-large" 
                              :class="score >= quizQuestions.length / 2 ? 'is-success' : 'is-danger'"
                              :value="score" 
                              :max="quizQuestions.length">
                          </progress>
                          <p class="mt-4 is-size-5 has-text-weight-semibold">
                              درصد موفقیت: {{ Math.round((score / quizQuestions.length) * 100) }}%
                          </p>
                          <button class="button is-link is-light mt-5" @click="startQuizAgain">
                              شروع مجدد کوییز
                          </button>
                      </div>
                    </div>
                  </template>

                  <template v-if="activeLesson.lesson_type === 'video'">
                    <Video :youtube_id="activeLesson.youtube_id" />
                  </template>

                  <template v-if="activeLesson.lesson_type === 'article' || activeLesson.lesson_type === 'video'">
                    <!-- اضافه کردن بخش کامنت‌ها فقط برای درس‌های Article و Video -->
                    <CourseComment
                      v-for="comment in comments"
                      :key="comment.id"
                      :comment="comment"
                    />
                    <AddComment
                      :course="course"
                      :activeLesson="activeLesson"
                      :isAuthenticated="isAuthenticated" 
                      :currentUser="currentUser"  
                      @submitComment="submitComment"
                    />
                  </template>

                </template>
                <!-- پایان محتوای درس -->

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
import hljs from 'highlight.js';

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
      
      quizQuestions: [],
      currentQuestionIndex: 0,
      score: 0,
      activity: {}
    }
  },
  computed: {
    isAuthenticated() {
      return this.$store?.state?.user?.isAuthenticated || false
    },
    currentUser() {
    return this.$store?.state?.user || {} 
    },
    // New computed property to sort lessons by type: article -> quiz -> video
    sortedLessons() {
      // 1. ایجاد یک کپی از آرایه lessons برای جلوگیری از تغییر مستقیم وضعیت
      const lessonsCopy = [...this.lessons];
      
      // 2. تعریف تابع مقایسه‌ای برای مرتب‌سازی
      const getLessonTypeOrder = (type) => {
        if (type === 'article') return 1;
        if (type === 'quiz') return 2;
        if (type === 'video') return 3;
        return 99; // برای انواع نامشخص
      };

      // 3. مرتب‌سازی بر اساس نوع و سپس بر اساس ترتیب اصلی (Index)
      return lessonsCopy.sort((a, b) => {
        const orderA = getLessonTypeOrder(a.lesson_type);
        const orderB = getLessonTypeOrder(b.lesson_type);

        if (orderA !== orderB) {
          // اگر نوع درس‌ها متفاوت است، بر اساس نوع مرتب کن
          return orderA - orderB;
        } else {
          // اگر نوع درس‌ها یکسان است، بر اساس id یا ترتیب اصلی (a.id - b.id) مرتب کن
          // در اینجا فرض می‌کنیم که idها ترتیب اصلی ایجاد را حفظ می‌کنند.
          return a.id - b.id;
        }
      });
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
        // تضمین می‌کنیم که lessons به عنوان آرایه‌ای از آبجکت‌های درس ذخیره شود.
        this.lessons = (Array.isArray(resp.data.lessons) ? resp.data.lessons : resp.data.lesson) || []
      }

      // تنظیم اولین درس فعال به عنوان اولین درس مرتب‌شده (اگر وجود داشته باشد)
      this.activeLesson = (this.sortedLessons && this.sortedLessons.length) ? this.sortedLessons[0] : null
      
      // فراخوانی داده‌های درس اولیه
      if (this.activeLesson) {
          this.fetchLessonData(this.activeLesson)
      }

      this.$nextTick(() => {
        hljs.highlightAll(); 
      });

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

      // Reset all lesson-specific data
      this.comments = [] 
      this.quizQuestions = [] 
      this.currentQuestionIndex = 0
      this.score = 0
      this.activity = {}

      history.pushState({}, null, `#${lesson.slug}`)

      this.fetchLessonData(lesson)

      this.$nextTick(() => {
        hljs.highlightAll(); 
      });
    },

    // متد جدید برای فراخوانی داده‌های مربوط به درس
    fetchLessonData(lesson) {
        // فراخوانی داده‌های وابسته به نوع درس
        if (lesson.lesson_type === 'quiz') {  
            this.getQuiz()
        } else if (lesson.lesson_type === 'article' || lesson.lesson_type === 'video') {
            this.getComments()
        }
        
        // Track started for all lesson types
        this.trackSatrted()
    },


    trackSatrted() {
      if (!this.activeLesson) return 
      
      const token = localStorage.getItem('token')
      const headers = {}
      if (token) headers['Authorization'] = 'Token ' + token

      axios
        .post(`activities/track_started/${this.$route.params.slug}/lessons/${this.activeLesson.slug}/`, null, { headers })
        .then(response => {
          console.log(response.data)

          this.activity = response.data
        })
    },
    

    markAsDone() {
      if (!this.activeLesson) return 

      const token = localStorage.getItem('token')
      const headers = {}
      if (token) headers['Authorization'] = 'Token ' + token
      
      axios
        .post(`activities/mark_as_done/${this.$route.params.slug}/lessons/${this.activeLesson.slug}/`, null, { headers })
        .then(response => {
          console.log(response.data)

          this.activity = response.data
        })
    },

    shareLesson() {
        const shareData = {
            title: this.activeLesson.title + ' | ' + this.course.title,
            text: `درس جذاب ${this.activeLesson.title} از دوره ${this.course.title} را در LearnwithAdel ببین!`,
            url: window.location.href,
        };

        if (navigator.share) {
            navigator.share(shareData)
                .then(() => console.log('محتوا با موفقیت به اشتراک گذاشته شد.'))
                .catch((error) => console.error('خطا در اشتراک گذاری:', error));
        } else {
            const tempInput = document.createElement('input');
            tempInput.value = shareData.url;
            document.body.appendChild(tempInput);
            tempInput.select();
            
            try {
                document.execCommand('copy');
                alert('لینک درس در حافظه کپی شد!');
            } catch (err) {
                console.error('Failed to copy text: ', err);
            }
            document.body.removeChild(tempInput);
        }
    },


    getQuiz() {
      if (!this.course || !this.activeLesson) return
      axios
        .get (`courses/${this.course.slug}/lessons/${this.activeLesson.slug}/get-quiz/`)
        .then(response => {
            console.log("Quiz Loaded:", response.data)
            this.quizQuestions = Array.isArray(response.data) ? response.data : (response.data ? [response.data] : [])
        })
        .catch(error => {
          console.error('خطا در بارگذاری کوییز:', error)
          this.quizQuestions = []
        })
    },

    handleNextQuestion(isCorrect) {
      if (isCorrect) {
        this.score++; 
      }
      this.currentQuestionIndex++; 
    },

    startQuizAgain() {
      this.currentQuestionIndex = 0;
      this.score = 0;
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

<style>
.action-icon {
    color: #485fc7;
    transition: color 0.3s ease, background-color 0.3s ease;
    border-radius: 50%;
    width: 36px; 
    height: 36px;
    display: flex;
    justify-content: center;
    align-items: center;
    margin-left: 0.5rem;
}

.action-icon:hover {
    color: #fff; 
    background-color: #9400d3;
    box-shadow: 0 4px 8px rgba(148, 0, 211, 0.4);
}

.action-icon .icon {
  line-height: 1;
}


/* @import url('https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/monokai.min.css'); */

.content pre {
  padding: 1rem;
  overflow-x: auto;
  border-radius: 6px;
}

.content pre code {
  background-color: transparent !important; 
  color: unset !important; 
  padding: 0;
}
</style>