<template>
  <div class="about">
    <div class="hero is-info">
      <div class="hero-body has-text-centered">
        <h1 class="title">Create Course</h1>
        <h2 class="subtitle">Welcome to Create Course</h2>
      </div>
    </div>

        <section class="section">
            <form v-on:submit.prevent="submitForm">
                <div class="field">
                    <label>Title</label>
                    <input type="text" class="input" v-model="form.title"></input>
                </div>
                
                <div class="field">
                    <label>Short Description</label>
                    <textarea class="textarea" v-model="form.short_description"></textarea>
                </div>
                
                <div class="field">
                    <label>Long Description</label>
                    <textarea class="textarea" v-model="form.long_description"></textarea>
                </div>

                <div class="field">
                    <div class="control has-icons-left">
                        <div class="select">
                            <select v-model="form.categories">
                                <option
                                v-for="category in categories"
                                v-bind:key="category.id"
                                v-bind:value="category.id"
                                    selected
                                >
                                    {{category.title}}</option>
                            </select>
                        </div>
                        <span class="icon is-left">
                            <i class="fas fa-bookmark"></i>
                        </span>
                    </div>
                </div>

                <div class="field">
                    <button class="button is success">Submit</button>
                </div>
            </form>
        </section>
    </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      form: {
        title: '',
        short_description: '',
        long_description: '',
        // single-select: store the selected category id (not an array)
        categories: null,
      },
      categories: [],
    }
  },
  mounted() {
    this.getCategories()
  },
  methods: {
    getCategories() {
      console.log('getCategories')

      axios
        .get('courses/get_categories/')
        .then(response => {
          console.log(response.data)
          this.categories = response.data

          if (this.categories && this.categories.length > 0 && !this.form.categories) {
            const first = this.categories[0]
            this.form.categories = first.id ?? first.value ?? first
          }
        })
        .catch(err => {
          console.error('failed to load categories', err)
        })
    },
    submitForm() {
      console.log('submitForm')
      console.log(this.form)

      axios
        .post('courses/create', this.form)
        .then(response => {
            console.log(response.data)
        })
        .catch(err => {
          console.error('failed to load categories', err)
        })
    }
  }
}
</script>