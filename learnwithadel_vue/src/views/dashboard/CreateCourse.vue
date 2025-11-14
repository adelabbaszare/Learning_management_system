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
                    <button class="button is success">Submit</button>
                </div>
            </form>
        </section>
    </div>
</template>

<script>
export default {
    data(){
        return {
            form: {
                title: '',
                short_description: '',
                long_description: '',
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
        },
        submitForm() {
            console.log('submitForm')
            console.log(this.form)
        }
    }
}
</script>