<template>
  <div class="home">
    <div class="hero is-info is-medium">
      <div class="hero-body has-text-centered">
        <h1 class="title">Welcome to LearnwithAdel</h1>


        <h2 class="subtitle">An Online place for learning what you want</h2>
      </div>
    </div>

    <section class="section">
      <div class="container">
        <div class="columns is-multiline">
          <div class="column is-4">
            <div class="box has-text-centered">
              <span class="icon is-size-2 has-text-info"><i class="far fa-clock"></i></span>

              <h2 class="is-size-4 mt-4 mb-4">Study at your pace</h2>

              <p>This is just random placeholder text</p>
            </div>
          </div>

          <div class="column is-4">
            <div class="box has-text-centered">
              <span class="icon is-size-2 has-text-info"><i class="far fa-comments"></i></span>

              <h2 class="is-size-4 mt-4 mb-4">Study with others</h2>

              <p>This is just random placeholder text</p>
            </div>
          </div>

          <div class="column is-4">
            <div class="box has-text-centered">
              <span class="icon is-size-2 has-text-info"><i class="fas fa-home"></i></span>

              <h2 class="is-size-4 mt-4 mb-4">Study from your home</h2>

              <p>This is just random placeholder text</p>
            </div>
          </div>

          <div class="column is-12 has-text-centered">
            <a href="/sign-up" class="button is-onfo is-size-3 mt-6 mb-6">Click to get started</a>
          </div>

          <hr>
            <div
                class="column is-4"
                v-for="course in courses"
                :key="courses.id"
            >
                <CourseItem :course="course" />
            </div>
          </hr>

        </div>
      </div>
    </section>
  </div>
</template>

<script>
import CourseItem from '@/components/CourseItem.vue';
import axios from 'axios'

export default {
  name: 'Home',

  data() {
        return {
            courses: []
        }
    },
    components: {
        CourseItem
    },
    mounted() {
        console.log('mounted')

        document.title = 'LearnwithAdel'

        axios
            .get('/api/v1/courses/get_frontpage_courses/')
            .then(response => {
                console.log(response.data)

                this.courses = response.data
            })
    }
}
</script>
