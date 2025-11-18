<template>
  <div class="home">
    <section class="hero is-fullheight has-background-image">
      <div class="hero-overlay"></div>
      <div class="hero-body">
        <div class="container has-text-centered relative-z">
          <h1 class="title is-1 has-text-white mb-6">Welcome to LearnwithAdel</h1>
          <h2 class="subtitle is-3 has-text-light mb-6">An Online place for learning what you want</h2>
          <a href="/sign-up" class="button is-info is-large is-rounded mt-4 shadow-button">
            <strong>Click to get started</strong>
          </a>

          <CodeTypingAnimation />
          
        </div>
      </div>
    </section>

    <section class="section has-background-light">
       </section>

    <section class="section overflow-hidden">
      <div class="container is-fluid">
        <div class="level mb-6 px-4">
            <div class="level-left">
                <h2 class="title is-3">Latest Courses</h2>
            </div>
            <div class="level-right">
                 <a href="/courses" class="button is-text">View All</a>
            </div>
        </div>

        <div v-if="loading" class="has-text-centered p-6">
            <button class="button is-loading is-white is-large">Loading</button>
        </div>

        <div v-else class="marquee-wrapper">
            <div class="marquee-track">
                
                <div 
                    class="marquee-item"
                    v-for="course in courses"
                    :key="`first-${course.id}`"
                >
                    <CourseItem :course="course" />
                </div>

                <div 
                    class="marquee-item"
                    v-for="course in courses"
                    :key="`second-${course.id}`"
                >
                    <CourseItem :course="course" />
                </div>

            </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import CourseItem from '@/components/CourseItem.vue';
import CodeTypingAnimation from '@/components/CodeTypingAnimation.vue';
import axios from 'axios'

export default {
  name: 'Home',
  components: {
    CourseItem,
    CodeTypingAnimation
  },
  data() {
    return {
      courses: [],
      loading: false
    }
  },
  mounted() {
    this.getLatestCourses();
    document.title = 'Home | LearnwithAdel';
  },
  methods: {
    async getLatestCourses() {
        this.loading = true;
        try {
            const response = await axios.get('courses/get_frontpage_courses/');
            this.courses = response.data;
        } catch (error) {
            console.error('Error loading courses:', error);
        } finally {
            this.loading = false;
        }
    }
  }
}
</script>

<style scoped>
/* --- Hero Styles (از مرحله قبل) --- */
.hero.has-background-image {
    background: url('https://images.unsplash.com/photo-1501504905252-473c47e087f8?ixlib=rb-1.2.1&auto=format&fit=crop&w=1334&q=80') center center no-repeat;
    background-size: cover;
    position: relative;
}
.hero-overlay {
    position: absolute; top: 0; left: 0; width: 100%; height: 100%;
    background-color: rgba(0, 0, 0, 0.6);
}
.relative-z { position: relative; z-index: 1; }

/* --- Marquee Animation Styles (بخش جدید) --- */

/* جلوگیری از اسکرول افقی صفحه اصلی */
.overflow-hidden {
    overflow: hidden;
}

.marquee-wrapper {
    width: 100%;
    overflow: hidden; /* مخفی کردن آیتم‌هایی که از کادر خارج می‌شوند */
    position: relative;
    mask-image: linear-gradient(to right, transparent, black 5%, black 95%, transparent); /* افکت محو شدن در لبه‌ها */
    -webkit-mask-image: linear-gradient(to right, transparent, black 5%, black 95%, transparent);
}

.marquee-track {
    display: flex;
    width: max-content; /* عرض به اندازه محتوا باز می‌شود */
    gap: 2rem; /* فاصله بین آیتم‌ها */
    padding: 1rem 0;
    /* انیمیشن: نام، مدت زمان، مدل حرکت، تکرار */
    animation: scroll-left 40s linear infinite; 
}

/* توقف حرکت وقتی موس روی آیتم‌هاست */
.marquee-track:hover {
    animation-play-state: paused;
}

.marquee-item {
    width: 300px; /* عرض ثابت برای هر کارت دوره */
    flex-shrink: 0; /* جلوگیری از جمع شدن کارت‌ها */
}

/* تعریف انیمیشن */
@keyframes scroll-left {
    0% {
        transform: translateX(0);
    }
    100% {
        /* حرکت به اندازه منفی 50 درصد (چون محتوا دو بار تکرار شده، 50 درصد یعنی پایان سری اول) */
        transform: translateX(-50%); 
    }
}

/* ریسپانسیو: در موبایل سرعت کمی بیشتر باشد یا سایز تغییر کند */
@media screen and (max-width: 768px) {
    .marquee-item {
        width: 260px;
    }
    .marquee-track {
        animation-duration: 25s;
    }
}
</style>