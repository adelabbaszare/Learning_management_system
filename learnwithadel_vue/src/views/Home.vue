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
/*.hero.has-background-image {
    background: url('https://static.vecteezy.com/system/resources/previews/067/865/560/non_2x/millimeter-graph-paper-grid-technical-and-educational-template-for-engineering-math-and-design-vector.jpg') center center no-repeat;
    background-size: cover;
    position: relative;
}*/
.hero.has-background-color {
  background: rgba(0, 0, 0, 0.792);
}
.hero-overlay {
    position: absolute; top: 0; left: 0; width: 100%; height: 100%;
    background-color: rgba(0, 0, 0, 0.792);
    background-color: linear-gradient(to right, transparent, black 5%, black 95%, transparent);
}
.relative-z { position: relative; z-index: 1; }

.overflow-hidden {
    overflow: hidden;
}

.marquee-wrapper {
    width: 100%;
    overflow: hidden;
    position: relative;
    mask-image: linear-gradient(to right, transparent, black 5%, black 95%, transparent);
    -webkit-mask-image: linear-gradient(to right, transparent, black 5%, black 95%, transparent);
}

.marquee-track {
    display: flex;
    width: max-content; 
    gap: 2rem;
    padding: 2rem 0;
    animation: scroll-left 20s linear infinite; 
}

.marquee-track:hover {
    animation-play-state: paused;
}

.marquee-item {
    width: 300px;
    flex-shrink: 0;
}

@keyframes scroll-left {
    0% {
        transform: translateX(0);
    }
    100% {
        transform: translateX(-50%); 
    }
}

@media screen and (max-width: 768px) {
    .marquee-item {
        width: 260px;
    }
    .marquee-track {
        animation-duration: 25s;
    }
}
</style>