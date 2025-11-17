<template>
  <div class="about">
    <div class="hero is-info">
      <div class="hero-body has-text-centered">
        <h1 class="title">Create Course</h1>
        <h2 class="subtitle">Welcome to Create Course</h2>
      </div>
    </div>

        <section class="section">
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
                          <select v-model.number="form.categories">
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

              <div class="field buttons">
                  <button class="button is-success" @click="submitForm('draft')">Save as draft</button>
                  <button class="button is-info" @click="submitForm('review')">Submit as review</button>
              </div>
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
        status: ''
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
    submitForm(status) {
      console.log('submitForm')
      console.log(this.form)

      this.form.status = status

      // normalize categories -> always an array (handles single id or already-array)
      const payload = {
        ...this.form,
        categories: Array.isArray(this.form.categories)
          ? this.form.categories
          : (this.form.categories == null ? [] : [this.form.categories])
      }

      axios
        .post('courses/create/', payload)
        .then(response => {
          console.log(response.data)
        })
        .catch(error => {
          console.error('failed to create course', error)
        })
    }
  }
}
</script>