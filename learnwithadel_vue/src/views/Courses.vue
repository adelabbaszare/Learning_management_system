<template>
    <div class="courses">
        <div class="hero is-info">
            <div class="hero-body has-text-centered">
                <h1 class="subtitle">Courses📖</h1>
                <h2 class="subtitle">An Online place for learning what you want</h2>
            </div>
        </div>

        <section class="section">
            <div class="container">
                <div class="columns">
                    <div class="column is-2">
                        <aside class="menu">
                            <p class="menu-label">Categories</p>

                            <ul class="menu-list">
                                <li><a class="is-active">All Courses</a></li>
                                <li><a>Python</a></li>
                                <li><a>Machine Learning</a></li>
                                <li><a>Data Science</a></li>
                                <li><a>Artificial Intelligence</a></li>
                            </ul>
                        </aside>
                    </div>

                    <div class="column is-10">
                        <div class="columns is-multiline is-variable is-10">
                            <div
                                class="column is-4"
                                v-for="course in courses"
                                :key="courses.id"
                            >

                                <CourseItem :course="course" />
                            </div>


                            <div class="column is-12">
                                <nav class="pagination">
                                    <a class="pagination-previous">Previous</a>
                                    <a class="pagination-next">Next</a>

                                    <ul class="pagination-list">
                                        <li>
                                            <a class="pagination-link is-current">1</a>
                                        </li>
                                        <li>
                                            <a class="pagination-link">2</a>
                                        </li>
                                        <li>
                                            <a class="pagination-link">3</a>
                                        </li>
                                    </ul>
                                </nav>
                            </div>
                        </div>
                    </div>

                </div>
            </div>
        </section>
    </div>
</template>


<style scoped>
.card.is-fullheight {
    height: 100%;
    display: flex;
    flex-direction: column;
}
</style>


<script>
import CourseItem from '@/components/CourseItem.vue';
import axios from 'axios'

export default {
    data() {
        return {
            courses: [],
            categories: [],
            activeCategory: null
        }
    },
    components: {
        CourseItem
    },
    async mounted() {
        console.log('mounted')

        await axios
            .get('api/v1/courses/get_categories')
            .then(response => {
                console.log(response.data)
            })

        await axios
            .get('/api/v1/courses')
            .then(response => {
                console.log(response.data)

                this.courses = response.data
            })
    }
}
</script>